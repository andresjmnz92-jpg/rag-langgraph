# documentos_v4 — 20 preguntas · topK 5 · max 1 vuelta(s) · qwen3:4b · 2026-08-13

- Controles superados (automático): **4/4**
- Citó la sección esperada (automático): **14/16**
- Segundos por consulta: **89.2** de media
- Fichas: 50,529 entrada + 84,750 salida — **$0.000** las 20

Calificado el 13 ago 2026: primer pase de Claude, criterio estricto elegido por Andres (si falta un elemento de una lista o un matiz que cambia el sentido legal, es fallo). NO es evaluacion independiente: la califica el mismo sistema que ayudo a construirla.

## 1. ¿Qué plazo tiene una entidad para notificar a los individuos afectados por una brecha?

**Esperada** (§ 164.404)

> Sin demora irrazonable, máximo 60 días calendario desde el descubrimiento.

**Obtenida** — 34.6s, 2269+1650 fichas

> 60 días calendario (§ 164.404(b))

Cita/negativa: ✅ · **Contenido: [x]**

---

## 2. ¿A partir de cuántos individuos afectados hay que notificar a los medios de comunicación?

**Esperada** (§ 164.406)

> Más de 500 residentes de un estado o jurisdicción.

**Obtenida** — 48.1s, 1993+2094 fichas

> Más de 500 individuos [Seccion 164.406 - 45 CFR 164.406]

Cita/negativa: ✅ · **Contenido: [ ] FALLO**

---

## 3. ¿Cuándo debe notificarse una brecha al Secretary?

**Esperada** (§ 164.408)

> Depende del tamaño. 500 personas o más: al mismo tiempo que la notificación a los individuos. Menos de 500: en un reporte anual, máximo 60 días después de cerrar el año calendario. § 164.408(b) y (c)

**Obtenida** — 92.9s, 2320+4740 fichas

> Para brechas de 500 o más individuos: contemporáneamente con la notificación requerida en § 164.404(a) (Sección 164.408b). Para brechas menores a 500 individuos: no más de 60 días después del final de cada año calendario (Sección 164.408c).

Cita/negativa: ✅ · **Contenido: [x]**

---

## 4. ¿Qué plazo tiene un business associate para notificar una brecha a la entidad cubierta?

**Esperada** (§ 164.410)

> No más de 60 días después de descubrir la brecha.

**Obtenida** — 33.7s, 2477+1103 fichas

> 60 días calendario. [Seccion 164.410 - 45 CFR 164.410]

Cita/negativa: ✅ · **Contenido: [x]**

---

## 5. ¿Cuántos años deben conservarse las políticas y procedimientos de seguridad?

**Esperada** (§ 164.316)

> 6 años desde su creación o desde la última fecha en que estuvo vigente, la que sea posterior. § 164.316(b)(2)(i)

**Obtenida** — 36.9s, 2373+1368 fichas

> 6 años. [Seccion 164.316 - 45 CFR 164.316]

Cita/negativa: ✅ · **Contenido: [x]**

---

## 6. ¿Cuál es la definición de business associate?

**Esperada** (§ 160.103)

> Persona o entidad que, por cuenta de una entidad cubierta y sin ser parte de su personal, crea, recibe, mantiene o transmite PHI para una función regulada por la norma (procesamiento de reclamaciones, análisis de datos, revisión de utilización, aseguramiento de calidad). § 160.103

**Obtenida** — 157.0s, 2247+7969 fichas

> Un negocio asociado es una persona que ofrece un registro de salud personal a uno o más individuos por cuenta de una entidad cubierta, o un subcontratista que crea, recibe, mantiene o transmite información protegida de salud por cuenta del negocio asociado. (Sección 160.103 - 45 CFR 160.103)

Cita/negativa: ✅ · **Contenido: [ ] FALLO**

---

## 7. ¿Cuál es la definición de breach?

**Esperada** (§ 164.402)

> Adquirir, acceder, usar o divulgar PHI de forma no permitida por la Subparte E, comprometiendo su seguridad o privacidad.
> EXCLUYE: (i) acceso no intencional de buena fe por personal autorizado, sin uso posterior indebido; (ii) divulgación inadvertida entre personas autorizadas de la misma entidad; (iii) casos donde de buena fe se cree que el receptor no pudo retener la información.
> Todo lo demás se presume brecha salvo que se demuestre baja probabilidad de compromiso, con evaluación de riesgo sobre 4 factores: naturaleza y alcance del PHI (y probabilidad de reidentificación), quién lo recibió, si fue realmente adquirido o visto, y cuánto se mitigó el riesgo. § 164.402

**Obtenida** — 129.0s, 2378+6428 fichas

> Breach se define como: "the acquisition, access, use, or disclosure of protected health information in a manner not permitted under subpart E of this part which compromises the security or privacy of the protected health information" (Sección 164.402).

