"""
Hierarquia Controller
Endpoints para estrutura organizacional
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path

from app.schemas.schemas import ContagemPorArea, EmpresaResponse, HierarquiaCompleta
from app.services.hierarquia_service import HierarquiaService


logger = logging.getLogger(__name__)
router = APIRouter()


def get_hierarquia_service() -> HierarquiaService:
    """Dependency injection"""
    return HierarquiaService()


@router.get("/empresas", response_model=list[EmpresaResponse], summary="Listar todas as empresas")
async def listar_empresas(service: HierarquiaService = Depends(get_hierarquia_service)):
    """Retorna lista de todas as empresas cadastradas"""
    try:
        return service.get_all_empresas()
    except Exception as e:
        logger.error(f"Erro ao listar empresas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar empresas") from e


@router.get("/empresas/{empresa_id}", response_model=EmpresaResponse, summary="Buscar empresa por ID")
async def get_empresa(
    empresa_id: UUID = Path(..., description="ID da empresa"),
    service: HierarquiaService = Depends(get_hierarquia_service),
):
    """Retorna dados de uma empresa específica"""
    try:
        empresa = service.get_empresa(empresa_id)
        if not empresa:
            raise HTTPException(status_code=404, detail="Empresa não encontrada")
        return empresa
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar empresa: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar empresa") from e


@router.get("/empresas/{empresa_id}/arvore", summary="Árvore hierárquica completa")
async def get_arvore_hierarquica(
    empresa_id: UUID = Path(..., description="ID da empresa"),
    service: HierarquiaService = Depends(get_hierarquia_service),
):
    """
    Retorna estrutura hierárquica completa em formato de árvore

    Estrutura:
    - Diretoria
      - Gerência
        - Coordenação
          - Área
    """
    try:
        return service.get_arvore_hierarquica(empresa_id)
    except Exception as e:
        logger.error(f"Erro ao buscar árvore hierárquica: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar hierarquia") from e


@router.get(
    "/empresas/{empresa_id}/areas",
    response_model=list[HierarquiaCompleta],
    summary="Listar todas as áreas com hierarquia",
)
async def listar_areas(
    empresa_id: UUID = Path(..., description="ID da empresa"),
    service: HierarquiaService = Depends(get_hierarquia_service),
):
    """Retorna todas as áreas da empresa com caminho hierárquico completo"""
    try:
        return service.get_areas(empresa_id)
    except Exception as e:
        logger.error(f"Erro ao listar áreas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar áreas") from e


@router.get(
    "/areas/{area_id}/hierarquia", response_model=HierarquiaCompleta, summary="Hierarquia de uma área específica"
)
async def get_hierarquia_area(
    area_id: UUID = Path(..., description="ID da área"), service: HierarquiaService = Depends(get_hierarquia_service)
):
    """Retorna caminho hierárquico completo de uma área"""
    try:
        hierarquia = service.get_area_hierarquia(area_id)
        if not hierarquia:
            raise HTTPException(status_code=404, detail="Área não encontrada")
        return hierarquia
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar hierarquia da área: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar hierarquia") from e


@router.get(
    "/empresas/{empresa_id}/funcionarios/contagem",
    response_model=list[ContagemPorArea],
    summary="Contagem de funcionários por área",
)
async def contagem_funcionarios(
    empresa_id: UUID = Path(..., description="ID da empresa"),
    service: HierarquiaService = Depends(get_hierarquia_service),
):
    """Retorna quantidade de funcionários ativos em cada área"""
    try:
        return service.get_contagem_funcionarios(empresa_id)
    except Exception as e:
        logger.error(f"Erro ao contar funcionários: {e}")
        raise HTTPException(status_code=500, detail="Erro ao contar funcionários") from e
