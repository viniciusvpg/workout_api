from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Query, status, Body
from datetime import datetime
from pydantic import UUID4
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletlaUpdate, AtletaListOut
from workout_api.categorias.models import CategoriaModel
from workout_api.contrib.repository.dependencies import DatabaseDependency
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from sqlalchemy.future import select
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate

router = APIRouter()

@router.post(
    '/', 
    summary="Criar um novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DatabaseDependency, 
    atleta_in: AtletaIn = Body(...)  
):
    
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_nome))).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A Categoria: {categoria_nome} não foi encontrada."
        )
    
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
    )).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O Centro de Treinamento: {centro_treinamento_nome} não foi encontrado."
        )
    
    atleta_existente = (await db_session.execute(
        select(AtletaModel).filter_by(cpf=atleta_in.cpf)
    )).scalars().first()

    if atleta_existente:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER, 
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
        )
        
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
        
    except Exception as e:

        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao inserir os dados no banco"
        )

    return atleta_out

@router.get(
    '/', 
    summary="Consultar todas os Atletas",
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaListOut],
)
async def query(
    db_session: DatabaseDependency, 
    nome: Optional[str] = Query(None, description="Filtrar atletas por nome"),
    cpf: Optional[str] = Query(None, description="Filtrar atletas por CPF")
) -> Page[AtletaListOut]:
    query = select(AtletaModel)
    
    if nome:
        query = query.filter(AtletaModel.nome == nome)

    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)
    
    atletas: list[AtletaModel] = (await db_session.execute(query)).scalars().all()
    
    if not atletas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhum Atleta encontrado com as informações fornecidas."
        )

    return await sqlalchemy_paginate(db_session, query)

@router.get(
    '/{id}', 
    summary="Consultar uma Atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com não encontrada no id: {id}"
        )
    return atleta

@router.get(
    '/{id}', 
    summary="Consultar uma Atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com não encontrada no id: {id}"
        )
    return atleta

@router.patch(
    '/{id}', 
    summary="Editar um Aleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletlaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com não encontrada no id: {id}"
        )
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
            setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)
    
    return atleta

@router.delete(
    '/{id}', 
    summary="Deletar um Atleta pelo id",
    status_code=status.HTTP_204_NO_CONTENT
)
async def query(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não foi possivel remover o Atleta ID: {id}"
        )

    await db_session.delete(atleta)
    await db_session.commit()


