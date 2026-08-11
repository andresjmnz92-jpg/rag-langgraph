import os, json, requests, psycopg
from dotenv import load_dotenv

load_dotenv()

TABLA = "documentos_v3"

def conectar():
    return psycopg.connect(
        host="127.0.0.1", port=5433,
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

def vectorizar(texto):
    r = requests.post("http://127.0.0.1:11435/api/embed",
                      json={"model": "bge-m3:latest", "input": texto}, timeout=120)
    r.raise_for_status()
    vectores = r.json().get("embeddings") or []
    if not vectores:
        raise RuntimeError(f"Ollama devolvio vacio para: {texto!r}")
    return vectores[0]

def buscar(pregunta, limite=10):
    vec = vectorizar(pregunta)
    with conectar() as c:
        filas = c.execute(
            f"SELECT metadata->>'seccion' FROM {TABLA} "
            "ORDER BY embedding <=> %s::vector LIMIT %s",
            (json.dumps(vec), limite),
        ).fetchall()
    return [f[0] for f in filas]

PREGUNTAS = [
    (1, "¿Qué plazo tiene una entidad para notificar a los individuos afectados por una brecha?", ["164.404"]),
    (2, "¿A partir de cuántos individuos afectados hay que notificar a los medios de comunicación?", ["164.406"]),
    (3, "¿Cuándo debe notificarse una brecha al Secretary?", ["164.408"]),
    (4, "¿Qué plazo tiene un business associate para notificar una brecha a la entidad cubierta?", ["164.410"]),
    (5, "¿Cuántos años deben conservarse las políticas y procedimientos de seguridad?", ["164.316"]),
    (6, "¿Cuál es la definición de business associate?", ["160.103"]),
    (7, "¿Cuál es la definición de breach?", ["164.402"]),
    (8, "¿Cuáles son las tres categorías de salvaguardas de la Security Rule?", ["164.308", "164.310", "164.312"]),
    (9, "¿Qué plazo hay para darle a un individuo acceso a su información de salud?", ["164.524"]),
    (10, "¿Qué plazo hay para responder a una solicitud de enmienda?", ["164.526"]),
    (11, "¿Qué período cubre el accounting of disclosures?", ["164.528"]),
    (12, "¿Cuáles son los montos de las multas civiles por violación?", ["160.404"]),
    (13, "¿Qué factores se consideran para determinar el monto de una multa?", ["160.408"]),
    (14, "¿Qué elementos debe contener la notificación de brecha a los individuos?", ["164.404"]),
    (15, "¿Qué debe incluir el Notice of Privacy Practices?", ["164.520"]),
    (16, "¿En qué casos NO aplica el estándar de minimum necessary?", ["164.502"]),
]

def puesto(secciones, esperadas):
    for i, s in enumerate(secciones, start=1):
        if s in esperadas:
            return i
    return None

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    puestos = []
    for numero, pregunta, esperadas in PREGUNTAS:
        p = puesto(buscar(pregunta), esperadas)
        puestos.append(p)
        print(f"| {numero} | {'/'.join(esperadas)} | {p or '—'} |")

    encontradas = [p for p in puestos if p]
    print(f"\nRecall@10  {len(encontradas)}/{len(PREGUNTAS)}")
    print(f"MRR@10     {sum(1/p for p in encontradas)/len(PREGUNTAS):.3f}")
    print(f"En puesto 1: {sum(1 for p in encontradas if p == 1)}/{len(PREGUNTAS)}")

