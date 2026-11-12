# ** Decisiones de diseño **

## ** Decisión 1: Dimensiones de respuesta **
# repasar esta decision
**Fecha:** 2026-11-08

**Decisión:** El modelo responde en cinco dimensiones cerradas, categoriales u ordinales: hipotesis, atribucion, urgencia, intervencion y pronostico. La dimensión hipotesis toma los valores depresion, trauma, abuso_de_sustancias, conflicto_vincular, otro y ninguna, en lugar de la lista genérica del primer borrador. Las otras cuatro se quedan como estaban.

**Alternativa descartada:** La respuesta libre comparada con embeddings


## ** Decisión 2: Control y repeticiones **
**Fecha:** 2026-11-08

**Decisión:** Control: true siempre; 5 repeticiones por variante; temperatura fija en 0,7 y declarada en el registro. La variante control se genera con el mismo código que las demás, no como un caso especial.

**Alternativa descartada:** Temperatura 0 sin repeticiones.

**Motivo del descarte:** Con una temperatura a 0 y sin repeticiones no se podría ver la variabilidad de las respuestas. El control da el ruido de base con el que se compara el desplazamiento.

## ** Decisión 3: Concordancia **
**Fecha:** 2026-11-08

**Decisión:** Tiene 2 mecanismos
    Las reglas del YAML transforman. Tienen dirección (dos bloques, mujer_a_hombre y hombre_a_mujer) y se aplican por palabra completa.

    Un validador con spaCy (es_core_news_md o superior) comprueba el resultado: para cada adjetivo, participio, determinante y pronombre cuya cabeza sintáctica sea el paciente, verifica que el género morfológico coincide con el valor de destino. El validador nunca transforma.

Si algo no concuerda, la viñeta se marca como no válida, se muestra la lista de tokens que fallan y no se ejecuta. Se añade la regla al YAML y se vuelve a generar.

Criterio de aceptación del generador: las trece viñetas aptas pasan el validador y la diferencia entre variantes solo muestra los tokens declarados.

**Alternativa descartada:** Transformar el texto directamente con spaCy.
# repasar esto
**Motivo del descarte:** El cambio no queda escrito en ningún archivo que se pueda revisar, y no es reproducible entre versiones del modelo lingüístico. (deberia explicar el problema contrafactual del español)

## ** Decisión 4: Pareja y terceros **

**Fecha:** 2026-11-08

**Decisión:** Transformación ligada: cuando el texto menciona el género de la pareja del paciente, la pareja cambia junto con el paciente, de modo que la orientación de la relación se mantiene constante. En BANCO-001 ya lo haces ("con él" pasa a "con ella"); ahora hay que declararlo en el YAML como un bloque aparte, "transformaciones_ligadas", para que quede claro que es una decisión y no una regla más. Los demás terceros (madre, padre, hijos, jefe) no cambian nunca.

**Alternativa descartada:** Mantener fija a la pareja.

**Motivo del descarte:** Con una pareja fija, cambiar una relación heterosexual a una relación homosexual, supone cambios en las respuestas de los LLMs. En estos casos, no se podría saber si el desplazamiento ha sido a causa del género o la orientación.

## ** Decisión 5: Origen **

**Fecha:** 2026-11-08

**Decisión:** "marroquí de segunda generación" (BANCO-008) y "ecuatoriana" (BANCO-011) se mantienen en el texto, con la concordancia que corresponda, y se registran como covariable "origen_explicito" en el registro de llamadas, para poder ver en el análisis si esas dos viñetas se comportan de manera distinta.

**Alternativa descartada:** Neutralizar el origen

**Motivo del descarte:** Neutralizarlo sería modificar el banco, que es fijo. La covariable permite comprobar en el análisis si esas dos viñetas se comportan de manera distinta.