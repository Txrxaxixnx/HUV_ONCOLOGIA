01 – Esquema de Datos del Proyecto

Actualizacion v2.5
- El esquema operativo de 55 columnas se mantiene como base historica y ahora se persiste en SQLite (`huv_oncologia.db`).
- La version 2.5 agrega columnas derivadas `IHQ_*` (HER2, Ki-67, RE, RP, PD-L1, P16, Estudios Solicitados) almacenadas junto a las 55 columnas originales.
- Este documento conserva la referencia detallada del esquema legacy y orienta la convergencia con el Esquema Maestro H.U.V.


Introducción
- Este documento es la referencia central del esquema de datos manejado por EVARISIS Gestor H.U.V. Aquí se describe el Esquema Operativo actual (55 columnas) validado en v1.0, la relación con el Esquema Maestro institucional del H.U.V, y el mapa de expansión para los nuevos campos de IHQ planificados en la Fase 2 del roadmap.

Esquema Operativo (55 Columnas)
- Fuente de verdad: `EJEMPLO DE LO QUE TENGO.xlsx` (salida auditada/confirmada del sistema para las plantillas soportadas). A continuación, se listan las 55 columnas con su propósito y un ejemplo ilustrativo.

| Nombre de la Columna | Descripción del Campo | Ejemplo de Dato |
|---|---|---|
| N. petición (0. Número de biopsia) | Identificador del caso (formato por tipo: Axxxxx, IHQxxxxxx, Mxxxxxxx, Rxxxxxx). | IHQ250905 |
| Hospitalizado | Estado de hospitalización del paciente. | SI |
| Sede | Sede institucional donde se procesa/atiende. | PRINCIPAL |
| EPS | Aseguradora/EPS reportada. | EMSSANAR S.A.S |
| Servicio | Servicio/área clínica de origen. | GINECOLOGIA |
| Médico tratante | Nombre del médico tratante. | NOMBRE APELLIDO |
| Especialidad | Especialidad deducida/asignada (heurística por servicio). | MEDICO INTENSIVISTA |
| Ubicación | Ubicación interna/área (si aplica). | UCI 3 |
| N. Autorización | Número de autorización (o COEX en IHQ). | COEX |
| Identificador Único | Identificador adicional (p. ej., defunción). | 2510326 |
| Datos Clínicos | Indicador/nota de datos clínicos suministrados. | SI |
| Fecha ordenamiento | Fecha considerada como ordenamiento (ver reglas por tipo). | 12/07/2025 |
| Tipo de documento | Tipo de documento del paciente. | CC |
| N. de identificación | Número de documento del paciente. | 1107**** |
| Primer nombre | Primer nombre del paciente. | JEISON |
| Segundo nombre | Segundo nombre del paciente. | ARMANDO |
| Primer apellido | Primer apellido del paciente. | RIVERA |
| Segundo apellido | Segundo apellido del paciente. | HENAO |
| Fecha de nacimiento | Derivada desde edad + fecha de referencia (si aplica). | 18/08/1991 |
| Edad | Edad en años (derivada del texto de edad). | 33 |
| Género | Sexo del paciente. | MASCULINO |
| Número celular | Teléfono celular (si aplica). | 3xx xxx xx xx |
| Dirección de correo electrónico | Email del paciente (si aplica). | ejemplo@correo.com |
| Dirección de correo electrónico 2 | Email alterno (si aplica). | — |
| Contacto de emergencia | Nombre/contacto de emergencia. | — |
| Departamento | Departamento de residencia. | VALLE DEL CAUCA |
| Teléfono del contacto | Teléfono de contacto (si aplica). | — |
| Municipio | Municipio de residencia. | CALI |
| N. muestra | Identificador de muestra (coincide o extiende N. petición). | A250092 |
| CUPS | Código CUPS por tipo de informe. | 898807 |
| Tipo de examen (4, 12, Método de obtención de la muestra, factor de certeza para el diagnóstico) | Clasificador de tipo de examen/obtención. | INMUNOHISTOQUIMICA |
| Procedimiento (11. Tipo de estudio para el diagnóstico) | Descripción estandarizada del procedimiento (por CUPS). | 898807 Estudio anatomopatológico de marcación inmunohistoquímica |
| Órgano (1. Muestra enviada a patología) | Órgano/tejido principal reportado. | CUERPO HUMANO COMPLETO |
| Tarifa | Tarifa aplicada. | GENERAL |
| Valor | Valor facturable (si aplica). | 0.0 |
| Copago | Copago (si aplica). | — |
| Descuento | Descuento (si aplica). | — |
| Fecha de ingreso (2. Fecha de la muestra) | Fecha de ingreso o fecha de toma. | 14/07/2025 |
| Fecha finalización (3. Fecha del informe) | Fecha de finalización del informe. | 26/08/2025 |
| Usuario finalización | Usuario que finaliza el informe. | ARMANDO CORTES |
| Usuario asignación micro | Usuario asignación micro (si aplica). | — |
| Fecha asignación micro | Fecha asignación micro (si aplica). | — |
| Malignidad | Presencia de malignidad (heurística por palabras clave). | PRESENTE |
| Condición | Condición particular (si aplica). | — |
| Descripción macroscópica | Texto macroscópico/“Resumen de historia clínica” asociado. | [Texto] |
| Descripción microscópica (8,9, 10,12. Invasión linfovascular y perineural, índice mitótico/Ki67, Inmunohistoquímica, tamaño tumoral) | Texto microscópico y hallazgos clave. | [Texto] |
| Descripción Diagnóstico (5,6,7 Tipo histológico, subtipo histológico, márgenes tumorales) | Texto diagnóstico detallado. | [Texto] |
| Diagnóstico Principal | Diagnóstico principal (resumen). | [Texto] |
| Comentario | Comentarios adicionales del informe. | [Texto] |
| Informe adicional | Observaciones de informe adicional (si aplica). | — |
| Congelaciones / Otros estudios | Notas sobre congelaciones/otros estudios. | — |
| Líquidos (5 Tipo histológico) | Observaciones de líquidos (si aplica). | — |
| Citometría de flujo (5 Tipo histológico) | Observaciones de citometría (si aplica). | — |
| Hora Desc. macro | Sello/registro de hora para desc. macro (si aplica). | 2025-08-26 10:30:00 |
| Responsable macro | Responsable macro asignado (si aplica). | [Nombre] |

