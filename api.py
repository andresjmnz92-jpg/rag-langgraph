"""La API sobre el RAG. Dos rutas y un chequeo de salud.

Estan separadas a proposito: /v1/buscar es determinista, instantaneo y gratis;
/v1/preguntar es no determinista, lento y cuesta dinero. Medir las dos mitades
por separado fue lo que encontro el fallo del 9 de agosto, y esta es esa
leccion puesta en la arquitectura.
"""

from typing import Annotated

import psycopg
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, StringConstraints

from agente import agente
from recuperar import TABLA, buscar_fragmentos, conectar, vectorizar

Pregunta = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class ConsultaBusqueda(BaseModel):
    pregunta: Pregunta
    limite: int = Field(20, ge=1, le=100)


class ConsultaPregunta(BaseModel):
    pregunta: Pregunta


class Fragmento(BaseModel):
    texto: str
    seccion: str | None
    cita: str | None


class Respuesta(BaseModel):
    respuesta: str
    fragmentos: list[Fragmento]
    vueltas: int
    uso: dict


app = FastAPI(
    title="RAG sobre HIPAA",
    version="1.0.0",
    description=f"Recuperacion y respuesta sobre 45 CFR 160/162/164. Tabla: {TABLA}.",
)


def traducir_fallo(e: Exception) -> HTTPException:
    """Un 503 que dice QUE se cayo. 'Error' a secas cuesta media hora de buscar."""
    if isinstance(e, requests.RequestException):
        return HTTPException(503, "Ollama no responde: no se pudo vectorizar la pregunta")
    if isinstance(e, psycopg.OperationalError):
        return HTTPException(503, "Postgres no responde: revisa el tunel SSH")
    if isinstance(e, RuntimeError):
        return HTTPException(503, str(e))
    raise e


@app.get("/health")
def health():
    """Comprueba el efecto, no el codigo de salida: consulta de verdad las dos piezas."""
    estado = {}
    try:
        with conectar() as c:
            c.execute("SELECT 1")
        estado["postgres"] = "ok"
    except Exception as e:
        estado["postgres"] = type(e).__name__
    try:
        vectorizar("ping")
        estado["ollama"] = "ok"
    except Exception as e:
        estado["ollama"] = type(e).__name__

    if any(v != "ok" for v in estado.values()):
        raise HTTPException(503, estado)
    return estado


@app.post("/v1/buscar", response_model=list[Fragmento])
def buscar(consulta: ConsultaBusqueda):
    try:
        return buscar_fragmentos(consulta.pregunta, consulta.limite)
    except Exception as e:
        raise traducir_fallo(e)


@app.post("/v1/preguntar", response_model=Respuesta)
def preguntar(consulta: ConsultaPregunta):
    try:
        return agente.invoke({"pregunta": consulta.pregunta})
    except Exception as e:
        raise traducir_fallo(e)
