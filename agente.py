from typing import TypedDict
from openai import OpenAI
from langgraph.graph import StateGraph, START, END
from recuperar import buscar_fragmentos

# Las mismas cinco reglas del workflow de n8n, palabra por palabra. Si se
# cambian, la comparacion deja de medir el framework y pasa a medir el prompt.
REGLAS = """Eres un asistente que responde UNICAMENTE con base en los documentos indexados.

Reglas:
1. Antes de responder, SIEMPRE usa la herramienta "Buscar en Documentos".
2. Responde solo con lo que aparezca en los fragmentos recuperados. No uses tu conocimiento propio.
3. Cita siempre de que documento salio la respuesta.
4. Si la respuesta no esta en los fragmentos, responde exactamente: "No encontre eso en los documentos cargados." No la inventes.
5. Responde en espanol, corto y directo."""


class Estado(TypedDict):
    pregunta: str
    fragmentos: list
    respuesta: str
    uso: dict



def nodo_buscar(estado):
    return {"fragmentos": buscar_fragmentos(estado["pregunta"], 20)}


def nodo_redactar(estado):
    contexto = "\n\n".join(
        f"[Seccion {f['seccion']} - {f['cita']}]\n{f['texto']}" for f in estado["fragmentos"]
    )
    respuesta = OpenAI().chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": REGLAS},
            {"role": "user", "content": f"Fragmentos:\n{contexto}\n\nPregunta: {estado['pregunta']}"},
        ],
    )
    return {
        "respuesta": respuesta.choices[0].message.content,
        "uso": {"entrada": respuesta.usage.prompt_tokens, "salida": respuesta.usage.completion_tokens},
    }



grafo = StateGraph(Estado)
grafo.add_node("buscar", nodo_buscar)
grafo.add_node("redactar", nodo_redactar)
grafo.add_edge(START, "buscar")
grafo.add_edge("buscar", "redactar")
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