Notas de conformidad
- Los nombres de las columnas en el Excel fuente pueden contener tildes y mayúsculas específicas; este documento estandariza la ortografía para facilitar lectura, sin alterar el mapeo funcional.
- El esquema operativo actual se mantiene como estándar validado para v1.0.

Esquema Maestro H.U.V (Referencia Institucional)
- Fuente: `BD_JULIO PARA ENSAYO IA.xlsx`. Este archivo sirve como “esquema maestro” de referencia del H.U.V y guía la expansión del esquema operativo.
- Encabezados en segunda fila (fila 2, índice 1). En el artefacto disponible se detectan 167 columnas de encabezado. Si existen versiones con 169, validar variaciones por hoja o actualización del archivo maestro.
- Uso: orientar mapeos extendidos (Fase 3) y asegurar compatibilidad con reportes institucionales.

Mapa de Expansión (Fase 2 – Nuevos Campos IHQ)
- Base de análisis: textos OCR crudos de `EXCEL/DEBUG_OCR_OUTPUT_IHQ250905.pdf.txt` e `EXCEL/DEBUG_OCR_OUTPUT_IHQ250906.pdf.txt`.
- Objetivo: definir heurísticas/patrones para extraer los biomarcadores planificados.

Estudios Solicitados
- Patrón observado (IHQ250905):
  - Encabezado “Estudios solicitados” y sección “Estudios Solicitados:” en el cuerpo.
  - Ejemplo de línea: “Se realizó tinción especial para CK7, CK20, CDX2, EMA, SOX10, GATA3.”
