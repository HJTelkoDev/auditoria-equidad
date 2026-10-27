# Banco de auditoría de equidad contrafactual para LLM.
Desarrollo de un software de auditoria automatizada de equidad contrafactual en Python. Con el uso de diferentes LLMs para evaluar el trato diferencial  por género y edad en razonamiento clínico psicoterapéutico sobre viñetas sintéticas.
 
## Arquitectura
Especificación Declarativa: Definición YAML de reglas contrafactuales, concordancia morfosintáctica en español y dimensiones clínicas.
Módulo 1 (Generador): Producción de pares contrafactuales con validación de concordancia y condición de control.
Módulo 2 (Motor Multiproveedor): Ejecución asíncrona para APIs (OpenAI, Anthropic, Gemini, DeepSeek, Qwen) y local (Ollama).
Módulo 3 (Analítico): Cálculo de desplazamiento, ruido generativo de base, evaluación de ensembles y análisis de la voz minoritaria.
Módulo 4 (Informes): Generación de reportes trazables alineados con el Reglamento de IA de la UE (AI Act - Arts. 9, 10 y 15).
