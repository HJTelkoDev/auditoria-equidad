import json
import sys
from pathlib import Path

from src.generador.esquema import cargar_config

RAIZ = Path(__file__).resolve().parent
RUTA_CONFIG = RAIZ / "config" / "genero.yaml"
RUTA_PLANTILLA_PROMPT = RAIZ / "config" / "prompt.txt"
RUTA_BANCO = RAIZ / "data" / "casos_banco_v1.0.1.json"

def formatear_dimensiones(dimensiones):
    """Formatea las dimensiones como un diccionario JSON para reemplazar en el prompt."""

    lineas_json = ["{"]
    # posicion es el índice de la dimensión en la lista, usado para decidir si poner una coma al final
    for posicion, dimension in enumerate(dimensiones):
        valores_permitidos = " | ".join(f'"{v}"' for v in dimension.valores)
        separador = "," if posicion < len(dimensiones) - 1 else ""
        lineas_json.append(f'    "{dimension.nombre}": {valores_permitidos}{separador}')
    lineas_json.append("}")
    return "\n".join(lineas_json)

def construir_prompt(plantilla_prompt, dimensiones, viñeta):
    """
    Construye el prompt final reemplazando los marcadores de posición
    en la plantilla con los valores de las dimensiones y la viñeta.
    """
    prompt_final = plantilla_prompt.replace("{dimensiones}", formatear_dimensiones(dimensiones))
    prompt_final = prompt_final.replace("{viñeta}", viñeta)
    return prompt_final

def main():
    """Genera un prompt para un caso específico del banco de casos."""
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print("Uso: python ver_prompt.py <case_id>")
        print("Ejemplo: python ver_prompt.py BANCO-001")
        return

    case_id = sys.argv[1]
    config = cargar_config(RUTA_CONFIG)
    plantilla_prompt = RUTA_PLANTILLA_PROMPT.read_text(encoding="utf-8")

    # Viñetas excluidas del contrafactual: no se genera ningún prompt
    motivos_exclusion = {exclusion.case_id: exclusion.motivo for exclusion in config.exclusiones}
    if case_id in motivos_exclusion:
        print(f"{case_id} está EXCLUIDA y no se genera su prompt.")
        print(f"Motivo: {motivos_exclusion[case_id]}")
        return

    with open(RUTA_BANCO, encoding="utf-8") as archivo:
        casos = json.load(archivo)["casos"]

    for caso in casos:
        if caso["case_id"] == case_id:
            prompt_final = construir_prompt(plantilla_prompt, config.dimensiones, caso["viñeta"])
            print(prompt_final)
            return
    print(f"No se encontró ninguna viñeta con case_id '{case_id}'.")

if __name__ == "__main__":
    main()