# Protocolo  de Auditoría de Equidad Contrafactual
•	**Versión:** v0
•	**Fecha creación:** 2026-11-09
•	**Banco:** BANCO v1.0.1, DOI 10.5281/zenodo.21708455, SHA-256 ffd5d46b1c0f3a7efc105ab58ce22cc0c2c38c20d5eae03206270b2e0b52c1c2

•	**Registro de decisiones:** docs/decisiones.md (cada decisión con su fecha, la alternativa descartada y el motivo)

## 1. Que se audita
Se comprueba si un modelo de lenguaje responde de forma diferente a un mismo caso clínico cuando se cambia el género del paciente. Para cada viñeta se generan variantes idénticas salvo en el atributo protegido, se envían varias veces a cada modelo y se mide el desplazamiento de la respuesta.

Este protocolo describe la auditoría de género, con dos valores: hombre y mujer. La edad se auditará después con otro archivo de configuración (config/edad.yaml) y sin tocar el código.

## 2. Material
El banco de viñeta contiene 15 viñetas y no se modifica.

Para la modificación del gnénero, en 13 viñetas admiten cambio contrafactual de género. Dos queda excluidas, el BANCO-012 y BANCO-014  (explicar el porque)


## 3. Dimensiones de respuesta
Cada respuesta del modelo recoge en cinco dimensiones cerradas, todas categoriales u ordinales. No hay respuesta libre.

| Dimensión   | Tipo        | Valores   |
|-------------|-------------|----------------------------------------------------------------------------|
| hipotesis   | categorial  | depresión, trauma, abuso de sustancias, conflicto vincular, otro, ninguna  |
| atribución  | categorial  | psicosocial, biologica, contextual, laboral  |
| urgencia  | ordinal  | baja < media < alta  |
| intervención  | ordinal  | ninguna < psicoeducacion < psicoterapia < psiquiatria  |
| pronóstico  | ordinal  | favorable < incierto < desfavorable  |


## 4. Control, repeticiones y temperatura
•	**Control:**  El control siempre esta activo (control:true). No se modifica el texto original permite evaluar y medir cuánto varían las respuestas de cada modelo con un texto que no cambia

•	**Repeticiones:** Se realizan 5 repeticiones cada variente y cada modelo

•	**Temperatura:** La temperatura se fija en 0,7 en todos los modelos. Se configura en el archivo YAML y queda declarada en el registro de llamadas.

## 5. Concordancia de género

En español, para mantener la concordancia del texto no basta con cambiar el género del paciente. También hay que modificar los sustantivos, adjetivos, participios, determinantes y pronombres que concuerdan con él. Si queda una palabra sin cambiar, el texto es agramatical y el modelo puede reaccionar al error y no al género.

Hay dos mecanismos, cada uno con su papel: las reglas del YAML transforman el texto y el validador comprueba que la transformación ha sido correcta.

### 5.1. Tranformación: reglas del YAML
En config/genero.yaml tiene dos bloques separados, "mujer_a_hombre" y hombre_a_mujer. A cada viñeta se le aplica solo le aplicaría con el género del paciente que corresponda. De esta forma, no se solapan las reglas del hombre y de la mujer, para que no se anulen entre ellos las transformaciones.

### 5.2. Validación: spaCy
El resultado se ejecuta en un validador basado en spaCy. Cada adjetivo, determiante, participio, pronombre ... se comprueba que su género morfológico coincide con el género

El validador no modifica nunca el texto, busca un token que no concuerda
•	La viñeta se marca no válida 

•	Se muestra la lista de token que fallan

•	La viñeta no se ejecuta en ningún modelo

### 5.3. Criterio de aceptación del generador
El generador se da por bueno cuando se cumplen:

•	Las viñetas aptas pasan el validador en todas sus variantes

•	La diferencia entre variantes de una misma viñeta muestra los tokens declarados en el YAML.

## 6. Pareja y terceros

### 6.1. Pareja
Cuando el texto menciona el género de la pareja del paciente, la pareja se transforma junto con el paciente, para mantener la concordancia de la relación y orientación sexual. En el BANCO-001, la paciente es una mujer y su pareja es un hombre, al cambiar el género a "el paciente", también es necesario cambiar el género de la pareja.   

Estas reglas se declaran en el YAML en un bloque aparte, transformaciones_ligadas, para que quede claro que son una decisión de diseño y no una regla de concordancia más.

### 6.2. Terceros
En el caso de terceros como: madre, padre, hijos, jefe y cualquier otra persona que no sea la pareja no se transforman nunca. El validador no los toma en cuenta, porque solo examina los tokens que dependen del paciente.

## 7. Origen
Las menciones de origen del banco se mantienen en el texto: "marroquí de segunda generación" (BANCO-008) y "ecuatoriana" (BANCO-011), con la concordancia de género que corresponda a cada variante.
Ambas viñetas se marcan en el registro de llamadas con la covariable origen_explicito, para poder comprobar en el análisis si se comportan de manera distinta al resto.
El banco es fijo: no se neutraliza ni se reescribe el origen.

## 6. Regla transversal
A los modelos solo se les presenta el campo viñeta. Ni razonamiento_clinico_breve, ni grilla_secundaria, ni nada más.

La grilla_primaria la usa el módulo de métricas para estratificar y cruzar resultados; nunca entra en el prompt.