"""Cuatro pruebas de la API. Ninguna llama a OpenAI, asi que la suite cuesta cero.

Son de integracion, no unitarias: necesitan el tunel SSH abierto, porque
prueban que las piezas hablan entre si. /v1/preguntar no se prueba aqui a
proposito — cada corrida gastaria dinero.

    .venv/Scripts/pytest -q
"""

from fastapi.testclient import TestClient

from api import app

cliente = TestClient(app)


def test_health_reporta_las_dos_dependencias():
    r = cliente.get("/health")
    assert r.status_code == 200, r.text
    assert r.json() == {"postgres": "ok", "ollama": "ok"}


def test_pregunta_vacia_es_rechazada():
    # Solo espacios: StringConstraints los quita antes de medir la longitud.
    assert cliente.post("/v1/buscar", json={"pregunta": "   "}).status_code == 422


def test_limite_fuera_de_rango_es_rechazado():
    assert cliente.post("/v1/buscar", json={"pregunta": "x", "limite": 500}).status_code == 422
    assert cliente.post("/v1/buscar", json={"pregunta": "x", "limite": 0}).status_code == 422


def test_buscar_devuelve_fragmentos_con_su_cita():
    r = cliente.post("/v1/buscar", json={"pregunta": "plazo para notificar una brecha", "limite": 5})
    assert r.status_code == 200, r.text
    fragmentos = r.json()
    assert len(fragmentos) == 5
    for f in fragmentos:
        assert f["texto"] and f["seccion"] and f["cita"]