Cita/negativa: ✅ · **Contenido: [x]**

---

## 8. ¿Cuáles son las tres categorías de salvaguardas de la Security Rule?

**Esperada** (§ 164.308/164.310/164.312)

> Tres: administrativas (§ 164.308), físicas (§ 164.310) y técnicas (§ 164.312).

**Obtenida** — 45.8s, 2269+1879 fichas

> Administrativas, Técnicas y Físicas.  
> Citas:  
> - [Seccion 164.308] (Administrative safeguards)  
> - [Seccion 164.310] (Physical safeguards)  
> - [Seccion 164.312] (Technical safeguards)

Cita/negativa: ✅ · **Contenido: [x]**

---

## 9. ¿Qué plazo hay para darle a un individuo acceso a su información de salud?

**Esperada** (§ 164.524)

> 30 días desde que recibe la solicitud. Extensible UNA sola vez por 30 días más, avisando por escrito dentro del plazo original el motivo y la fecha en que responderá. § 164.524(b)(2)

**Obtenida** — 94.4s, 2507+4593 fichas

> 30 días (Sección 164.524)

Cita/negativa: ✅ · **Contenido: [ ] FALLO**

---

## 10. ¿Qué plazo hay para responder a una solicitud de enmienda?

**Esperada** (§ 164.526)

> 60 días desde que recibe la solicitud. Extensible UNA sola vez por 30 días más, avisando por escrito el motivo y la fecha. § 164.526(b)(2)

**Obtenida** — 60.1s, 2403+2716 fichas

> 60 días (45 CFR § 164.526)

Cita/negativa: ✅ · **Contenido: [ ] FALLO**

---

## 11. ¿Qué período cubre el accounting of disclosures?

**Esperada** (§ 164.528)

> 6 años anteriores a la fecha de la solicitud. El individuo puede pedir un período menor. § 164.528(a)(1) y (a)(3)

**Obtenida** — 80.8s, 2614+3866 fichas

> Los seis años anteriores a la fecha de solicitud o un período más corto a solicitud del individuo según el inciso (a)(3) de esta sección. (Fragmento 1)

Cita/negativa: ❌ · **Contenido: [x]**

---

## 12. ¿Cuáles son los montos de las multas civiles por violación?

**Esperada** (§ 160.404)

> Cuatro niveles según culpabilidad (violaciones desde 18-feb-2009), todos con tope de $1,500,000/año por violaciones idénticas:
> · No sabía ni podía saber con diligencia razonable: $100–$50,000 por violación
> · Causa razonable, sin negligencia deliberada: $1,000–$50,000
> · Negligencia deliberada CORREGIDA en 30 días: $10,000–$50,000
> · Negligencia deliberada NO corregida: mínimo $50,000, sin máximo por violación
> (Antes del 18-feb-2009: $100 por violación, tope $25,000/año.) § 160.404(b)

**Obtenida** — 177.9s, 2808+8411 fichas

> Menos de $1,000 o más de $50,000 por violación, menos de $50,000 por violación, menos de $10,000 o más de $50,000 por violación, más de $1,500,000 para violaciones idénticas anuales y más de $25,000 para violaciones idénticas anuales (antes de febrero de 2009).

Cita/negativa: ❌ · **Contenido: [ ] FALLO**

---

## 13. ¿Qué factores se consideran para determinar el monto de una multa?

**Esperada** (§ 160.408)

> Cinco, y cada uno puede ser atenuante o agravante:
> (a) Naturaleza y alcance de la violación (nº de individuos afectados, duración)
> (b) Naturaleza y alcance del daño (físico, financiero, reputacional, o si impidió obtener atención médica)
> (c) Historial de cumplimiento previo (reincidencia, correcciones, respuesta a asistencia técnica y a quejas)
> (d) Condición financiera de la entidad (dificultades, si la multa pondría en riesgo su capacidad de dar atención, tamaño)
> (e) Otros asuntos que la justicia requiera. § 160.408

**Obtenida** — 120.0s, 2524+5841 fichas

> Los factores son: naturaleza y extensión del incumplimiento; naturaleza y extensión de los daños; historial de cumplimiento previo; condición financiera del ente cubierto y otros aspectos que justifiquen. [Seccion 160.408 - 45 CFR 160.408]

Cita/negativa: ✅ · **Contenido: [x]**

---

## 14. ¿Qué elementos debe contener la notificación de brecha a los individuos?

**Esperada** (§ 164.404)

> Cinco elementos, en lenguaje sencillo:
> (A) Descripción breve de qué pasó, con fecha de la brecha y fecha del descubrimiento
> (B) Tipos de PHI involucrados (nombre, SSN, fecha de nacimiento, dirección, nº de cuenta, diagnóstico, etc.)
> (C) Pasos que el individuo debe tomar para protegerse
> (D) Qué está haciendo la entidad para investigar, mitigar y evitar que se repita
> (E) Datos de contacto: teléfono gratuito, correo, sitio web o dirección postal
> § 164.404(c)

