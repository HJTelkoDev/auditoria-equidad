import json
import os
import re
import sys
from pathlib import Path
 
import yaml
 
# Rutas de los archivos que usa el programa
RAIZ = Path(__file__).resolve().parent.parent
RUTA_CONFIG = RAIZ / "config" / "genero.yaml"
RUTA_BANCO = RAIZ / "data" / "casos_banco_v1.0.1.json"
RUTA_SALIDA = RAIZ / "runs" / "comprobacion_de_cambios_contrafactuales_de_genero.md"
 
# Códigos de color para la terminal
ROJO = "\033[91m"   # Rojo para destacar los cambios en el texto original
VERDE = "\033[92m"  # Verde para destacar los cambios en la variante
RESETEAR_COLOR = "\033[0m"  # Fin del color, para resetear al color normal de la terminal
 
 
def cargar_config_yaml():
    # Lee el archivo YAML con las reglas de género
    with open(RUTA_CONFIG, encoding="utf-8") as f:
        return yaml.safe_load(f)
 
 
def cargar_banco():
    # Lee el JSON del banco y devuelve la lista de casos
    with open(RUTA_BANCO, encoding="utf-8") as casos:
        banco = json.load(casos)
    return banco["casos"]
 
 
def construir_reglas(bloque):
    """
    Junta todas las reglas de un bloque (mujer_a_hombre u hombre_a_mujer)
    en un diccionario {texto_original: texto_nuevo}.
    """
    reglas = {}
 
    for regla in bloque["transformaciones"]:
        reglas[regla["de"]] = regla["a"]
 
    # Las transformaciones ligadas son las de la pareja del paciente
    for regla in bloque["transformaciones_ligadas"]:
        reglas[regla["de"]] = regla["a"]
 
    # Las frases protegidas se "sustituyen" por sí mismas, así no se tocan
    # aunque dentro tengan una palabra con regla
    frases_protegidas = bloque.get("proteger") or []
    for frase in frases_protegidas:
        reglas[frase] = frase
 
    return reglas
 
 
def construir_patron(reglas):
    """
    Crea una única expresión regular que busca todas las reglas a la vez.
 
    - Se ordenan de más larga a más corta para que "con él" se pruebe antes que "él".
    - (?<!\\w) y (?!\\w) obligan a que sea palabra completa: "ella" no coincide
      dentro de "aquella".
    """
    textos = sorted(reglas.keys(), key=len, reverse=True)
 
    alternativas = []
    for texto in textos:
        alternativas.append(r"(?<!\w)" + re.escape(texto) + r"(?!\w)")
 
    return re.compile("|".join(alternativas))
 
 
def transformar(texto, reglas):
    """
    Recorre el texto una sola vez y lo divide en fragmentos.
 
    Devuelve una lista de tuplas (original, nuevo). Si los dos elementos son
    iguales, ese fragmento no cambia; si son distintos, ahí se aplicó una regla.
    """
    patron = construir_patron(reglas)
    fragmentos = []
    posicion = 0
 
    for coincidencia in patron.finditer(texto):
        # Texto que hay entre la coincidencia anterior y esta (no cambia)
        sin_cambio = texto[posicion:coincidencia.start()]
        fragmentos.append((sin_cambio, sin_cambio))
 
        # Texto que coincide con una regla
        encontrado = coincidencia.group(0)
        fragmentos.append((encontrado, reglas[encontrado]))
 
        posicion = coincidencia.end()
 
    # Lo que queda después de la última coincidencia
    resto = texto[posicion:]
    fragmentos.append((resto, resto))
 
    return fragmentos
 
 
def contar_cambios(fragmentos):
    # Cuenta cuántos fragmentos son distintos en el original y en la variante
    total = 0
    for original, nuevo in fragmentos:
        if original != nuevo:
            total += 1
    return total
 
 
def montar_texto(fragmentos, version, marca_inicio, marca_fin):
    """
    Vuelve a unir los fragmentos en un solo texto.
 
    version = "original" o "variante".
    Los fragmentos que cambian se rodean con marca_inicio y marca_fin.
    """
    texto = ""
    for original, nuevo in fragmentos:
        if version == "original":
            trozo = original
        else:
            trozo = nuevo
 
        if original != nuevo:
            texto += marca_inicio + trozo + marca_fin
        else:
            texto += trozo
    return texto
 
 
def direccion_de_la_viñeta(viñeta):
    # Decide qué bloque de reglas toca según cómo empieza la viñeta
    if viñeta.startswith("Mujer"):
        return "mujer_a_hombre"
    return "hombre_a_mujer"
 
 
def main():
    os.system("")  # necesario para que la terminal de Windows muestre los colores
    sys.stdout.reconfigure(encoding="utf-8")
 
    config = cargar_config_yaml()
    casos = cargar_banco()
 
    # Viñetas excluidas y su motivo
    excluidas = {}
    for exclusion in config["exclusiones"]:
        excluidas[exclusion["case_id"]] = exclusion["motivo"]
 
    # Si se pasa un identificador por línea de comandos, solo se muestra esa viñeta
    caso_pedido = None
    if len(sys.argv) > 1:
        caso_pedido = sys.argv[1]
 
    lineas_informe = ["# Comprobación de cambios contrafactuales de género\n",
                      "Los cambios están en negrita.\n"]
 
    for caso in casos:
        case_id = caso["case_id"]
        viñeta = caso["viñeta"]
 
        if caso_pedido is not None and case_id != caso_pedido:
            continue
 
        if case_id in excluidas:
            print(f"\n===== {case_id}  EXCLUIDA: {excluidas[case_id]}")
            continue
 
        direccion = direccion_de_la_viñeta(viñeta)
        reglas = construir_reglas(config[direccion])
        fragmentos = transformar(viñeta, reglas)
        num_cambios = contar_cambios(fragmentos)
 
        # Salida por pantalla: cambios entre corchetes y en color
        print(f"\n===== {case_id}  {direccion}  ({num_cambios} cambios)")
        print("\nORIGINAL:")
        print(montar_texto(fragmentos, "original", ROJO + "[", "]" + RESETEAR_COLOR))
        print("\nVARIANTE:")
        print(montar_texto(fragmentos, "variante", VERDE + "[", "]" + RESETEAR_COLOR))
 
        # Salida para el archivo Markdown: cambios en negrita
        lineas_informe.append(f"## {case_id} ({direccion}, {num_cambios} cambios)\n")
        lineas_informe.append("**Original**\n")
        lineas_informe.append(montar_texto(fragmentos, "original", "**", "**") + "\n")
        lineas_informe.append("**Variante**\n")
        lineas_informe.append(montar_texto(fragmentos, "variante", "**", "**") + "\n")
 
    RUTA_SALIDA.parent.mkdir(exist_ok=True)
    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_informe))
    print(f"\nTambién guardado en {RUTA_SALIDA}")
 
 
if __name__ == "__main__":
    main()
