#  Análisis de documentos de referencia 

## 1. EQUITRIAGE: A Fairness Audit of Gender Bias in LLM-Based Emergency Department Triage 

### ¿Qué miden? 

Miden el sesgo de género en la toma de decisiones clínicas automatizadas para el triaje en servicios de urgencias hospitalarias. Evalúan si la asignación de la escala de gravedad del paciente varía al modificar el género en la viñeta clínica.

### ¿Cómo lo miden?

Realizan una evaluación contrafactual masiva, con más de 374.000 evaluaciones sobre cinco modelos. Generan pares contrafactuales alterando el nombre y los términos de género, y comparan paridad de grupo, invarianza contrafactual y calibración por género. Excluyen explícitamente las viñetas cuyo contenido está intrínsecamente ligado al sexo biológico.

### ¿Qué no hacen?

No controlan el ruido generativo de base de los modelos: no hay una condición de control que repita el caso original, por lo que parte de la variación atribuida al género puede deberse al muestreo. Además, el contrafactual principal cambia nombre y género a la vez; solo en una ablación con dos modelos separan el cambio de género del cambio de nombre. Por último, la escala ESI que usan como referencia procede del triaje humano, que ya contiene sesgo de género.

## 2. Baseline-Aware Counterfactual Audits for Clinical NLP 

### ¿Qué miden?

Miden la capacidad de aislar el sesgo contrafactual real frente al ruido o la variabilidad generativa de base en auditorías de procesamiento del lenguaje natural aplicadas al ámbito clínico.

### ¿Cómo lo miden?

Introducen una condición de control no demográfica: una paráfrasis del caso que conserva el contenido clínico y los atributos del paciente. Comparan las diferencias que produce el cambio de edad o de sexo con las que produce el control, sobre doce casos sintéticos de triaje y tres modelos. Además miden el «suelo de ruido» de cada modelo, repitiendo la misma entrada sin modificar.

### ¿Qué no hacen?

No trabajan con una muestra suficiente: son doce casos sintéticos y tres repeticiones, y los propios autores presentan sus análisis como exploratorios. Su medida del ruido se basa en la similitud del texto, que no distingue una variación de estilo de un cambio clínico real. Tampoco fijan un umbral formal para decidir cuándo un efecto supera el ruido.

## 3. Sociodemographic biases in medical decision making by large language models (Omar et al.) 

### ¿Qué miden?

Miden la presencia de sesgos sociodemográficos (raza, género y orientación sexual, entre otros) en las recomendaciones clínicas de los LLM, evaluando si influyen en la prioridad de triaje, las pruebas diagnósticas, el nivel de tratamiento y la valoración de salud mental.

### ¿Cómo lo miden?

Evalúan nueve modelos de lenguaje mediante el intercambio sistemático de variables sociodemográficas en casos clínicos, aplicando análisis estadístico multivariante.

### ¿Qué no hacen?

No distinguen entre la invarianza contrafactual (tratar igual a individuos idénticos salvo en el atributo) y la paridad (igualdad de resultados entre grupos poblacionales): comparan tasas de cada grupo frente al control. Tampoco separan el efecto del atributo del ruido del modelo, porque su control es un caso sin etiqueta y no una repetición del mismo texto.

## 4. Minority Sentinel: When to Overturn Majority Voting in Multi-Agent LLM Debates

### ¿Qué miden?
Miden las condiciones bajo las cuales la opinión de un modelo minoritario en un debate o conjunto de LLM es más acertada que la decisión de la mayoría.

### ¿Cómo lo miden?
Analizan debates multiagente sobre tareas de razonamiento que poseen una respuesta correcta de referencia. Cuantifican la exactitud de los agentes discrepantes frente al consenso del grupo.

### ¿Qué no hacen?
Necesitan una única «verdad de referencia» (ground truth) para decidir cuándo la minoría tiene razón, por lo que el método no es aplicable a tareas donde esa verdad no existe.

## 5. Emergent Bias and Fairness in Multi-Agent Decision Systems

### ¿Qué miden?
Miden cómo emerge y se propaga el sesgo en sistemas de decisión multiagente, y muestran que la equidad del conjunto no se deduce de la equidad de los modelos individuales.

### ¿Cómo lo miden?
Simulan sistemas de tres agentes LLM que discuten hasta alcanzar un consenso en tareas financieras con datos tabulares (riesgo de crédito y estimación de ingresos). Comparan el sesgo del sistema con el de sus componentes mediante métricas de equidad de grupo por género.

### ¿Qué no hacen?
No explican en qué condiciones un sistema amplifica o atenúa el sesgo; los autores lo dejan como trabajo futuro. Miden solo equidad de grupo frente a etiquetas correctas, y se limitan a dos conjuntos de datos y a un atributo.

## 6. FACT: Fairness Audit via Counterfactual Testing

### ¿Qué miden?
Miden si la salida estructurada de un LLM cambia cuando solo se modifica un atributo sensible, sin modificar el resto del contenido. La herramienta mide diferencias y no decide si constituyen sesgo: no da una puntuación global ni un ranking de modelos.

### ¿Cómo lo miden?
El atributo y sus valores se declaran en un archivo YAML. Cada caso contiene una marca que se sustituye por un valor neutro para el original, o por el texto de cada valor del atributo para los contrafactuales. Validan la respuesta en formato JSON contra un esquema estricto; las respuestas inválidas no se reparan ni se descartan, se guardan con su estado. Comparan los pares de cada caso mediante pruebas estadísticas emparejadas según el tipo de campo (McNemar, Wilcoxon, Stuart–Maxwell y t emparejada), con corrección de Benjamini–Hochberg por comparaciones múltiples. Incluyen una condición de control (retest) que repite el caso original, guardan cada llamada con su respuesta en bruto y generan un informe en PDF.

### ¿Qué no hacen?
No gestionan la concordancia gramatical: la sustitución es literal sobre una única marca, lo que basta en sus casos en inglés pero no en lenguas con flexión de género, donde el cambio obliga a modificar varias palabras del texto. Solo incluyen un adaptador para modelos locales de Hugging Face, para otros proveedores hay que programarlos. Por defecto trabajan con temperatura 0 y una única repetición, por lo que su control no refleja la variabilidad de muestreo de un uso real, aunque ambos parámetros son configurables. Analizan cada modelo por separado.

### Referencias
1. Young, R. J. y Matthews, A. M. (2026). EQUITRIAGE: A Fairness Audit of Gender Bias in LLM-Based Emergency Department Triage. arXiv:2605.03998. https://arxiv.org/abs/2605.03998
2. Baseline-Aware Counterfactual Audits for Clinical NLP (2026). Proceedings of the BioNLP Workshop 2026. https://aclanthology.org/2026.bionlp-1.14.pdf
3. Omar, M. et al. (2025). Sociodemographic biases in medical decision making by large language models. Nature Medicine. https://www.nature.com/articles/s41591-025-03626-6
4. He et al. (2026). Minority Sentinel: When to Overturn Majority Voting in Multi-Agent LLM Debates. arXiv:2606.29270. https://arxiv.org/abs/2606.29270
5. Madigan et al. (2025). Emergent Bias and Fairness in Multi-Agent Decision Systems. arXiv:2512.16433. https://arxiv.org/abs/2512.16433
6. FACT: Fairness Audit via Counterfactual Testing. Repositorio de código. https://github.com/PeterM739/FACT