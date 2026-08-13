import os, json, requests, psycopg
from pathlib import Path
from dotenv import load_dotenv

# Con ruta absoluta a proposito: el servidor MCP lo arranca Claude desde su
# propio directorio, y un load_dotenv() a secas busca el .env en el cwd.
load_dotenv(Path(__file__).parent / ".env")

TABLA = "documentos_v4"


def conectar():
    # connect_timeout no sobra: sin el, con el tunel caido psycopg espera 130 s
    # antes de rendirse. Un chequeo de salud que se cuelga se lee como "lento"
    # en vez de "caido", que es la peor de las dos lecturas.
    return psycopg.connect(
        host="127.0.0.1", port=5433,
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=5,
    )

def vectorizar(texto):
    r = requests.post("http://127.0.0.1:11435/api/embed",
                      json={"model": "bge-m3:latest", "input": texto}, timeout=120)
    r.raise_for_status()
    vectores = r.json().get("embeddings") or []
    if not vectores:
        raise RuntimeError(f"Ollama devolvio vacio para: {texto!r}")
    return vectores[0]

def buscar_fragmentos(pregunta, limite=20):
    vec = vectorizar(pregunta)
    with conectar() as c:
        filas = c.execute(
            f"SELECT text, metadata->>'seccion', metadata->>'citation' FROM {TABLA} "
            "ORDER BY embedding <=> %s::vector LIMIT %s",
            (json.dumps(vec), limite),
        ).fetchall()
    return [{"texto": t, "seccion": s, "cita": ci} for t, s, ci in filas]

def buscar(pregunta, limite=10):
    return [f["seccion"] for f in buscar_fragmentos(pregunta, limite)]


from golden import CON_RESPUESTA


def puesto(secciones, esperadas):
    for i, s in enumerate(secciones, start=1):
        if s in esperadas:
            return i
    return None


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    puestos = []
    for p in CON_RESPUESTA:
        r = puesto(buscar(p["pregunta"]), p["secciones"])
        puestos.append(r)
        print(f"| {p['n']} | {'/'.join(p['secciones'])} | {r or '—'} |")

    encontradas = [x for x in puestos if x]
    print(f"\nRecall@10  {len(encontradas)}/{len(CON_RESPUESTA)}")
    print(f"MRR@10     {sum(1/x for x in encontradas)/len(CON_RESPUESTA):.3f}")
    print(f"En puesto 1: {sum(1 for x in encontradas if x == 1)}/{len(CON_RESPUESTA)}")
