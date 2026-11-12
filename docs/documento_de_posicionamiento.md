# Documento de Posicionamiento

## 1. Análisis de herramientas existentes
### 1.1. FACT

Es una herramienta de código abierto orientada a pruebas contrafactuales de sesgos en modelos de lenguaje. FACT valida la salida estructurada (JSON) contra un esquema predefinido y compara pares de respuestas utilizando pruebas estadísticas emparejadas. El atributo sensible se declara únicamente mediante configuración, e incluye una condición de control que repite el caso original para medir la variabilidad del modelo.

Sin embargo, su motor sustituye una única marca del texto por un valor fijo, por lo que carece de soporte para la concordancia gramatical necesaria en lenguas con flexión de género. Además, solo ejecuta modelos locales de Hugging Face y analiza cada modelo por separado, sin estudiar la decisión conjunta de varios modelos (ensembles). Su informe es estadístico, no enlaza cada cifra con las llamadas que la generaron ni está orientado al cumplimiento regulatorio.

### 1.2. LangFair

LangFair evalúa cuantitativamente sesgos y equidad en casos de uso basados en LLM, a partir de los prompts que aporta el usuario. Proporciona métricas predefinidas de toxicidad, estereotipos y equidad contrafactual en respuestas de texto libre, además de métricas para recomendación y clasificación, facilitando la integración con flujos de trabajo de procesamiento de lenguaje natural.

Está diseñado para interactuar con modelos individuales y para comparar textos generados (sentimiento y similitud), no decisiones clínicas estructuradas. No incorpora una condición de control explícita para diferenciar la deriva contrafactual del ruido estocástico propio del muestreo del LLM. Tampoco aborda la evaluación de decisiones colectivas en conjuntos, ni proporciona informes estructurados orientados al cumplimiento de la normativa europea de IA.

### 1.3. EQUITRIAGE

Se trata de un estudio sobre la auditoría contrafactual de género en el triaje de urgencias médicas. Realiza más de 374.000 evaluaciones sobre 5 modelos, alterando el nombre y el género del paciente en las viñetas clínicas (escritas en inglés), y distingue tres propiedades: paridad de grupo, invarianza contrafactual y calibración.

Esta referencia es fundamental para el ámbito clínico. Sin embargo, se trata de un estudio experimental cerrado, no de una plataforma de software reutilizable. Evalúa únicamente modelos aislados, no analiza el comportamiento de la "voz minoritaria", y no controla el ruido generativo del modelo, al carecer de una condición de control que repita el caso original.

## 2. Aspectos diferenciales

### 2.1. Idioma y concordancia morfológica

Para el desarrollo del banco de auditoría, es imprescindible considerar las diferencias estructurales entre el inglés y el español. Mientras que en inglés determinantes como "the" son neutros para ambos géneros, en español existe una concordancia obligatoria que afecta a determinantes ("el" para masculino y "la" para femenino), sustantivos, adjetivos, participios y pronombres.

Por ello, es necesaria una especificación declarativa (YAML) que empaquete tanto las reglas de sustitución morfológica como las transformaciones ligadas. El Módulo 1 (Generador de Pares Contrafactuales) es el encargado de procesar las viñetas clínicas originales del banco de datos y generar variantes controladas que difieran únicamente en el atributo protegido configurado. Las reglas se aplican con dirección y por palabra completa, y un validador morfológico comprueba que en la variante no queda ninguna palabra sin concordar; la viñeta que no supera la validación se marca y no se ejecuta.

### 2.2. Evaluación de Ensambles

El Módulo 2 (motor de ejecución) está desarrollado en Python y permite auditar los modelos de lenguaje tanto de forma individual como agrupados en conjuntos (ensembles). El sistema integra un panel variado de proveedores mediante dos modalidades:

•	**Servicios de API:**  
    Conexión asíncrona con modelos comerciales y abiertos de alto rendimiento (OpenAI, Anthropic, Google Gemini, DeepSeek y Qwen), registrando el coste real de cada llamada y estimando el coste total antes de lanzar la auditoría. Esta variedad permite analizar diferencias de alineamiento, sesgos culturales y comportamientos entre distintas familias de IA.

•	**Ejecución local con Ollama:**
    Conexión nativa con Ollama para procesar modelos open-source (como Llama 3 o Mistral) directamente en el ordenador del auditor, sin coste por llamada y sin necesidad de internet.

### ** 2.3. Informe de conformidad

Las aplicaciones de soporte al diagnóstico y valoración psicoterapéutica están clasificadas como sistemas de IA de alto riesgo bajo el Reglamento Europeo de Inteligencia Artificial (Reglamento UE 2024/1689). El marco normativo exige explícitamente la evaluación de sesgos, la gobernanza de datos y la trazabilidad de las decisiones.

El Módulo 4 (Generador de Informes) procesa los resultados analíticos y automatiza la creación de un informe de auditoría y conformidad. La característica central de este informe es la trazabilidad de extremo a extremo: cualquier métrica, tabla o gráfica estadística permite rastrear la cifra exacta hasta la llamada a la API o la ejecución local concreta que la generó.
