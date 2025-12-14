"""
Analytics Controller
Endpoints para análises e métricas
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.services.analytics_service import AnalyticsService


router = APIRouter()


def get_analytics_service():
    return AnalyticsService()


@router.get("/enps")
async def get_enps_distribution(
    empresa_id: UUID | None = Query(None, description="Filtrar por empresa"),
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Distribuição eNPS (Employee Net Promoter Score)
    
    - **Promotores**: Respostas 9-10
    - **Neutros**: Respostas 7-8
    - **Detratores**: Respostas 0-6
    - **eNPS Score**: % Promotores - % Detratores (-100 a +100)
    """
    return service.get_enps_distribution(empresa_id)


@router.get("/tenure-distribution")
async def get_tenure_distribution(
    empresa_id: UUID | None = Query(None, description="Filtrar por empresa"),
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Distribuição de funcionários por tempo de casa
    
    Agrupa funcionários por categorias de tempo na empresa
    """
    return service.get_tenure_distribution(empresa_id)


@router.get("/satisfaction-scores")
async def get_satisfaction_scores(
    empresa_id: UUID | None = Query(None, description="Filtrar por empresa"),
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Scores médios por dimensão de avaliação
    
    Retorna a média de todas as 7 dimensões avaliadas:
    1. Ambiente de Trabalho
    2. Liderança
    3. Reconhecimento
    4. Desenvolvimento
    5. Comunicação
    6. Equilíbrio
    7. Recomendação (usado para eNPS)
    """
    return service.get_satisfaction_scores(empresa_id)
