from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
import yaml

class ModeloEstricto(BaseModel):
    """Clase base: rechaza campos que el esquema no declara"""
 
    model_config = ConfigDict(extra="forbid")
 
 
class Regla(ModeloEstricto):
    """Una sustitución de texto: aparece `de` y se pone `a`."""

    de: str = Field(min_length=1)
    a: str
    #tipo: Literal["coherencia", "reescritura"] | None = None

    @model_validator(mode="after")
    def validar_campos(self):
        # Si la regla no cambia nada, es un error
        if self.de == self.a:
            raise ValueError(f"la regla '{self.de}' no cambia nada")
        return self
 
 
class Exclusion(ModeloEstricto):
    case_id: str = Field(pattern=r"^BANCO-\d{3}$")
    motivo: str = Field(min_length=1)
 
 
class Bloque(ModeloEstricto):
    """Las reglas de una dirección de cambio de atributo"""

    transformaciones: list[Regla] = Field(min_length=1)
    transformaciones_ligadas: list[Regla] = []
    proteger: list[str] = []
 
    @model_validator(mode="after")
    def sin_repetidas(self):
        origenes_vistos = set()
        for regla in self.transformaciones + self.transformaciones_ligadas:
            if regla.de in origenes_vistos:
                raise ValueError(f"la regla '{regla.de}' está repetida en el bloque")
            origenes_vistos.add(regla.de)
        return self
 
 
class Concordancia(ModeloEstricto):
    """Ajustes del validador de concordancia con spaCy (solo comprueba, nunca transforma)."""

    verificar: bool
    modelo_spacy: str | None = None
 
    @model_validator(mode="after")
    def comprobar_modelo(self):
        if self.verificar and not self.modelo_spacy:
            raise ValueError("si 'verificar' es true, 'modelo_spacy' debe estar definido")
        return self
 
 
class Dimension(ModeloEstricto):
    """Una dimensión de la respuesta del modelo (hipotesis, urgencia, etc.)."""

    nombre: str = Field(min_length=1)
    tipo: Literal["categorial", "ordinal"]
    valores: list[str] = Field(min_length=2)
 
    @model_validator(mode="after")
    def sin_valores_repetidos(self):
        if len(set(self.valores)) != len(self.valores):
            raise ValueError(f"la dimensión '{self.nombre}' tiene valores repetidos")
        return self
 
 
class Ejecucion(ModeloEstricto):
    """Parámetros de ejecución fijados por el protocolo."""
    repeticiones: int = Field(ge=1)
    temperatura: float = Field(ge=0.0, le=2.0)
    control: bool
 
 
# Claves del YAML que NO son bloques de reglas. Todo lo demás se lee como bloque.
CLAVES_QUE_NO_SON_BLOQUES = {
    "atributo",
    "descripcion",
    "valores",
    "bloques",
    "exclusiones",
    "concordancia",
    "dimensiones",
    "ejecucion",
}
 
 
class Config(ModeloEstricto):
    atributo: str
    descripcion: str = ""
    valores: list[str | int] = Field(min_length=2)
    bloques: dict[str, Bloque]
    exclusiones: list[Exclusion] = []
    concordancia: Concordancia
    dimensiones: list[Dimension] = Field(min_length=1, max_length=6)
    ejecucion: Ejecucion
 
    @model_validator(mode="before")
    @classmethod
    def agrupar_bloques(cls, datos):
        datos = dict(datos)
        bloques = dict(datos.get("bloques") or {})
        for clave in list(datos):
            if clave not in CLAVES_QUE_NO_SON_BLOQUES:
                bloques[clave] = datos.pop(clave)
        datos["bloques"] = bloques
        return datos
 
    @model_validator(mode="after")
    def comprobar_coherencia(self):
        if not self.bloques:
            raise ValueError("el YAML no tiene ningún bloque de reglas")
 
        # Un bloque se llama "<origen>_a_<destino>" con valores declarados.
        # Así una errata en una clave del nivel superior no se cuela como bloque,
        # y el esquema sirve igual para género, edad u otro atributo.
        validos = {
            f"{origen}_a_{destino}" for origen in self.valores for destino in self.valores if origen != destino
        }
        for nombre in self.bloques:
            if nombre not in validos:
                raise ValueError(
                    f"clave desconocida o bloque inválido: '{nombre}'. "
                    f"Los bloques válidos son {sorted(validos)}"
                )
 
        nombre_de_dimensiones = [d.nombre for d in self.dimensiones]
        if len(nombre_de_dimensiones) != len(set(nombre_de_dimensiones)):
            raise ValueError("hay dimensiones con el nombre repetido")
        ids_excluidos = [e.case_id for e in self.exclusiones]
        if len(ids_excluidos) != len(set(ids_excluidos)):
            raise ValueError("hay viñetas excluidas más de una vez")
        return self
 
 
def cargar_config(ruta) -> Config:
    """Lee un YAML de configuración y lo valida contra el esquema."""
    with open(ruta, encoding="utf-8") as f:
        datos = yaml.safe_load(f)
    return Config.model_validate(datos)