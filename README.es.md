*[English](README.md) · **Español***

# RAG en Python — el mismo sistema, reconstruido en código

Reconstrucción de [mi RAG en n8n](https://github.com/andresjmnz92-jpg/rag-privado) como Python: el
agente en LangGraph, expuesto por FastAPI y por MCP, con la comparación medida entre API y modelo
local.

**El primer trabajo no era mejorarlo. Era hacerlo idéntico.** Mientras el recuperador en Python no
puntúe lo que este corpus ya puntúa, cualquier comparación posterior entre los dos agentes estaría
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

## Semana 2: el agente, y una métrica que mentía

El agente son dos nodos y una flecha: `buscar → redactar`. Las cinco reglas del system prompt
están copiadas del workflow de n8n palabra por palabra — cambiarlas convertiría una comparación
de frameworks en una comparación de prompts.

**Una de esas reglas deja de ser una regla aquí.** La número 1 le pide al modelo que SIEMPRE
busque antes de responder. En n8n eso es una petición que el modelo puede ignorar. En un grafo,
`START → buscar → redactar` significa que el redactor no puede ejecutarse sin fragmentos
recuperados. **La misma instrucción pasa de súplica a estructura**, y esa diferencia solo se vio
construyendo las dos.

### Los puntajes

20 preguntas con respuestas verificadas a mano, bajo la regla estricta: una cita equivocada es un
fallo aunque el contenido sea correcto.

| | corpus v3 | **corpus v4** |
| --- | --- | --- |
| Citó la sección correcta | 14/16 | **16/16** |
| Contenido correcto | 14/16 | **15/16** |
| Controles (callarse es lo correcto) | 4/4 | **4/4** |
| **Total** | **17/20** | **19/20** |
| Costo de las 20 | $0,029 | **$0,027** |
| Segundos por consulta | 16,8 | 15,4 |

### El hallazgo: recall@10 reportaba 100% sobre un sistema que entregaba 81%

Tres de los cuatro fallos tenían la misma causa, y la métrica no podía ver ninguno.

`recall@10` pregunta *¿volvió la sección correcta?* — y volvía. Lo que no puede preguntar es si
volvió el **fragmento que contiene la respuesta**. Una sección partida en 17 fragmentos puede
llegar cuatro veces sin la frase que responde.

Medido fragmento por fragmento:

| Pregunta | Puesto real del fragmento que responde |
| --- | --- |
| Plazo de acceso (§ 164.524) | **63** de 581 |
| Factores de la multa (§ 160.408) | **26** — seis puestos fuera de la ventana |
| Business associate (§ 160.103) | **151** |

El sistema se negó a responder la del plazo de acceso. Y era lo correcto: la frase de los 30 días
nunca estuvo delante. **El redactor no era el cuello de botella; la métrica apuntaba a la mitad
equivocada.**

### El experimento rechazado se rechazó con evidencia mala

Una versión anterior del corpus —`v4`, que le pone el encabezado de la sección a cada fragmento—
se había medido y **descartado**: subía el MRR de 0,938 a 0,969, "una pregunta de dieciséis", a
cambio de 4% más de fichas de entrada para siempre.

Esa decisión usó la métrica por sección. Vuelta a medir contra el fragmento que responde:

| Pregunta | v3 | **v4** |
| --- | --- | --- |
| Plazo de acceso | 63 | **2** |
| Factores de la multa | 26 | **2** |
| Business associate | 151 | 95 — sigue fuera |

Funciona por un motivo concreto. El fragmento con el plazo de acceso empieza en *"(2) Timely
action by the covered entity"* — no dice "acceso" ni "información de salud" en ninguna parte. Con
`§ 164.524 Access of individuals to protected health information` pegado delante, el vector sabe
de qué trata.

**Las dos preguntas que saltaron al puesto 2 son exactamente las dos que se arreglaron.** Y el
argumento del 4% corría al revés: v4 costó **menos** en total, porque una respuesta precisa es
una respuesta más corta.

El rechazo fue una decisión sólida tomada sobre una medición que no podía ver el defecto. Esa es
la lección más útil de todo esto: **un experimento vale lo que valga la métrica que lo juzgó.**

### Quién calificó qué

Los controles se califican solos: su respuesta correcta es una frase exacta. Los 16 juicios de
contenido salieron de leer cada respuesta contra la verificada a mano; Claude hizo el primer pase
y señaló los casos ambiguos, y esos los decidí yo. Tres eran genuinamente discutibles, y en uno
fallé en contra de su lectura. **Eso no es evaluación independiente y el repo no debe fingir que
lo es** — es un camino más rápido a la misma lectura, con los desacuerdos anotados.

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

1. **Una métrica de recuperación que mida el fragmento, no la sección.** La actual reportaba 16/16
   mientras tres respuestas no estaban en lo que llegó al modelo. Todo lo demás depende de
   arreglar eso.
2. **El fallo que queda, § 160.103.** Su fragmento con la respuesta está en el puesto 95 incluso
   con v4, y empieza en *"(i) On behalf of such covered entity"* — las palabras "business
   associate" no aparecen por ningún lado. La recuperación sola puede no alcanzarlo; devolver la
   sección entera cuando un fragmento suyo entra al top es el candidato obvio, y cuesta 4,6 veces
   más fichas, así que se mide antes de adoptarlo.
3. **FastAPI y MCP sobre la misma función.** Dos fachadas, un solo motor.
4. **Desplegar con Docker, y medir `gpt-5-mini` contra un modelo local.** Esa comparación es el
   argumento de privacidad con un número en vez de una promesa.

**Sigue abierto, y se dice en vez de esconderse:** estos números son una corrida de cada uno. El
modelo no es determinista, y dos preguntas de dieciséis no sobrevivirían a una prueba pareada. Lo
que sostiene el argumento es el mecanismo — los puestos se midieron ANTES de volver a correr
ninguna pregunta, y las dos que mejoraron son exactamente las dos que los puestos predijeron.

**Todavía sin comparar:** n8n contra LangGraph en calidad de respuesta. El puntaje publicado de
n8n se midió sobre el corpus v2, y meterlo en la misma tabla que un número de v3/v4 repetiría el
error que esta semana se gastó en encontrar.
