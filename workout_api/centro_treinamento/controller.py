from pydantic import UUID4
from sqlalchemy import select
from uuid import uuid4
from fastapi import HTTPException
from fastapi import APIRouter, status, Body

from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.contrib.repository.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
        '/', 
        summary="Criar uma novo Centro de Treinamento",
        status_code=status.HTTP_201_CREATED,
        response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency, 
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:    
    centro_treinamento_out = CentroTreinamentoOut(id=str(uuid4()), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
    
    db_session.add(centro_treinamento_model)
    await db_session.commit()
    return centro_treinamento_out

@router.get(
    '/', 
    summary="Consultar todas os Centros de Treinamento",
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centros_treinamentos_out: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return centros_treinamentos_out


@router.get(
    '/{id}', 
    summary="Consultar um Centro de Treinamento pelo id",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de treinamento não encontrado no id: {id}"
        )
    return centro_treinamento