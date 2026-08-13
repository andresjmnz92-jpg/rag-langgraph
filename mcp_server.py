"""El RAG de HIPAA, servido como herramienta para Claude.

Segunda fachada sobre el mismo motor. No llama a la API por HTTP: importa
buscar_fragmentos directamente, igual que api.py. Dos consumidores hermanos,
sin una red en medio que pueda fallar.
"""

from mcp.server import MCPServer

from recuperar import TABLA, buscar_fragmentos

mcp = MCPServer(
    name="rag-hipaa",
    description=f"Busqueda semantica sobre HIPAA, 45 CFR 160/162/164. Tabla: {TABLA}.",
)


@mcp.tool()
def buscar_hipaa(pregunta: str, limite: int = 20) -> list[dict]:
    """Busca en la normativa HIPAA los fragmentos que responden a una pregunta.

    Los documentos estan en ingles y la pregunta puede venir en espanol: el
    modelo de embeddings es multilingue, asi que NO hay que traducir la
    pregunta antes de llamar.

    Cada fragmento vuelve con su seccion y su cita oficial, para poder
    comprobarlo contra el eCFR.
    """
    return buscar_fragmentos(pregunta, limite)


if __name__ == "__main__":
    mcp.run()
