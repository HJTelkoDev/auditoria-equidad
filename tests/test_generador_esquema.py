import copy
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from src.generador.esquema import Config, cargar_config

RUTA_GENERO_YAML = Path(__file__).resolve().parent.parent / "config" / "genero.yaml"
 
@pytest.fixture
def datos_genero():
    """Devuelve los datos del YAML de configuración de género como diccionario."""
    return yaml.safe_load(RUTA_GENERO_YAML.read_text(encoding="utf-8"))
 
 
def test_genero_yaml_valido():
    """Comprueba que el YAML de configuración de género es válido según el esquema."""
    config = cargar_config(RUTA_GENERO_YAML)
    assert config.atributo == "genero"
    assert set(config.bloques) == {"mujer_a_hombre", "hombre_a_mujer"}
    assert len(config.dimensiones) == 5
 
 
def test_falta_campo_obligatorio(datos_genero):
    """Comprueba que falta un campo obligatorio provoca un error de validación."""
    del datos_genero["ejecucion"]
    with pytest.raises(ValidationError):
        Config.model_validate(datos_genero)
 
 
def test_dimension_con_un_solo_valor(datos_genero):
    """Comprueba que una dimensión con un solo valor provoca un error de validación."""
    datos_genero["dimensiones"][0]["valores"] = ["depresion"]
    with pytest.raises(ValidationError):
        Config.model_validate(datos_genero)
 
 
def test_dimension_con_valores_repetidos(datos_genero):
    """Comprueba que una dimensión con valores repetidos provoca un error de validación."""
    datos_genero["dimensiones"][2]["valores"] = ["baja", "baja", "alta"]
    with pytest.raises(ValidationError):
        Config.model_validate(datos_genero)
 
 
def test_tipo_de_dimension_desconocido(datos_genero):
    """Comprueba que una dimensión con un tipo desconocido provoca un error de validación."""
    datos_genero["dimensiones"][0]["tipo"] = "categorica"
    with pytest.raises(ValidationError):
        Config.model_validate(datos_genero)
 
 
def test_regla_repetida_en_un_bloque(datos_genero):
    """Comprueba que una regla repetida en un bloque provoca un error de validación."""
    datos_genero["mujer_a_hombre"]["transformaciones"].append(
        copy.deepcopy(datos_genero["mujer_a_hombre"]["transformaciones"][0])
    )
    with pytest.raises(ValidationError, match="repetida"):
        Config.model_validate(datos_genero)
 
 
def test_regla_que_no_cambia_nada(datos_genero):
    """Comprueba que una regla que no cambia nada provoca un error de validación."""
    datos_genero["hombre_a_mujer"]["transformaciones"][0]["a"] = datos_genero["hombre_a_mujer"]["transformaciones"][0]["de"]
    with pytest.raises(ValidationError, match="no cambia nada"):
        Config.model_validate(datos_genero)
 
 
def test_errata_en_clave_de_nivel_superior(datos_genero):
    """Comprueba que una errata en una clave de nivel superior provoca un error de validación."""
    datos_genero["dimension"] = datos_genero.pop("dimensiones")
    with pytest.raises(ValidationError):
        Config.model_validate(datos_genero)
 
 
def test_bloque_con_valores_no_declarados(datos_genero):
    """Comprueba que un bloque con valores no declarados provoca un error de validación."""
    datos_genero["hombre_a_otro"] = datos_genero.pop("hombre_a_mujer")
    with pytest.raises(ValidationError, match="bloque inválido"):
        Config.model_validate(datos_genero)

 
def test_campo_desconocido_en_una_regla(datos_genero):
    """Comprueba que un campo desconocido en una regla provoca un error de validación."""
    datos_genero["mujer_a_hombre"]["transformaciones"][0]["extra"] = "x"
    with pytest.raises(ValidationError, match="Extra inputs"):
        Config.model_validate(datos_genero)

 
def test_verificar_sin_modelo_spacy(datos_genero):
    """Comprueba que verificar sin modelo de spaCy provoca un error de validación."""
    datos_genero["concordancia"] = {"verificar": True}
    with pytest.raises(ValidationError):
        Config.model_validate(datos_genero)


def test_exclusion_con_case_id_mal_formado(datos_genero):
    """Comprueba que una exclusión con un case_id que no coincide con el patrón provoca un error de validación."""
    datos_genero["exclusiones"][0]["case_id"] = "BANCO-XYZ"
    with pytest.raises(ValidationError):
        Config.model_validate(datos_genero)

 
def test_exclusion_repetida(datos_genero):
    """Comprueba que una exclusión repetida provoca un error de validación."""
    datos_genero["exclusiones"].append(copy.deepcopy(datos_genero["exclusiones"][0]))
    with pytest.raises(ValidationError, match="excluidas"):
        Config.model_validate(datos_genero)