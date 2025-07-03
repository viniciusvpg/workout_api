from uuid import UUID
from pydantic import Field
from typing_extensions import Annotated
from workout_api.contrib.repository.schemas import BaseSchema


class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", example="Scale", max_length=10)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID, Field(description="Identificador da Categoria")]