- Heurística:
  - Localizar el encabezado “Estudios solicitados” o “Estudios Solicitados:” y capturar la lista de marcadores hasta el fin de línea o punto final.
  - Regex ejemplo: `(?i)estudios\s+solicitados:?\s*(?:se\s+realizó\s+tinción\s+especial\s+para\s*)?([A-Z0-9 ,+/.-]+)`
  - Normalizar separadores por coma/espacio y unificar alias (p. ej., “SOX 10” → “SOX10”).

P16 (Estado y Porcentaje)
- Patrón observado (IHQ250906):
  - “... niveles histológicos ... tinción con: p16 y p40.”
  - “Las células tumorales presentan marcación para p16 en bloque y p40.”
  - “P16 POSITIVO.”
- Heurística:
  - Estado: buscar “\bP16\b.*?(POSITIVO|NEGATIVO)” o frases como “marcación para p16 en bloque” (mapear “en bloque” como positivo difuso).
  - Porcentaje: si existe, capturar “(\d{1,3})\s*%” próximo a “P16” o en la misma sección; si no aparece, dejar vacío.
  - Regex ejemplo estado: `(?i)\bP\s*16\b[^\n]*\b(positiv[oa]|negativ[oa])\b`
  - Regex ejemplo porcentaje: `(?i)\bP\s*16\b[^\n%]*?(\d{1,3})\s*%`

HER2
- Patrón esperado (no presente en los textos analizados):
  - Reportes IHQ suelen consignar HER2 con escala semicuantitativa: 0 / 1+ / 2+ / 3+ y/o resultado ISH/FISH (amplificado/no amplificado).
- Heurística:
  - Buscar “\bHER2\b” u “HER2/neu” seguido de “0|1\+|2\+|3\+” y capturar el score.
  - Adicional: detectar “ISH|FISH.*(amplificad[oa]|no amplificad[oa])”.
  - Regex ejemplo score: `(?i)\bHER2(?:/neu)?\b\s*[:\-]??\s*(0|1\+|2\+|3\+)`
  - Regex ejemplo ISH/FISH: `(?i)\b(?:ISH|FISH)\b[^\n]*\b(amplificad[oa]|no\s*amplificad[oa])\b`

KI-67 (Ki67)
- Patrón esperado (mencionado como posible en descripciones):
  - Indicado como índice de proliferación y típicamente expresado en porcentaje.
- Heurística:
  - Buscar “\bKI\s*[- ]?67\b” o “\bKi67\b” y capturar porcentaje a la derecha.
  - Regex ejemplo: `(?i)\bK[il]\s*[- ]?67\b[^\n%]*?(\d{1,3})\s*%`

Receptor Hormonal de Estrógeno (RE / ER)
- Sinónimos: “Receptor de Estrógeno”, “RECEPTOR HORMONAL DE ESTRÓGENO”, “ER”.
- Heurística:
  - Capturar estado (positivo/negativo) y, si existe, porcentaje/Allred.
  - Regex estado: `(?i)(receptor(?:\s+hormonal)?\s+de\s+estr(o|ó)geno|\bER\b)[^\n]*\b(positiv[oa]|negativ[oa])\b`
  - Regex %: `(?i)(receptor(?:\s+hormonal)?\s+de\s+estr(o|ó)geno|\bER\b)[^\n%]*?(\d{1,3})\s*%`

Receptor Hormonal de Progestágenos (RP / PR)
- Sinónimos: “Receptor de Progesterona”, “RECEPTOR HORMONAL DE PROGESTÁGENOS”, “PR”.
- Heurística:
  - Idéntica a RE, reemplazando por PR/Progesterona.
  - Regex estado: `(?i)(receptor(?:\s+hormonal)?\s+de\s+progest(erona|ágenos)|\bPR\b)[^\n]*\b(positiv[oa]|negativ[oa])\b`
  - Regex %: `(?i)(receptor(?:\s+hormonal)?\s+de\s+progest(erona|ágenos)|\bPR\b)[^\n%]*?(\d{1,3})\s*%`

