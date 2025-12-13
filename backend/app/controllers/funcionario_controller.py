"""
Funcionário Controller
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, Depends
from app.services.funcionario_service import FuncionarioService
from app.schemas.schemas import (
    FuncionarioResponse,
    FuncionarioPaginada,
    FuncionarioCreate
)


router = APIRouter()


def get_funcionario_service():
    return FuncionarioService()


@router.get("", response_model=FuncionarioPaginada)
async def listar_funcionarios(
    empresa_id: Optional[UUID] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    areas: Optional[List[UUID]] = Query(None),
    cargos: Optional[List[UUID]] = Query(None),
    localidades: Optional[List[UUID]] = Query(None),
    cargo: Optional[str] = Query(None),
    service: FuncionarioService = Depends(get_funcionario_service)
):
    """Lista funcionários com paginação e filtros"""
    return service.listar_funcionarios(
        empresa_id=empresa_id,
        page=page,
        page_size=page_size,
        areas=areas,
        cargos=cargos,
        localidades=localidades
    )


@router.get("/buscar", response_model=FuncionarioPaginada)
async def buscar_funcionarios(
    termo: str = Query(..., min_length=3),
    empresa_id: Optional[UUID] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    areas: Optional[List[UUID]] = Query(None),
    cargos: Optional[List[UUID]] = Query(None),
    localidades: Optional[List[UUID]] = Query(None),
    service: FuncionarioService = Depends(get_funcionario_service)
):
    """Busca funcionários por nome ou email"""
    return service.buscar_funcionarios(
        empresa_id=empresa_id,
        termo=termo,
        page=page,
        page_size=page_size,
        areas=areas,
        cargos=cargos,
        localidades=localidades
    )


@router.get("/filtros")
async def obter_filtros(
    empresa_id: Optional[UUID] = Query(None),
    service: FuncionarioService = Depends(get_funcionario_service)
):
    """Obtém opções disponíveis para filtros"""
    return service.obter_filtros_disponiveis(empresa_id)


@router.get("/{funcionario_id}", response_model=FuncionarioResponse)
async def obter_funcionario(
    funcionario_id: UUID,
    service: FuncionarioService = Depends(get_funcionario_service)
):
    """Obtém detalhes de um funcionário"""
    funcionario = service.obter_funcionario(funcionario_id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario


@router.post("", status_code=201)
async def criar_funcionario(
    funcionario: FuncionarioCreate,
    service: FuncionarioService = Depends(get_funcionario_service)
):
    """Cria novo funcionário"""
    funcionario_id = service.criar_funcionario(funcionario)
    return {"id": funcionario_id, "message": "Funcionário criado com sucesso"}
