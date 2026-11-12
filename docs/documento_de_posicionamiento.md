# Documento de Posicionamiento

## 1. Análisis de herramientas existentes
### 1.1. FACT

Es una herramienta de código abierto orientada a pruebas contrafactuales de sesgos en modelos de lenguaje. FACT valida la salida estructurada (JSON) contra un esquema predefinido y compara pares de respuestas utilizando pruebas estadísticas emparejadas, elegidas según el tipo de cada campo. El atributo sensible se declara únicamente mediante configuración. Incluye una condición de control (retest) que repite el caso original para medir la variabilidad del modelo, y guarda cada llamada con su respuesta en bruto junto con la configuración de la ejecución.

Sin embargo, su motor sustituye una única marca del texto por un valor fijo, por lo que carece de soporte para la concordancia gramatical necesaria en lenguas con flexión de género. Con la configuración por defecto (temperatura 0 y una repetición), su control no refleja la variabilidad de muestreo de un uso real, aunque ambos parámetros son configurables. Solo incluye un adaptador para modelos locales de Hugging Face, para otros proveedores hay que programarlos. Analiza cada modelo por separado, sin estudiar la decisión conjunta de varios modelos. Su informe es estadístico: no enlaza cada cifra con las llamadas que la generaron ni está orientado al cumplimiento regulatorio.

### 1.2. LangFair

LangFair evalúa cuantitativamente sesgos y equidad en casos de uso basados en LLM, a partir de los prompts que aporta el usuario. Proporciona métricas predefinidas de toxicidad, estereotipos y equidad contrafactual en respuestas de texto libre, además de métricas para recomendación y clasificación, lo que facilita su integración en flujos de trabajo de procesamiento del lenguaje natural.

Está diseñado para evaluar modelos individuales y para comparar textos generados (sentimiento y similitud), no decisiones clínicas estructuradas. No incorpora una condición de control explícita para diferenciar el efecto contrafactual del ruido propio del muestreo del modelo. Tampoco aborda la evaluación de decisiones colectivas en conjuntos de modelos, ni proporciona informes orientados al cumplimiento de la normativa europea de IA.

### 1.3. EQUITRIAGE

Es un estudio de auditoría contrafactual de género en el triaje de urgencias médicas. Realiza más de 374.000 evaluaciones sobre cinco modelos, alterando el nombre y el género del paciente en viñetas clínicas escritas en inglés, y distingue tres propiedades: paridad de grupo, invarianza contrafactual y calibración.

Esta referencia es fundamental para el ámbito clínico. Sin embargo, es un estudio experimental cerrado, no una plataforma de software reutilizable. Evalúa únicamente modelos aislados, no analiza el comportamiento de la «voz minoritaria» y no controla el ruido generativo del modelo, al carecer de una condición de control que repita el caso original.

## 2. Aspectos diferenciales

### 2.1. Idioma y concordancia morfológica

Para el desarrollo del banco de auditoría, es imprescindible considerar las diferencias estructurales entre el inglés y el español. Mientras que en inglés determinantes como "the" son neutros para ambos géneros, en español existe una concordancia obligatoria que afecta a determinantes ("el" para masculino y "la" para femenino), sustantivos, adjetivos, participios y pronombres.

Por ello, es necesaria una especificación declarativa (YAML) que recoja tanto las reglas de sustitución morfológica como las transformaciones ligadas. El módulo 1 (generador de pares contrafactuales) procesará las viñetas clínicas originales del banco y generará variantes controladas que difieran únicamente en el atributo protegido configurado. Las reglas se aplican con dirección y por palabra completa, y un validador morfológico comprueba que en la variante no queda ninguna palabra sin concordar, la viñeta que no supera la validación se marca y no se ejecuta.

### 2.2. Evaluación de Ensambles

El Módulo 2 (motor de ejecución) está desarrollado en Python y permite auditar los modelos de lenguaje tanto de forma individual como agrupados en conjuntos (ensembles). El sistema integra un panel variado de proveedores mediante dos modalidades:

•	**Servicios de API:**  
    Conexión asíncrona con modelos comerciales y abiertos de alto rendimiento (OpenAI, Anthropic, Google Gemini, DeepSeek y Qwen), registrando el coste real de cada llamada y estimando el coste total antes de lanzar la auditoría. Esta variedad permite analizar diferencias de alineamiento, sesgos culturales y comportamientos entre distintas familias de IA.

•	**Ejecución local con Ollama:**
    Conexión nativa con Ollama para procesar modelos open-source (como Llama 3 o Mistral) directamente en el ordenador del auditor, sin coste por llamada y sin necesidad de internet.

### ** 2.3. Informe de conformidad

Las aplicaciones de soporte al diagnóstico y valoración psicoterapéutica están clasificadas como sistemas de IA de alto riesgo bajo el Reglamento Europeo de Inteligencia Artificial (Reglamento UE 2024/1689). El marco normativo exige explícitamente la evaluación de sesgos, la gobernanza de datos y la trazabilidad de las decisiones.

El Módulo 4 (Generador de Informes) procesa los resultados analíticos y automatiza la creación de un informe de auditoría y conformidad. La característica central de este informe es la trazabilidad de extremo a extremo: cualquier métrica, tabla o gráfica estadística permite rastrear la cifra exacta hasta la llamada a la API o la ejecución local concreta que la generó.

## Referencias 
-   Bull, D. et al. (2025). LangFair: A Python Package for Assessing Bias and Fairness in LLM Use Cases. Journal of Open Source Software.
-   FACT: Fairness Audit via Counterfactual Testing. Repositorio: https://github.com/PeterM739/FACT
-   Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo (Reglamento de Inteligencia Artificial), artículos 9, 10 y 15.
-   Young, R. J. y Matthews, A. M. (2026). EQUITRIAGE: A Fairness Audit of Gender Bias in LLM-Based Emergency Department Triage. arXiv:2605.03998.