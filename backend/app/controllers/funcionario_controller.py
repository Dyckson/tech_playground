"""
Funcionário Controller
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.schemas import FuncionarioCreate, FuncionarioPaginada, FuncionarioResponse
from app.services.funcionario_service import FuncionarioService


router = APIRouter()


def get_funcionario_service():
    return FuncionarioService()


@router.get("", response_model=FuncionarioPaginada)
async def listar_funcionarios(
    empresa_id: UUID | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    areas: list[UUID] | None = Query(None),
    cargos: list[UUID] | None = Query(None),
    localidades: list[UUID] | None = Query(None),
    tempo_casa: list[UUID] | None = Query(None),
    score_min: float | None = Query(None, ge=1, le=7),
    score_max: float | None = Query(None, ge=1, le=7),
    enps_status: str | None = Query(None, pattern="^(promotor|neutro|detrator)$"),
    order_by: str = Query("nome", pattern="^(nome|cargo|area|tempo|score)$"),
    order_dir: str = Query("asc", pattern="^(asc|desc)$"),
    service: FuncionarioService = Depends(get_funcionario_service),
):
    """Lista funcionários com paginação e filtros avançados"""
    return service.listar_funcionarios(
        empresa_id=empresa_id,
        page=page,
        page_size=page_size,
        areas=areas,
        cargos=cargos,
        localidades=localidades,
        tempo_casa=tempo_casa,
        score_min=score_min,
        score_max=score_max,
        enps_status=enps_status,
        order_by=order_by,
        order_dir=order_dir,
    )


@router.get("/buscar", response_model=FuncionarioPaginada)
async def buscar_funcionarios(
    termo: str = Query(..., min_length=2),
    empresa_id: UUID | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    areas: list[UUID] | None = Query(None),
    cargos: list[UUID] | None = Query(None),
    localidades: list[UUID] | None = Query(None),
    tempo_casa: list[UUID] | None = Query(None),
    score_min: float | None = Query(None, ge=1, le=7),
    score_max: float | None = Query(None, ge=1, le=7),
    enps_status: str | None = Query(None, pattern="^(promotor|neutro|detrator)$"),
    order_by: str = Query("nome", pattern="^(nome|cargo|area|tempo|score)$"),
    order_dir: str = Query("asc", pattern="^(asc|desc)$"),
    service: FuncionarioService = Depends(get_funcionario_service),
):
    """Busca funcionários por nome ou email com filtros avançados"""
    return service.buscar_funcionarios(
        empresa_id=empresa_id,
        termo=termo,
        page=page,
        page_size=page_size,
        areas=areas,
        cargos=cargos,
        localidades=localidades,
        tempo_casa=tempo_casa,
        score_min=score_min,
        score_max=score_max,
        enps_status=enps_status,
        order_by=order_by,
        order_dir=order_dir,
    )


@router.get("/filtros")
async def obter_filtros(
    empresa_id: UUID | None = Query(None), service: FuncionarioService = Depends(get_funcionario_service)
):
    """Obtém opções disponíveis para filtros"""
    return service.obter_filtros_disponiveis(empresa_id)


@router.get("/{funcionario_id}", response_model=FuncionarioResponse)
async def obter_funcionario(funcionario_id: UUID, service: FuncionarioService = Depends(get_funcionario_service)):
    """Obtém detalhes de um funcionário"""
    funcionario = service.obter_funcionario(funcionario_id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario


@router.get("/{funcionario_id}/detailed-profile")
async def obter_perfil_detalhado(funcionario_id: UUID, service: FuncionarioService = Depends(get_funcionario_service)):
    """
    Obtém perfil detalhado do funcionário com analytics completo
    
    Inclui:
    - Dados básicos do funcionário
    - Comparação de scores (funcionário vs empresa vs área)
    - Histórico de avaliações
    - Comentários detalhados por dimensão
    - Análise de diferenças e tendências
    """
    from app.services.analytics_service import AnalyticsService
    
    # Buscar dados básicos do funcionário
    funcionario = service.obter_funcionario(funcionario_id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    # Buscar analytics detalhado
    analytics_service = AnalyticsService()
    analytics = analytics_service.get_employee_detailed_profile(funcionario_id)
    
    return {
        "employee": funcionario,
        "analytics": analytics,
    }


@router.post("", status_code=201)
async def criar_funcionario(
    funcionario: FuncionarioCreate, service: FuncionarioService = Depends(get_funcionario_service)
):
    """Cria novo funcionário"""
    funcionario_id = service.criar_funcionario(funcionario)
    return {"id": funcionario_id, "message": "Funcionário criado com sucesso"}
