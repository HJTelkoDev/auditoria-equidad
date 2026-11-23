# Formato del Registro de llamadas
•	**Versión:** v0
•	**Fecha creación:** 2026-11-21

Este documento explica el registro que se genera en el motor y que leen las métricas y el informe.


## 1. Archivos de una ejecución
Cada ejecución crea una carpeta **runs/<fecha>_<run_id>/** con 3 archivos:

| Archivo | Contenido | Una fila por |
| --- | --- | --- |
| `llamadas.parquet` | Cada llamada a un modelo, incluidas las fallidas. Se puede exportar a llamadas.csv. | Viñeta × variante × modelo × repetición |
| `variantes.parquet` | El texto exacto generado y el resultado de la validación de concordancia. | Viñeta × variante (y una fila por viñeta excluida) |
| `ejecucion.json` | Metadatos comunes a toda la ejecución. Hashes, parámetros, modelos... | Ejecución |


## 2. Reglas generales
•	**Una fila por llamada, haya respuesta o no:** Si una llamada falla, la fila se guarda con su estado y su motivo.
•	**Solo se añade, no se edita:** Si algo cambia, se hace otra ejecución.
•	**Los valores categoriales se escriben igual que en el YAML:** minúsculas y sin tildes (`depresion`, `abuso_de_sustancias`).
•	**Lo que no se puede rellenar se guarda como nulo:** no como cadena vacía.
•	**La respuesta bruta se guarda siempre que exista:** aunque no se pueda interpretar.
•	**Ningún nombre de columna menciona hombre o mujer:** todo se expresa con atributo, variante y tipo_de_texto, para que el mismo esquema sirva con edad.yaml sin cambios.
•	**El registro contiene texto del banco:** prompt_enviado, respuesta_bruta y variantes.texto incluyen las viñetas. Para respetar las reglas de uso del banco, runs/ va en .gitignore y solo se publican ejecucion.json, las métricas y el informe.

## 3. Tabla de las Llamadas
### 3.1 Identificación de la ejecución

| # | Columna | Tipo | Nulo | Descripción |
| --- | --- | --- | --- | --- |
| 1 | `run_id` | texto | no | Identificador de la ejecución. |
| 2 | `llamada_id` | texto | no | Clave única: run_id\|case_id\|variante\|modelo\|repeticion. |
| 3 | `fecha_utc` | fecha y hora | no | Momento de la llamada que dio el resultado, en UTC. |
| 4 | `case_id` | texto | no | BANCO-001 a BANCO-015. |
| 5 | `atributo` | texto | no | Atributo auditado, tomado del YAML (genero). |
| 6 | `variante` | texto | no | Valor del atributo en el texto enviado (hombre, mujer) |
| 7 | `tipo_de_texto` | texto | no | original, contrafactual |
| 8 | `repeticion` | entero | no | Hasta 5 repeticiones. |
| 9 | `hash_texto_variante` | texto | no | SHA-256 del texto que vio el modelo. Enlaza con `variantes`. |

#### Tipos de texto
•	**Original:** el texto de la viñeta del banco, sin cambios.
•	**Contrafactual:** el texto transformado con las reglas del YAML, con el otro valor del atributo.

### 3.2 Qué se envió
Se copian del banco. No entran nunca en el prompt: solo sirven para desagregar resultados.

| # | Columna | Tipo | Nulo | Descripción |
| --- | --- | --- | --- | --- |
| 10 | `cuadro` | texto | no | De `grilla_primaria.cuadro`. |
| 11 | `apertura_interpretativa` | texto | no | De `grilla_primaria.apertura_interpretativa`. |
| 12 | `origen_explicito` | booleano | no | Verdadero en BANCO-008 y BANCO-011. |
### 3.3 Modelo y parámetros

| # | Columna | Tipo | Nulo | Descripción |
| --- | --- | --- | --- | --- |
| 13 | `proveedor` | texto | no |  `gemini`, `anthropic`, `openai`, `ollama`, `deepseek`... |
| 14 | `familia_modelo` | texto | no | Para agregar por familia. |
| 15 | `modelo` | texto | no | Nombre tal como se pide a la API. |
| 16 | `version_modelo` | texto | no | La que devuelve la API; si no la devuelve, la declarada en `ejecucion.json`. |
| 17 | `temperatura` | decimal | sí | Temperatura enviada (0,7). Nula si el modelo no la admite. |
| 18 | `max_tokens` | entero | no | Límite de salida enviado. |
| 19 | `parametros_extra` | texto (JSON) | sí | Otros parámetros enviados (`top_p`, `seed`...). |


### 3.4 Prompt y respuesta

| # | Columna | Tipo | Nulo | Descripción |
| --- | --- | --- | --- | --- |
| 20 | `prompt_enviado` | texto | no | El prompt completo, tal como se envió. |
| 21 | `respuesta_bruta` | texto | sí | La respuesta completa del modelo. Nula solo si la API no devolvió nada. |
| 22 | `json_extraido` | texto | sí | Bloque JSON que extrajo el intérprete.|

Guardar el prompt entero en cada fila.

### 3.5 Dimensiones de respuesta

| # | Columna | Tipo | Nulo | Descripción |
| --- | --- | --- | --- | --- |
| 23 | `hipotesis` | texto | sí | `depresion`, `trauma`, `abuso_de_sustancias`, `conflicto_vincular`, `otro`, `ninguna`. |
| 24 | `atribucion` | texto | sí | 	`psicosocial`, `biologica`, `contextual`, `laboral`. |
| 25 | `urgencia` | texto | sí | `baja`, `media`, `alta`. |
| 26 | `intervencion` | texto | sí | `ninguna`, `psicoeducacion`, `psicoterapia`, `psiquiatria`. |
| 27 | `pronostico` | texto | sí | `favorable`, `incierto`, `desfavorable`. |


### 3.6 Estado

| # | Columna | Tipo | Nulo | Descripción |
| --- | --- | --- | --- | --- |
| 28 | `estado` | texto | no | La información del estado se encuentra más abajo, en la sección 4 |
| 29 | `motivo` | texto | sí | Explicación cuando `estado` no es `ok`. |
| 30 | `intentos` | entero | no | Intentos hasta obtener este resultado. |

### 3.7 Coste

| # | Columna | Tipo | Nulo | Descripción |
| --- | --- | --- | --- | --- |
| 31 | `tokens_entrada` | entero | sí | Tokens del prompt, según la API. |
| 32 | `tokens_salida` | entero | sí | Tokens de la respuesta, según la API. |
| 33 | `tokens_razonamiento` | entero | sí | Nulo si la API no los separa. |
| 34 | `coste_usd` | decimal | sí | Calculado con las tarifas anotadas en `ejecucion.json`. |
| 35 | `tiempo_de_respuesta` | decimal | sí | Segundos que tardó en dar la respuesta el modelo. |

### 3.8 Trazabilidad

Se repiten en cada fila a propósito: Parquet los comprime casi sin coste.

| # | Columna | Tipo | Nulo | Descripción |
| --- | --- | --- | --- | --- |
| 36 | `hash_banco` | texto | no | SHA-256 del banco, recalculado al cargarlo. |
| 37 | `hash_yaml` | texto | no | SHA-256 del YAML de la ejecución. |
| 38 | `hash_plantilla_prompt` | texto | no | SHA-256 de `config/prompt.txt`. |

## 4. Estados de una llamada
| Estado | Cuándo | Dimensiones |
| `ok` | 	Respuesta interpretada y todos los valores permitidos. | Rellenas |
| `formato_invalido` | No hay JSON interpretable o falta una clave. | Nulas |
| `valor_invalido` | JSON interpretable, pero algún valor no está en el YAML. | Nulas |
| `rechazo` | El modelo declina responder. | Nulas |
| `error` | Sin respuesta tras los reintentos. | Nulas |

## 5. Tabla variantes

**`variantes.parquet`**, salida del módulo 1, una fila por `(case_id, variante)`. Aquí están también las viñetas excluidas y el motivo, para que nada se descarte en silencio.

| Columna | Descripción |
|---|---|
| `case_id`, `tipo_de_texto` | Clave. Las viñetas excluidas tienen una fila con `tipo_de_texto = null` |
| `variante` | Valor del atributo en el texto. Nulo en las excluidas. |
| `apto` | Booleano. Falso en las viñetas excluidas. |
| `motivo_exclusion` | Texto copiado del motivo de exclusiones en el YAML; nulo si es apto. |
| `texto` | Viñeta de la variante. Nulo en las excluidas. |
| `hash_texto_variante` | Hash del texto; enlaza con el llamadas |
| `tokens_modificados` | Lista de `(original, nuevo)` según el diff |
| `validador_ok`, `validador_fallos` | Resultado del validador spaCy y lista de tokens que no concuerdan |

## 6. Invariantes
El motor las comprueba al escribir y el módulo 4 al leer. Si alguna falla, el informe no se genera.

•	`llamada_id` es único
•	Cada llamada tiene su fila (case_id, tipo_de_texto) en variantes, con apto y validador_ok
•	
•	Si estado es ok, todas las dimensiones tienen un valor del YAML. En cualquier otro estado, las dimensiones son nulas y motivo no lo es.
•	
•	hash_banco coincide con el hash declarado del banco.
•	coste_usd se puede recalcular con los tokens y las tarifas de ejecucion.json
•	emperatura coincide con la del YAML, salvo que sea nula.

## 7. Ejecucion JSON
**`ejecucion.json`**, una vez por ejecución:
•	`run_id`, fechas de inicio y fin.
•	Hash declarado y hash calculado del banco, hash del YAML, copia del YAML, versión del protocolo.
•	Modelos planificados con su configuración.
•	Tabla de precios con la fecha de consulta y su fuente.
•	Estimación de coste previa a la ejecución, y número de llamadas planificadas, ejecutadas y válidas.
•	Versiones de Python, spaCy, es_core_news_md, pyarrow y demás dependencias.

##  8. Qué lee cada módulo
| **Módulo** | **Qué necesita de este registro** |
| 3. Métricas | De llamadas: case_id, tipo_de_texto, variante, repeticion, modelo, familia_modelo, estado y las dimensiones. De variantes: nada más que el filtro de viñetas válidas. De las covariables: cuadro, apertura_interpretativa y origen_explicito. Del YAML: tipo y orden de las dimensiones. |
| 4. Informe | Todo lo anterior, más ejecucion.json, el coste, las versiones de los modelos y las viñetas excluidas con su motivo. Cada cifra enlaza con los llamada_id de las filas que la generaron. |