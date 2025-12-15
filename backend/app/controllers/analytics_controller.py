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


# ===== TASK 7: AREA LEVEL ANALYTICS =====


@router.get("/areas/scores-comparison")
async def get_areas_scores_comparison(
    empresa_id: UUID | None = Query(None, description="Filtrar por empresa"),
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    **Task 7 - Visualização 1: Average Feedback Scores by Department**
    
    Retorna comparação de scores médios entre áreas por dimensão.
    
    **Uso:**
    - Gráfico de barras comparando áreas
    - Identificar áreas com melhores/piores scores
    - Filtrar por dimensão específica
    
    **Resposta inclui:**
    - Scores por dimensão para cada área
    - Score médio geral por área
    - Total de funcionários e respostas
    - Hierarquia completa (diretoria → gerência → coordenação)
    """
    return service.get_areas_scores_comparison(empresa_id)


@router.get("/areas/enps-comparison")
async def get_areas_enps_comparison(
    empresa_id: UUID | None = Query(None, description="Filtrar por empresa"),
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    **Task 7 - Visualização 2: eNPS Scores Segmented by Department**
    
    Retorna comparação de eNPS entre áreas da empresa.
    
    **Uso:**
    - Gráfico comparativo de engajamento por área
    - Identificar áreas com maior/menor intenção de permanência
    - Segmentação: Promotores / Neutros / Detratores
    
    **Resposta inclui:**
    - eNPS score por área (-100 a +100)
    - Distribuição: promotores, neutros, detratores
    - Ranking de áreas (melhor → pior)
    - Médias gerais da empresa
    
    **Insights:**
    - Melhor área (maior eNPS)
    - Pior área (menor eNPS)
    - Áreas que precisam atenção
    """
    return service.get_areas_enps_comparison(empresa_id)


@router.get("/areas/{area_id}/detailed-metrics")
async def get_area_detailed_metrics(
    area_id: UUID,
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    **Métricas detalhadas de uma área específica**
    
    Retorna análise completa de uma área incluindo:
    - Scores por dimensão vs média da empresa
    - eNPS detalhado (promotores/neutros/detratores)
    - Total de funcionários
    - Hierarquia (diretoria → gerência → coordenação)
    
    **Uso:**
    - Drill-down em área específica
    - Comparação área vs empresa
    - Identificar gaps de performance
    """
    return service.get_area_detailed_metrics(area_id)
