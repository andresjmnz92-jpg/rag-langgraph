# Diseño — la API y el servidor MCP

**12 de agosto de 2026.** Semana 3b del plan. Documento en español porque es el idioma de trabajo;
los dos README siguen siendo bilingües.

## El problema

El RAG solo funciona ejecutando Python a mano en un PC con el túnel abierto. Ningún otro programa
puede pedirle nada. Este documento diseña **dos fachadas sobre el mismo motor**, sin tocar el motor.

```
recuperar.py            agente.py             ← el motor, no se toca
  buscar_fragmentos()     agente.invoke()
        ↑         ↖            ↑
     api.py            mcp_server.py          ← las dos fachadas
    (FastAPI)             (stdio)
```

Las dos fachadas **importan las funciones directamente**. El MCP no llama a la API por HTTP: son
consumidores hermanos del mismo módulo, no una cadena. Si el motor cambia, cambian los dos a la vez
y no hay una red en medio que pueda fallar.

## `api.py`

| Ruta | Entrada | Salida | Costo |
| --- | --- | --- | --- |
| `GET /health` | — | estado de Postgres y de Ollama por separado | $0 |
| `POST /v1/buscar` | `{pregunta, limite}` | lista de `{texto, seccion, cita}` | $0 |
| `POST /v1/preguntar` | `{pregunta}` | `{respuesta, fragmentos, vueltas, uso}` | ~$0,004 |

**Por qué dos rutas y no una.** La medición del 9 de agosto encontró que una redacción buena esconde
un recuperador malo, y que hay que medir las dos mitades por separado. Separarlas en la API es esa
lección convertida en arquitectura: `/v1/buscar` es determinista, instantáneo y gratis; `/v1/preguntar`
es no determinista, lento y cuesta dinero. Mezclarlas obligaría a pagar un LLM para saber si la
base de datos responde.

**Contrato, en modelos Pydantic** — no diccionarios sueltos:

- `pregunta`: texto, mínimo 1 carácter después de quitar espacios. Vacía → **422**, y lo hace
  Pydantic sin código propio.
- `limite`: entero, por defecto **20** (el mismo topK del chat de n8n y de la evaluación), máximo
  **100**. El tope existe para que nadie pida diez mil fragmentos y tumbe el proceso.
- La respuesta también es un modelo, así que el contrato queda publicado en `/docs` sin escribirlo
  aparte.

**`/health` comprueba el efecto, no el código de salida.** Devolver `{"status": "ok"}` a secas es
justo el fallo que este proyecto ya pisó dos veces: Telegram y el generador de vectores devolvieron
éxito sin hacer nada. Así que `/health` hace una consulta real a Postgres y una llamada real de
embedding a Ollama, y reporta cada una por separado. Si uno falla, la respuesta dice **cuál**.

## `mcp_server.py`

Servidor MCP por **stdio** — corre en la máquina del usuario, no en red. Expone **una sola
herramienta**:

- `buscar_hipaa(pregunta, limite=20)` → los fragmentos.

**No expone `preguntar`, y es una decisión, no un olvido.** Quien consume el MCP es Claude, que ya
redacta. Exponer `preguntar` sería pagar `gpt-5-mini` para escribir algo que el modelo del otro lado
iba a escribir de todos modos, y además metería un redactor peor en medio. La herramienta correcta
que ofrecer a un modelo es la que él no puede hacer solo: **buscar en un corpus privado**.

## Errores

| Situación | Respuesta |
| --- | --- |
| Pregunta vacía o `limite` fuera de rango | **422**, lo genera Pydantic |
| Postgres no responde (túnel caído) | **503**, diciendo que es la base de datos |
| Ollama no responde | **503**, diciendo que es el modelo de embeddings |
| Ollama responde pero devuelve un vector vacío | **503** — `recuperar.py` ya lanza `RuntimeError` en ese caso, y no se convierte en un 200 con basura |

## `test_api.py`

Cuatro tests con el `TestClient` de FastAPI. **Ninguno llama a OpenAI**, así que la suite cuesta cero
dólares y se puede correr las veces que haga falta.

1. `/health` con el túnel vivo → 200 y las dos dependencias en `ok`.
2. `/v1/buscar` con pregunta vacía → 422.
3. `/v1/buscar` con `limite` de 500 → 422.
4. `/v1/buscar` con una pregunta real → 20 fragmentos, y cada uno trae `texto`, `seccion` y `cita`.

`/v1/preguntar` **no se testea automáticamente**: cada corrida gastaría dinero. Se prueba a mano
desde `/docs` y queda escrito que es así.

Los tests necesitan el túnel SSH abierto — son de integración, no unitarios, y el README lo dice.

## Lo que NO entra, y por qué

| Fuera | Motivo |
| --- | --- |
| Autenticación | Nada queda expuesto a internet esta semana. Añadirla ahora sería proteger un puerto local |
| Límites de uso y caché | No hay tráfico que limitar ni consultas repetidas que cachear |
| `/ingest` | El corpus se carga aparte y una sola vez. Un endpoint para eso no tendría quién lo llame |
| Docker | Es la semana 4 del plan, con su propia medición |
| Reemplazar el chat público | El chat de n8n sigue siendo la demo. Esto es el motor detrás, no la vitrina |

## Dependencias nuevas

`fastapi` · `uvicorn` · `pytest` · `httpx` (lo necesita `TestClient`) · `mcp`

## Cuándo está terminado

1. `uvicorn api:app` levanta y `/docs` muestra las tres rutas con su contrato.
2. Los cuatro tests pasan con el túnel abierto.
3. Con el túnel **cerrado**, `/health` devuelve 503 nombrando la dependencia caída — probado en las
   dos direcciones, como el vigilante del servidor.
4. Claude Code, con el MCP configurado, responde una pregunta de HIPAA citando la sección.
5. Los dos README actualizados a la vez.
