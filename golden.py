"""The golden dataset: 20 questions with answers verified by hand against 45 CFR.

Copied from rag-privado/evaluacion/preguntas.md, where it lived inside a results
table. A dataset that only a human can read is a dataset no script can score, and
this one gets re-measured every time the pipeline changes.

The four control questions carry an empty `secciones` list. That is not missing
data: there is no correct section because the correct behaviour is to refuse. It
is also what makes them machine-checkable, since the expected answer is one exact
sentence rather than prose.
"""

NEGATIVA = "No encontré eso en los documentos cargados."

PREGUNTAS = [
    {
        "n": 1,
        "pregunta": "¿Qué plazo tiene una entidad para notificar a los individuos afectados por una brecha?",
        "secciones": ["164.404"],
        "esperada": "Sin demora irrazonable, máximo 60 días calendario desde el descubrimiento.",
    },
    {
        "n": 2,
        "pregunta": "¿A partir de cuántos individuos afectados hay que notificar a los medios de comunicación?",
        "secciones": ["164.406"],
        "esperada": "Más de 500 residentes de un estado o jurisdicción.",
    },
    {
        "n": 3,
        "pregunta": "¿Cuándo debe notificarse una brecha al Secretary?",
        "secciones": ["164.408"],
        "esperada": (
            "Depende del tamaño. 500 personas o más: al mismo tiempo que la notificación a los "
            "individuos. Menos de 500: en un reporte anual, máximo 60 días después de cerrar el "
            "año calendario. § 164.408(b) y (c)"
        ),
    },
    {
        "n": 4,
        "pregunta": "¿Qué plazo tiene un business associate para notificar una brecha a la entidad cubierta?",
        "secciones": ["164.410"],
        "esperada": "No más de 60 días después de descubrir la brecha.",
    },
    {
        "n": 5,
        "pregunta": "¿Cuántos años deben conservarse las políticas y procedimientos de seguridad?",
        "secciones": ["164.316"],
        "esperada": (
            "6 años desde su creación o desde la última fecha en que estuvo vigente, la que sea "
            "posterior. § 164.316(b)(2)(i)"
        ),
    },
    {
        "n": 6,
        "pregunta": "¿Cuál es la definición de business associate?",
        "secciones": ["160.103"],
        "esperada": (
            "Persona o entidad que, por cuenta de una entidad cubierta y sin ser parte de su "
            "personal, crea, recibe, mantiene o transmite PHI para una función regulada por la "
            "norma (procesamiento de reclamaciones, análisis de datos, revisión de utilización, "
            "aseguramiento de calidad). § 160.103"
        ),
    },
    {
        "n": 7,
        "pregunta": "¿Cuál es la definición de breach?",
        "secciones": ["164.402"],
        "esperada": (
            "Adquirir, acceder, usar o divulgar PHI de forma no permitida por la Subparte E, "
            "comprometiendo su seguridad o privacidad.\n"
            "EXCLUYE: (i) acceso no intencional de buena fe por personal autorizado, sin uso "
            "posterior indebido; (ii) divulgación inadvertida entre personas autorizadas de la "
            "misma entidad; (iii) casos donde de buena fe se cree que el receptor no pudo retener "
            "la información.\n"
            "Todo lo demás se presume brecha salvo que se demuestre baja probabilidad de "
            "compromiso, con evaluación de riesgo sobre 4 factores: naturaleza y alcance del PHI "
            "(y probabilidad de reidentificación), quién lo recibió, si fue realmente adquirido o "
            "visto, y cuánto se mitigó el riesgo. § 164.402"
        ),
    },
    {
        "n": 8,
        "pregunta": "¿Cuáles son las tres categorías de salvaguardas de la Security Rule?",
        "secciones": ["164.308", "164.310", "164.312"],
        "esperada": (
            "Tres: administrativas (§ 164.308), físicas (§ 164.310) y técnicas (§ 164.312)."
        ),
    },
    {
        "n": 9,
        "pregunta": "¿Qué plazo hay para darle a un individuo acceso a su información de salud?",
        "secciones": ["164.524"],
        "esperada": (
            "30 días desde que recibe la solicitud. Extensible UNA sola vez por 30 días más, "
            "avisando por escrito dentro del plazo original el motivo y la fecha en que "
            "responderá. § 164.524(b)(2)"
        ),
    },
    {
        "n": 10,
        "pregunta": "¿Qué plazo hay para responder a una solicitud de enmienda?",
        "secciones": ["164.526"],
        "esperada": (
            "60 días desde que recibe la solicitud. Extensible UNA sola vez por 30 días más, "
            "avisando por escrito el motivo y la fecha. § 164.526(b)(2)"
        ),
    },
    {
        "n": 11,
        "pregunta": "¿Qué período cubre el accounting of disclosures?",
        "secciones": ["164.528"],
        "esperada": (
            "6 años anteriores a la fecha de la solicitud. El individuo puede pedir un período "
            "menor. § 164.528(a)(1) y (a)(3)"
        ),
    },
    {
        "n": 12,
        "pregunta": "¿Cuáles son los montos de las multas civiles por violación?",
        "secciones": ["160.404"],
        "esperada": (
            "Cuatro niveles según culpabilidad (violaciones desde 18-feb-2009), todos con tope de "
            "$1,500,000/año por violaciones idénticas:\n"
            "· No sabía ni podía saber con diligencia razonable: $100–$50,000 por violación\n"
            "· Causa razonable, sin negligencia deliberada: $1,000–$50,000\n"
            "· Negligencia deliberada CORREGIDA en 30 días: $10,000–$50,000\n"
            "· Negligencia deliberada NO corregida: mínimo $50,000, sin máximo por violación\n"
            "(Antes del 18-feb-2009: $100 por violación, tope $25,000/año.) § 160.404(b)"
        ),
    },
    {
        "n": 13,
        "pregunta": "¿Qué factores se consideran para determinar el monto de una multa?",
        "secciones": ["160.408"],
        "esperada": (
            "Cinco, y cada uno puede ser atenuante o agravante:\n"
            "(a) Naturaleza y alcance de la violación (nº de individuos afectados, duración)\n"
            "(b) Naturaleza y alcance del daño (físico, financiero, reputacional, o si impidió "
            "obtener atención médica)\n"
            "(c) Historial de cumplimiento previo (reincidencia, correcciones, respuesta a "
            "asistencia técnica y a quejas)\n"
            "(d) Condición financiera de la entidad (dificultades, si la multa pondría en riesgo "
            "su capacidad de dar atención, tamaño)\n"
            "(e) Otros asuntos que la justicia requiera. § 160.408"
        ),
    },
    {
        "n": 14,
        "pregunta": "¿Qué elementos debe contener la notificación de brecha a los individuos?",
        "secciones": ["164.404"],
        "esperada": (
            "Cinco elementos, en lenguaje sencillo:\n"
            "(A) Descripción breve de qué pasó, con fecha de la brecha y fecha del descubrimiento\n"
            "(B) Tipos de PHI involucrados (nombre, SSN, fecha de nacimiento, dirección, nº de "
            "cuenta, diagnóstico, etc.)\n"
            "(C) Pasos que el individuo debe tomar para protegerse\n"
            "(D) Qué está haciendo la entidad para investigar, mitigar y evitar que se repita\n"
            "(E) Datos de contacto: teléfono gratuito, correo, sitio web o dirección postal\n"
            "§ 164.404(c)"
        ),
    },
    {
        "n": 15,
        "pregunta": "¿Qué debe incluir el Notice of Privacy Practices?",
        "secciones": ["164.520"],
        "esperada": (
            "Ocho elementos, en lenguaje sencillo:\n"
            "(i) Encabezado con el texto LITERAL: \"THIS NOTICE DESCRIBES HOW MEDICAL INFORMATION "
            "ABOUT YOU MAY BE USED AND DISCLOSED AND HOW YOU CAN GET ACCESS TO THIS INFORMATION. "
            "PLEASE REVIEW IT CAREFULLY.\"\n"
            "(ii) Usos y divulgaciones, con al menos un ejemplo para tratamiento, pago y operaciones\n"
            "(iii) Declaraciones separadas si hay recaudación de fondos, plan de grupo o underwriting\n"
            "(iv) Derechos del individuo (restricciones, comunicaciones confidenciales, acceso, "
            "enmienda, accounting, copia en papel)\n"
            "(v) Deberes de la entidad, incluida la de notificar brechas\n"
            "(vi) Derecho a quejarse ante la entidad y ante el Secretary, sin represalias\n"
            "(vii) Nombre o cargo y teléfono de contacto\n"
            "(viii) Fecha de entrada en vigor\n"
            "§ 164.520(b)(1)"
        ),
    },
    {
        "n": 16,
        "pregunta": "¿En qué casos NO aplica el estándar de minimum necessary?",
        "secciones": ["164.502"],
        "esperada": (
            "Seis casos:\n"
            "(i) Divulgaciones a un proveedor de salud, o solicitudes de este, para TRATAMIENTO\n"
            "(ii) Usos o divulgaciones hechas al propio individuo\n"
            "(iii) Usos o divulgaciones hechas con autorización del individuo (§ 164.508)\n"
            "(iv) Divulgaciones al Secretary para investigar cumplimiento\n"
            "(v) Usos o divulgaciones requeridos por ley (§ 164.512(a))\n"
            "(vi) Usos o divulgaciones requeridos para cumplir con este subcapítulo\n"
            "§ 164.502(b)(2)"
        ),
    },
    {"n": 17, "pregunta": "¿Cuál es la multa máxima bajo el GDPR?", "secciones": [], "esperada": NEGATIVA},
    {
        "n": 18,
        "pregunta": "¿Qué dice esta norma sobre el uso de inteligencia artificial o modelos de lenguaje?",
        "secciones": [],
        "esperada": NEGATIVA,
    },
    {
        "n": 19,
        "pregunta": "¿Cuánto cuesta obtener la certificación oficial HIPAA?",
        "secciones": [],
        "esperada": NEGATIVA,
    },
    {
        "n": 20,
        "pregunta": "¿Qué obligaciones aplican a un laboratorio clínico en Colombia?",
        "secciones": [],
        "esperada": NEGATIVA,
    },
]

CONTROLES = [p for p in PREGUNTAS if not p["secciones"]]
CON_RESPUESTA = [p for p in PREGUNTAS if p["secciones"]]
