#  Análisis de documentos de referencia 

## 1. EQUITRIAGE: A Fairness Audit of Gender Bias in LLM-Based Emergency Department Triage 

### ¿Qué miden? 

Miden el sesgo de género en la toma de decisiones clínicas automatizadas para el triaje en servicios de urgencias hospitalarias. Evalúan si la asignación de la escala de gravedad del paciente varía al modificar el género en la viñeta clínica.

### ¿Cómo lo miden?

Realizan una evaluación contrafactual masiva, con más de 374.000 evaluaciones sobre 5 modelos. Generan pares contrafactuales alterando el nombre y los términos de género, comparando paridad de grupo, invarianza contrafactual y calibración por género. Excluyen explícitamente las viñetas cuyo contenido está intrínsecamente ligado al sexo biológico.

### ¿Qué no hacen?

No controlan el ruido estocástico o generativo de base de los modelos: no hay una condición de control que repita el caso original, por lo que parte de la variación atribuida al género puede deberse al muestreo. Además, el contrafactual principal cambia nombre y género a la vez, y la escala ESI que usan como referencia procede del triaje humano, que ya contiene sesgo de género.

## 2. Baseline-Aware Counterfactual Audits for Clinical NLP 

### ¿Qué miden?

Miden la capacidad de aislar el sesgo contrafactual real frente al ruido estocástico o la variabilidad generativa de base en auditorías de Procesamiento del Lenguaje Natural (PLN) aplicadas al ámbito clínico.

### ¿Cómo lo miden?

Introducen una condición de control no demográfica: una paráfrasis del caso que conserva el contenido clínico y los atributos del paciente. Comparan las diferencias que produce el cambio de edad o de sexo con las que produce el control, sobre 12 casos sintéticos de triaje y tres modelos. Además miden el "suelo de ruido" de cada modelo, repitiendo la misma entrada sin modificar.

### ¿Qué no hacen?

No trabajan con una muestra suficiente: son 12 casos sintéticos y tres repeticiones, y los propios autores presentan sus análisis como exploratorios. Su medida del ruido se basa en la similitud del texto, que no distingue una variación de estilo de un cambio clínico real. Tampoco fijan un umbral formal para decidir cuándo un efecto supera el ruido.

## 3. Sociodemographic biases in medical decision making by large language models (Omar et al.) 

### ¿Qué miden?

Miden la presencia de sesgos sociodemográficos (raza, género, orientación sexual...) en las recomendaciones clínicas de los LLM, evaluando si influyen en la prioridad de triaje, las pruebas diagnósticas, el nivel de tratamiento y la valoración de salud mental.

### ¿Cómo lo miden?

Evalúan 9 modelos de lenguaje de alto nivel mediante el intercambio sistemático de variables sociodemográficas en casos clínicos, aplicando análisis estadístico multivariante.

### ¿Qué no hacen?

No distinguen entre la invarianza contrafactual (tratar igual a individuos idénticos salvo en el atributo) y la paridad (igualdad de resultados entre grupos poblacionales): comparan tasas de cada grupo frente al control. Tampoco separan el efecto del atributo del ruido del modelo, porque su control es un caso sin etiqueta y no una repetición del mismo texto.

## 4. Minority Sentinel: When to Overturn Majority Voting in Multi-Agent LLM Debates

### ¿Qué miden?
Miden las condiciones bajo las cuales la opinión de un modelo minoritario en un debate o conjunto de LLMs es objetivamente más precisa o correcta que la decisión de la mayoría.

### ¿Cómo lo miden?
Analizan debates multiagente sobre tareas de razonamiento que poseen una respuesta correcta de referencia. Cuantifican la exactitud de los agentes discrepantes frente al consenso del grupo.

### ¿Qué no hacen?
Necesitan una única "verdad de referencia" (ground truth) para decidir cuándo la minoría tiene razón, por lo que el método no es aplicable a tareas donde esa verdad no existe. Miden únicamente exactitud objetiva, no invarianza contrafactual ante atributos protegidos.

## 5. Emergent Bias and Fairness in Multi-Agent Decision Systems

### ¿Qué miden?
Miden cómo emerge y se propaga el sesgo en sistemas de decisión multi-agente, demostrando que la equidad conjunta no es una suma lineal de la equidad de los modelos individuales.

### ¿Cómo lo miden?
Simulan sistemas de tres agentes LLM que discuten hasta alcanzar un consenso en tareas financieras con datos tabulares (riesgo de crédito y estimación de ingresos). Comparan el sesgo del sistema con el de sus componentes mediante métricas de equidad de grupo por género.

### ¿Qué no hacen?
No explican en qué condiciones un sistema amplifica o atenúa el sesgo; los autores lo dejan como trabajo futuro. Miden la equidad de grupo frente a etiquetas correctas, no la invarianza contrafactual, y se limitan a dos conjuntos de datos y a un atributo.

## 6. FACT: Fairness Audit via Counterfactual Testing

### ¿Qué miden?
Miden si la salida de un LLM cambia cuando solo se modifica un atributo sensible, sin modificar el resto del contenido. El atributo y sus valores se declaran en un archivo YAML.

### ¿Cómo lo miden?
Cada caso contiene una marca que se sustituye por un valor neutro para el original, o por el texto de cada valor del atributo para los contrafactuales. Validan la respuesta en formato JSON contra un esquema estricto y comparan los pares de cada caso mediante pruebas estadísticas emparejadas según el tipo de campo, con corrección por comparaciones múltiples. Incluyen una condición de control que repite el caso original y generan un informe en PDF.

### ¿Qué no hacen?
No gestionan la concordancia gramatical: la sustitución es literal sobre una única marca, lo que basta en sus casos en inglés pero no en español, donde el género obliga a cambiar varias palabras del texto. Solo ejecutan modelos locales de Hugging Face y, por defecto, con temperatura 0 y una única repetición, por lo que su control no mide la variabilidad de muestreo de un uso real.