**Obtenida** — 101.0s, 2267+4972 fichas

> Los elementos son: (A) Una descripción breve de lo ocurrido, incluyendo la fecha de la brecha y la fecha de descubrimiento si es conocida; (B) Descripción de los tipos de información protegida no segura involucrados; (C) Pasos que los individuos deben tomar para protegerse; (D) Breve descripción de las acciones del ente cubierto para investigar, mitigar daños y prevenir futuras brechas. [Sección 164.404(c)(1)]

Cita/negativa: ✅ · **Contenido: [ ] FALLO**

---

## 15. ¿Qué debe incluir el Notice of Privacy Practices?

**Esperada** (§ 164.520)

> Ocho elementos, en lenguaje sencillo:
> (i) Encabezado con el texto LITERAL: "THIS NOTICE DESCRIBES HOW MEDICAL INFORMATION ABOUT YOU MAY BE USED AND DISCLOSED AND HOW YOU CAN GET ACCESS TO THIS INFORMATION. PLEASE REVIEW IT CAREFULLY."
> (ii) Usos y divulgaciones, con al menos un ejemplo para tratamiento, pago y operaciones
> (iii) Declaraciones separadas si hay recaudación de fondos, plan de grupo o underwriting
> (iv) Derechos del individuo (restricciones, comunicaciones confidenciales, acceso, enmienda, accounting, copia en papel)
> (v) Deberes de la entidad, incluida la de notificar brechas
> (vi) Derecho a quejarse ante la entidad y ante el Secretary, sin represalias
> (vii) Nombre o cargo y teléfono de contacto
> (viii) Fecha de entrada en vigor
> § 164.520(b)(1)

**Obtenida** — 93.7s, 2561+4588 fichas

> El Notice of Privacy Practices debe incluir: encabezado específico, descripción de usos y revelaciones (con ejemplo), declaración de cumplimiento con notificación vigente, declaración de derecho a cambiar la notificación y proporcionarla revisada, información de contacto, fecha de efectividad y sección de quejas (45 CFR § 164.520).

Cita/negativa: ✅ · **Contenido: [ ] FALLO**

---

## 16. ¿En qué casos NO aplica el estándar de minimum necessary?

**Esperada** (§ 164.502)

> Seis casos:
> (i) Divulgaciones a un proveedor de salud, o solicitudes de este, para TRATAMIENTO
> (ii) Usos o divulgaciones hechas al propio individuo
> (iii) Usos o divulgaciones hechas con autorización del individuo (§ 164.508)
> (iv) Divulgaciones al Secretary para investigar cumplimiento
> (v) Usos o divulgaciones requeridos por ley (§ 164.512(a))
> (vi) Usos o divulgaciones requeridos para cumplir con este subcapítulo
> § 164.502(b)(2)

**Obtenida** — 110.9s, 2299+5531 fichas

> (i) Divulgaciones o solicitudes por parte de proveedores de salud para tratamiento; (ii) Uso o divulgación al individuo; (iii) Uso o divulgación bajo autorización § 164.508; (iv) Divulgaciones al Secretario conforme con subparte C del parte 160; (v) Uso o divulgación requerido por ley § 164.512(a); (vi) Uso o divulgación requerido para cumplir requisitos de esta subsección. [Seccion 164.502 - 45 CFR 164.502]

Cita/negativa: ✅ · **Contenido: [x]**

---

## 17. ¿Cuál es la multa máxima bajo el GDPR?

**Esperada** (§ ninguna, es control)

> No encontré eso en los documentos cargados.

**Obtenida** — 90.6s, 2744+4300 fichas

> No encontre eso en los documentos cargados.

Cita/negativa: ✅ · **Contenido: [ ]**

---

## 18. ¿Qué dice esta norma sobre el uso de inteligencia artificial o modelos de lenguaje?

**Esperada** (§ ninguna, es control)

> No encontré eso en los documentos cargados.

**Obtenida** — 122.5s, 4232+5390 fichas

> No encontre eso en los documentos cargados.

Cita/negativa: ✅ · **Contenido: [ ]**

---

## 19. ¿Cuánto cuesta obtener la certificación oficial HIPAA?

**Esperada** (§ ninguna, es control)

> No encontré eso en los documentos cargados.

**Obtenida** — 63.7s, 2834+2844 fichas

> No encontre eso en los documentos cargados.

Cita/negativa: ✅ · **Contenido: [ ]**

---

## 20. ¿Qué obligaciones aplican a un laboratorio clínico en Colombia?

**Esperada** (§ ninguna, es control)

> No encontré eso en los documentos cargados.

**Obtenida** — 91.0s, 2410+4467 fichas

> No encontre eso en los documentos cargados.

Cita/negativa: ✅ · **Contenido: [ ]**

---