PD-L1 (PDL-1)
- Sinónimos: “PD-L1”, “PDL1”, “PD L1”. Reportado como TPS% y/o CPS.
- Heurística:
  - Detectar líneas con PD-L1 y capturar TPS/CPS si existen.
  - Regex TPS: `(?i)\bPD\s*-?L1\b[^\n]*\bTPS\b[^\n%]*?(\d{1,3})\s*%`
  - Regex CPS: `(?i)\bPD\s*-?L1\b[^\n]*\bCPS\b[^\n\d]*?(\d{1,3})`

Normalización y controles
- Unificar alias y espacios (p. ej., “SOX 10” → “SOX10”; “P D - L 1” → “PD-L1”).
- Permitir variaciones de acentuación y mayúsculas/minúsculas (`re.IGNORECASE`).
- Definir precedencia de secciones: buscar primero en “RESULTADO DE INMUNOHISTOQUÍMICA”, luego en “DESCRIPCIÓN MICROSCÓPICA”, y como fallback en todo el texto del informe.
- Cuando un marcador no aparezca en el informe, registrar vacío (no aplica/no reportado).

Anexo – Ubicación típica en IHQ (según ejemplos)
- Estudios Solicitados: encabezado explícito y/o frase “Se realizó tinción especial para …”.
- P16: puede aparecer en la sección de macroscopía/microscopía con “marcación” y cierre con “P16 POSITIVO/NEGATIVO”.
- Otros biomarcadores (HER2, Ki-67, RE, RP, PD-L1): suelen consignarse en “RESULTADO DE INMUNOHISTOQUÍMICA” o parte final de la microscopia.

Mapa de Mapeo Preliminar (Esquema Operativo → Esquema Maestro)
- Objetivo: orientar la compatibilidad del Esquema Operativo (55) con el Esquema Maestro H.U.V (167). Se listan candidatos probables según similitud semántica. La validación final se hará con el equipo clínico y/o dueños del maestro.

