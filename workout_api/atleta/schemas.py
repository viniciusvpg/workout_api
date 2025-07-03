from typing import Annotated, Optional
from pydantic import BaseModel, Field, PositiveFloat
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.repository.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="João", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="12345678900", max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", example=25)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta em kg", exampls=70.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta em metros", example= 1.75)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description="Categoria do Atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro do atleta")]


class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass

class AtletlaUpdate(BaseModel):
    nome: Annotated[Optional[str], Field(default=None, description="Nome do atleta", example="João", max_length=50)]
    idade: Annotated[Optional[int], Field(default=None, description="Idade do atleta", example=25)]
    
class CategoriaAtleta(BaseModel):
    nome: Annotated[str, Field(description="Nome da categoria do atleta", example="Categoria A", max_length=50)]

class CentroTreinamentoAtleta(BaseModel):
    nome: Annotated[str, Field(description="Nome do centro de treinamento do atleta", example="Centro A", max_length=50)]

class AtletaListOut(BaseModel):
    nome: Annotated[str, Field(description="Nome do atleta", example="João", max_length=50)]
    categoria: CategoriaAtleta
    centro_treinamento: CentroTreinamentoAtleta
    