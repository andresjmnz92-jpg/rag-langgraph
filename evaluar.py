"""Corre las 20 preguntas por el agente y deja la calificación a medio hacer.

Los 4 controles se califican solos: su respuesta correcta es una frase exacta.
Las 16 restantes no — juzgar si una respuesta en prosa dice lo que dice la norma
necesita a alguien que sepa leerla. El script comprueba lo que sí es objetivo
(¿citó la sección correcta?) y deja la casilla de contenido vacía para que la
llene una persona, con la respuesta verificada al lado.

Un archivo por corrida, con su fecha y su corpus en el nombre: un resultado sin
las condiciones que lo produjeron no es un resultado.
"""

import os, sys, time
from datetime import date
from golden import PREGUNTAS
from agente import agente, TOP_K, MAX_VUELTAS, MODELO, MODELO_URL
from recuperar import TABLA

PRECIO_ENTRADA = 0.13 / 1_000_000   # gpt-5-mini, verificado el 10 ago 2026
PRECIO_SALIDA = 1.00 / 1_000_000
# El modelo local corre en el PC de Andres: la factura es la luz, no fichas. Dejar
# el precio de OpenAI aqui reportaria un costo que nadie pago.
if MODELO_URL:
    PRECIO_ENTRADA = PRECIO_SALIDA = 0.0


def se_nego(respuesta):
    """La negativa exacta, tolerando la tilde que el modelo pone o no pone."""
    return "no encontre eso en los documentos cargados" in respuesta.lower().replace("é", "e")


def cito(respuesta, secciones):
    return any(s in respuesta for s in secciones)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    filas = []
    for p in PREGUNTAS:
        t0 = time.perf_counter()
        salida = agente.invoke({"pregunta": p["pregunta"]})
        p = {**p, "respuesta": salida["respuesta"], "uso": salida["uso"],
             "segundos": time.perf_counter() - t0}
        p["ok"] = se_nego(p["respuesta"]) if not p["secciones"] else cito(p["respuesta"], p["secciones"])
        filas.append(p)
        print(f"  {p['n']}/20 listo", file=sys.stderr)

    controles = [f for f in filas if not f["secciones"]]
    conresp = [f for f in filas if f["secciones"]]
    entrada = sum(f["uso"]["entrada"] for f in filas)
    salida_t = sum(f["uso"]["salida"] for f in filas)
    costo = entrada * PRECIO_ENTRADA + salida_t * PRECIO_SALIDA

    os.makedirs("resultados", exist_ok=True)
    # Las condiciones van en el nombre: sin ellas, dos corridas del mismo dia se
    # pisan y la segunda borra la primera. Los dos puntos de "qwen3:4b" no son
    # validos en un nombre de archivo de Windows.
    etiqueta = f"top{TOP_K}-v{MAX_VUELTAS}-{MODELO.replace(':', '-').replace('/', '-')}"
    ruta = f"resultados/{date.today()}-{TABLA}-{etiqueta}.md"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"# {TABLA} — 20 preguntas · topK {TOP_K} · "
                f"max {MAX_VUELTAS} vuelta(s) · {MODELO} · {date.today()}\n\n")
        f.write(f"- Controles superados (automático): **{sum(1 for c in controles if c['ok'])}/4**\n")
        f.write(f"- Citó la sección esperada (automático): **{sum(1 for c in conresp if c['ok'])}/16**\n")
        f.write(f"- Segundos por consulta: **{sum(x['segundos'] for x in filas)/len(filas):.1f}** de media\n")
        f.write(f"- Fichas: {entrada:,} entrada + {salida_t:,} salida — **${costo:.3f}** las 20\n\n")
        f.write("La columna **Contenido** va vacía a propósito: es la que no puede llenar un script.\n\n")
        for x in filas:
            f.write(f"## {x['n']}. {x['pregunta']}\n\n")
            f.write(f"**Esperada** (§ {'/'.join(x['secciones']) or 'ninguna, es control'})\n\n")
            f.write(f"> {x['esperada'].replace(chr(10), chr(10) + '> ')}\n\n")
            f.write(f"**Obtenida** — {x['segundos']:.1f}s, {x['uso']['entrada']}+{x['uso']['salida']} fichas\n\n")
            f.write(f"> {x['respuesta'].replace(chr(10), chr(10) + '> ')}\n\n")
            f.write(f"Cita/negativa: {'✅' if x['ok'] else '❌'} · **Contenido: [ ]**\n\n---\n\n")

    print(f"\nControles {sum(1 for c in controles if c['ok'])}/4 · "
          f"Citas {sum(1 for c in conresp if c['ok'])}/16 · ${costo:.3f}")
    print(f"Escrito {ruta} — te toca llenar las casillas de Contenido.")



if __name__ == "__main__":
    main()
