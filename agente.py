import os
from typing import Annotated, TypedDict
from openai import OpenAI
from langgraph.graph import StateGraph, START, END
from recuperar import buscar_fragmentos

# El mismo tope que el agente de n8n. No es una meta: la ejecucion 551 acerto
# con dos vueltas. Es el freno de mano por si el juez nunca se da por satisfecho.
MAX_VUELTAS = 5

# 20 se heredo del chat de n8n; nadie lo midio. Con el corpus v4 el fragmento
# que responde llega en el puesto 2, asi que los otros 18 se pagan en cada
# consulta sin saber si aportan. Por variable de entorno para poder correr las
# dos y comparar sin editar el archivo entre corridas. Cuando el numero decida,
# esto vuelve a ser una constante.
TOP_K = int(os.environ.get("TOP_K", 20))

# Las mismas cinco reglas del workflow de n8n, palabra por palabra. Si se
# cambian, la comparacion deja de medir el framework y pasa a medir el prompt.
REGLAS = """Eres un asistente que responde UNICAMENTE con base en los documentos indexados.

Reglas:
1. Antes de responder, SIEMPRE usa la herramienta "Buscar en Documentos".
2. Responde solo con lo que aparezca en los fragmentos recuperados. No uses tu conocimiento propio.
3. Cita siempre de que documento salio la respuesta.
4. Si la respuesta no esta en los fragmentos, responde exactamente: "No encontre eso en los documentos cargados." No la inventes.
5. Responde en espanol, corto y directo."""


# El juez no responde la pregunta: decide si ya se puede responder. Se le pasan
# los fragmentos enteros a proposito — el vocabulario para la segunda busqueda
# esta dentro de lo que trajo la primera.
JUEZ = """Decides si unos fragmentos de normativa contienen la respuesta a una pregunta.

Si la contienen, responde exactamente: SUFICIENTE
Si no, responde SOLO una consulta de busqueda nueva, sin explicar nada. Escribela con
el vocabulario literal que veas en los fragmentos (los documentos estan en ingles) y
no repitas la consulta anterior."""


def sumar_uso(anterior, nuevo):
    anterior = anterior or {}
    return {k: anterior.get(k, 0) + nuevo.get(k, 0) for k in ("entrada", "salida")}


class Estado(TypedDict):
    pregunta: str
    consulta: str
    vueltas: int
    fragmentos: list
    respuesta: str
    uso: Annotated[dict, sumar_uso]


def preguntar_al_modelo(sistema, usuario):
    r = OpenAI().chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "system", "content": sistema},
                  {"role": "user", "content": usuario}],
    )
    return r.choices[0].message.content, {"entrada": r.usage.prompt_tokens,
                                          "salida": r.usage.completion_tokens}


def formatear(fragmentos):
    return "\n\n".join(f"[Seccion {f['seccion']} - {f['cita']}]\n{f['texto']}" for f in fragmentos)


def nodo_buscar(estado):
    # Los fragmentos se acumulan entre vueltas, como el historial del agente de
    # n8n: si la segunda busqueda sale peor, lo bueno de la primera no se pierde.
    ya = estado.get("fragmentos") or []
    vistos = {f["texto"] for f in ya}
    nuevos = buscar_fragmentos(estado.get("consulta") or estado["pregunta"], TOP_K)
    return {"fragmentos": ya + [f for f in nuevos if f["texto"] not in vistos],
            "vueltas": estado.get("vueltas", 0) + 1}


def nodo_decidir(estado):
    veredicto, uso = preguntar_al_modelo(
        JUEZ,
        f"Fragmentos:\n{formatear(estado['fragmentos'])}\n\n"
        f"Pregunta: {estado['pregunta']}\nConsulta anterior: {estado.get('consulta') or estado['pregunta']}",
    )
    return {"consulta": "" if "SUFICIENTE" in veredicto else veredicto.strip(), "uso": uso}


def otra_vuelta(estado):
    return "buscar" if estado["consulta"] and estado["vueltas"] < MAX_VUELTAS else "redactar"


def nodo_redactar(estado):
    respuesta, uso = preguntar_al_modelo(
        REGLAS,
        f"Fragmentos:\n{formatear(estado['fragmentos'])}\n\nPregunta: {estado['pregunta']}",
    )
    return {"respuesta": respuesta, "uso": uso}



grafo = StateGraph(Estado)
grafo.add_node("buscar", nodo_buscar)
grafo.add_node("decidir", nodo_decidir)
grafo.add_node("redactar", nodo_redactar)
grafo.add_edge(START, "buscar")
grafo.add_edge("buscar", "decidir")
grafo.add_conditional_edges("decidir", otra_vuelta, ["buscar", "redactar"])
grafo.add_edge("redactar", END)
agente = grafo.compile()


def preguntar(pregunta):
    return agente.invoke({"pregunta": pregunta})["respuesta"]


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for p in ["¿Qué plazo tiene una entidad para notificar a los individuos afectados por una brecha?",
              "¿Cuál es la multa máxima del GDPR?"]:
        print(f"\nP: {p}\nR: {preguntar(p)}")
