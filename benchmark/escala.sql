-- Cuanto aguanta pgvector: latencia, indice y recall a 581, 10.000 y 100.000 vectores.
--
-- Corre en un contenedor APARTE del de produccion, con limite de memoria de Docker,
-- porque en la misma maquina vive un chat publico:
--
--   docker run -d --name bench-pg --memory=3g -e POSTGRES_HOST_AUTH_METHOD=trust \
--     pgvector/pgvector:0.8.6-pg17
--
-- El contenedor murio una vez durante estas pruebas (un count(DISTINCT) sobre 100.000
-- vectores) y produccion no se entero. Ese era el proposito del limite.

CREATE EXTENSION vector;
CREATE TABLE bench (id bigserial PRIMARY KEY, embedding vector(1024));

-- Los 581 vectores reales del corpus entran tal cual, y las 16 preguntas del golden
-- dataset son las consultas. El volumen es sintetico; lo que se busca, no.
--   docker exec produccion psql -c "COPY (SELECT embedding FROM documentos_v4) TO STDOUT" \
--     | docker exec -i bench-pg psql -c "COPY bench (embedding) FROM STDIN"


-- ---------------------------------------------------------------------------
-- El relleno: copias de los vectores reales con ruido encima.
--
-- La amplitud 0.12 no se eligio a ojo. Se midio: deja los clones a 0.34 de su
-- original, que es la distancia que hay entre dos documentos reales distintos
-- (medidas: 0.287 a 0.497). Con 0.06 quedaban a 0.13 y eran casi duplicados.
--
-- EL "WHERE g > 0" NO SOBRA. Sin el, la subconsulta lateral no depende de nada
-- de la fila, Postgres la evalua UNA VEZ y reutiliza el mismo ruido: 100.000
-- filas que son ~1.700 vectores distintos. No da error, no da aviso, y el
-- indice se construye igual. Lo unico que delata el fallo es un recall absurdo.
-- ---------------------------------------------------------------------------
INSERT INTO bench (embedding)
SELECT (b.embedding + r.ruido)::vector
FROM (SELECT embedding FROM bench WHERE id <= 581) b
CROSS JOIN generate_series(1, 160) g
CROSS JOIN LATERAL (
  SELECT array_agg((random() - 0.5) * 0.12)::real[]::vector AS ruido
  FROM generate_series(1, 1024) s WHERE g > 0
) r
LIMIT 90000;

-- Comprobar SIEMPRE que el relleno son vectores distintos, antes de medir nada.
SELECT count(*) AS copias_de_una_fila FROM bench WHERE embedding = (SELECT embedding FROM bench WHERE id = 90000);

VACUUM ANALYZE bench;


-- --- La verdad: top-10 exacto, calculado antes de que exista el indice ---
CREATE TABLE verdad AS
SELECT c.id AS q, array(SELECT b.id FROM bench b ORDER BY b.embedding <=> c.embedding LIMIT 10) AS top
FROM consultas c;

\timing on

-- --- Busqueda exacta: las 16 preguntas ---
SELECT count(*) FROM consultas c, LATERAL (SELECT b.id FROM bench b ORDER BY b.embedding <=> c.embedding LIMIT 10) t;

-- --- El indice ---
SET maintenance_work_mem = '1GB';   -- si el grafo no cabe aqui, pgvector avisa y tarda el doble
CREATE INDEX idx_hnsw ON bench USING hnsw (embedding vector_cosine_ops);
SELECT pg_size_pretty(pg_relation_size('idx_hnsw')) AS indice, pg_size_pretty(pg_total_relation_size('bench')) AS tabla;

-- --- Busqueda con indice ---
SELECT count(*) FROM consultas c, LATERAL (SELECT b.id FROM bench b ORDER BY b.embedding <=> c.embedding LIMIT 10) t;

\timing off

-- --- Cuanto del top-10 exacto recupera el indice ---
SELECT round(avg(cardinality(ARRAY(SELECT unnest(v.top) INTERSECT SELECT unnest(a.top))))/10.0, 3) AS recall_at_10
FROM verdad v
JOIN (SELECT c.id AS q, array(SELECT b.id FROM bench b ORDER BY b.embedding <=> c.embedding LIMIT 10) AS top FROM consultas c) a
USING (q);

-- Despues de borrar filas para bajar de escala: VACUUM FULL, no VACUUM.
-- Con la tabla hinchada el indice tardo 125 ms por consulta; compactada, 1,2 ms.