| Columna Operativa (55) | Candidato(s) en Esquema Maestro (167) | Observaciones |
|---|---|---|
| N. petición (0. Número de biopsia) | — | Operativo interno; no hay campo explícito en maestro. |
| Hospitalizado | — | Operativo; no presente en maestro. |
| Sede | — | Operativo; no presente en maestro. |
| EPS | Código de la EPS o de la entidad territorial | Equivalente directo. |
| Servicio | — | Operativo; no presente en maestro. |
| Médico tratante | — | No hay campo directo; podría inferirse vía IPS/atenciones. |
| Especialidad | — | Operativo; no presente en maestro. |
| Ubicación | — | Operativo; no presente en maestro. |
| N. Autorización | — | Operativo; no presente en maestro. |
| Identificador Único | CÓDIGO ÚNICO DE IDENTIFICACIÓN (BDUA-BDEX-PVS) | Alinear semántica institucional del “identificador único”. |
| Datos Clínicos | — | Indicador operativo; maestro no captura este flag. |
| Fecha ordenamiento | FECHA INGRESO IPS QUE REALIZÓ EL DX | Alternativa: “FECHA NOTA REMISIÓN/INTERCONSULTA…”. |
| Tipo de documento | TIPO IDENTIFICACIÓN | Equivalente directo. |
| N. de identificación | NÚMERO DOCUMENTO | Equivalente directo. |
| Primer nombre | 1er NOMBRE | Equivalente directo. |
| Segundo nombre | 2do SEGUNDO | Equivalente directo (etiqueta maestro). |
| Primer apellido | 1er APELLIDO | Equivalente directo. |
| Segundo apellido | 2do APELLIDO | Equivalente directo. |
| Fecha de nacimiento | FECHA DE NACIMIENTO | Equivalente directo. |
| Edad | — | Derivable de fecha de nacimiento; no suele existir como campo crudo. |
| Género | SEXO | Equivalente directo. |
| Número celular | TELÉFONO | Consolidar con “Teléfono del contacto”. |
| Dirección de correo electrónico | — | No identificado en maestro. |
| Dirección de correo electrónico 2 | — | No identificado en maestro. |
| Contacto de emergencia | — | No identificado en maestro. |
| Departamento | Municipio de Residencia - CÓDIGO DIVIPOLA | Departamento derivable por DIVIPOLA. |
| Teléfono del contacto | TELÉFONO | Equivalente directo. |
| Municipio | Municipio de Residencia - CÓDIGO DIVIPOLA | Equivalente (codificado). |
| N. muestra | — | Operativo; relaciona con N. petición/especímenes; sin campo explícito. |
| CUPS | TIPO DE PRUEBA | No existe campo “CUPS” general; para cirugía sí hay “CÓDIGO CUPS PRIMERA CIRUGIA”. |
| Tipo de examen (4, 12, …) | TIPO DE PRUEBA | Alinear taxonomía de tipos. |
| Procedimiento (11. Tipo de estudio…) | TIPO DE PRUEBA | Mapeo de descripción operativa a categoría del maestro. |
| Órgano (1. Muestra enviada a patología) | HISTOLOGÍA DEL TUMOR | “Órgano” alimenta determinación de histología; no hay campo “órgano” libre. |
| Tarifa | — | Operativo; no presente en maestro. |
| Valor | — | Operativo/facturación; no presente en maestro. |
| Copago | — | Operativo/facturación; no presente en maestro. |
| Descuento | — | Operativo/facturación; no presente en maestro. |
| Fecha de ingreso (2. Fecha de la muestra) | FECHA DE RECOLECCIÓN HISTOPATOLÓGICO | Equivalente principal. |
| Fecha finalización (3. Fecha del informe) | FECHA DE INFORME HISTOPATOLÓGICO VÁLIDO | Equivalente principal. |
| Usuario finalización | — | Operativo; no presente en maestro. |
| Usuario asignación micro | — | Operativo; no presente en maestro. |
| Fecha asignación micro | — | Operativo; no presente en maestro. |
| Malignidad | NOMBRE DE LA NEOPLASIA (CÁNCER) | Derivable desde diagnóstico/histología; no campo “Malignidad” explícito. |
| Condición | — | Operativo; no presente en maestro. |
| Descripción macroscópica | — | Maestro no almacena texto libre; insumo para campos estructurados. |
| Descripción microscópica (… Ki67 … IHQ …) | — | Igual a anterior; insumo para campos estructurados (p. ej., KI-67, HER2). |
| Descripción Diagnóstico (tipo/subtipo/márgenes) | HISTOLOGÍA DEL TUMOR | Consolidar a un código/valor estandarizado. |
| Diagnóstico Principal | NOMBRE DE LA NEOPLASIA (CÁNCER) | Equivalente probable. |
| Comentario | — | No identificado en maestro. |
| Informe adicional | — | No identificado en maestro. |
| Congelaciones /Otros estudios | TIPO DE PRUEBA | Según proceda. |
| Líquidos (5 Tipo histológico) | — | No identificado en maestro (posible texto libre). |
| Citometría de flujo (5 Tipo histológico) | TIPO DE PRUEBA | Según proceda. |
| Hora Desc. macro | — | Operativo; no presente en maestro. |
| Responsable macro | — | Operativo; no presente en maestro. |

Notas
- El Esquema Maestro incorpora campos de estadificación (TNM/FIGO), pruebas específicas (HER2) y tratamientos (quimioterapia/radioterapia), que serán alimentados parcialmente cuando se habilite Fase 2 (IHQ) y Fase 3 (BD + ETL).
- Los campos operativos no presentes en el maestro pueden mantenerse a nivel de staging/ETL para auditoría y trazabilidad, sin formar parte del modelo maestro definitivo.
