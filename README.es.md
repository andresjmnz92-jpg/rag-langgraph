*[English](README.md) · **Español***

# RAG en Python — el mismo sistema, reconstruido en código

Reconstrucción de [mi RAG en n8n](https://github.com/andresjmnz92-jpg/rag-privado) como Python: el
agente en LangGraph, expuesto por FastAPI y por MCP, con la comparación medida entre API y modelo
local.

**El primer trabajo no era mejorarlo. Era hacerlo idéntico.** Mientras el recuperador en Python no
devuelva los mismos números que el de n8n, cualquier comparación posterior entre los dos estaría
midiendo el port en vez del agente.

**Stack:** PostgreSQL 17 + pgvector · Ollama con BGE-M3 · psycopg · `gpt-5-mini`

---

## Semana 1: el recuperador, portado y verificado

Las mismas 16 preguntas, el mismo corpus de 581 fragmentos, el mismo modelo de embeddings, la
misma tabla que consulta el chat de n8n en vivo. Los números de referencia se midieron el 10 de
agosto; los de Python el 11.

| | Referencia | **Python** |
| --- | --- | --- |
| Recall@10 | 16/16 | **16/16** |
| MRR@10 | 0,938 | **0,938** |
| En puesto 1 | 14/16 | **14/16** |

Idénticos hasta el tercer decimal. El port no es una reescritura que casualmente funciona:
recupera los mismos fragmentos en el mismo orden.

**Vale la pena ser preciso sobre qué se compara aquí.** Los dos números salen de consultar la
misma tabla directamente; ninguno pasa por una ejecución de n8n, porque la calidad de la
recuperación es una propiedad del corpus y del modelo de embeddings, no de la herramienta que los
llama. La comparación n8n contra LangGraph es sobre el **agente**, y esa cae en la semana 2.

**Para qué sirve:** cuando esa comparación llegue, el recuperador ya no será una variable.

### Toda la búsqueda es una línea de SQL

```sql
SELECT metadata->>'seccion' FROM documentos_v3
ORDER BY embedding <=> %s::vector LIMIT 10
```

`<=>` es el operador de distancia coseno de pgvector. No hay base de datos vectorial, ni
framework, ni librería de recuperación: 25 líneas de `psycopg` y `requests` reemplazan los nodos
de n8n.

---

## Cómo se corre

Postgres y Ollama corren en Docker en el servidor y no publican puertos, así que un túnel SSH
llega a ellos sin abrir nada hacia internet:

```bash
ssh -i <llave> -N -L 5433:<ip-contenedor-postgres>:5432 -L 11435:<ip-contenedor-ollama>:11434 <usuario>@<host>
```

Después, con `POSTGRES_USER`, `POSTGRES_PASSWORD` y `POSTGRES_DB` en un `.env` local:

```bash
python -m venv .venv && .venv/Scripts/activate
pip install "psycopg[binary]" requests python-dotenv
python recuperar.py
```

Esas IP de contenedor las asigna Docker y cambian cuando los contenedores se reinician.
`docker inspect` da las vigentes.

---

## Qué sigue

1. **El agente en LangGraph**, y las 20 preguntas corridas contra él — una tabla de n8n contra
   LangGraph con las mismas preguntas y la misma métrica.
2. **FastAPI y MCP sobre la misma función.** Dos fachadas, un solo motor.
3. **Desplegar con Docker, y medir `gpt-5-mini` contra un modelo local.** Esa comparación es el
   argumento de privacidad con un número en vez de una promesa.

**Deuda conocida, arrastrada:** el 16/20 de respuestas que está publicado se midió sobre el corpus
anterior. Se vuelve a medir una sola vez, en la semana 2, para que esa corrida sirva a las dos
tablas.
