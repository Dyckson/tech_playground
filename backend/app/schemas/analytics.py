"""
Schemas de Analytics e eNPS
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from uuid import UUID


class EnpsGeral(BaseModel):
    """eNPS geral da empresa"""
    enps: float = Field(..., ge=-100, le=100)
    promotores: int
    promotores_pct: float
    passivos: int
    passivos_pct: float
    detratores: int
    detratores_pct: float
    total: int


class EnpsPorSegmento(BaseModel):
    """eNPS segmentado (por área ou cargo)"""
    segmento: str
    segmento_id: Optional[UUID] = None
    enps: float
    promotores: int
    passivos: int
    detratores: int
    total: int


class EnpsPorArea(EnpsPorSegmento):
    """eNPS por área"""
    pass


class EnpsPorCargo(EnpsPorSegmento):
    """eNPS por cargo"""
    pass


class FavorabilidadeDimensao(BaseModel):
    """Favorabilidade de uma dimensão"""
    dimensao: str
    dimensao_id: UUID
    favoravel: int
    neutro: int
    desfavoravel: int
    total: int
    favorabilidade_pct: float = Field(..., description="% de respostas favoráveis (4-5)")


class FavorabilidadePorSegmento(BaseModel):
    """Favorabilidade segmentada"""
    segmento: str
    dimensao: str
    favorabilidade_pct: float
    favoravel: int
    total: int


class InsightBaixoEnps(BaseModel):
    """Insights de funcionários com baixo eNPS"""
    funcionario_id: UUID
    funcionario_nome: str
    cargo: str
    area: str
    enps: int
    comentario_enps: Optional[str] = None
    data_avaliacao: date
    dimensoes_baixas: List[str] = Field(default_factory=list, description="Dimensões com score <= 2")


class TendenciaEnps(BaseModel):
    """Tendência temporal de eNPS"""
    periodo: str  # YYYY-MM
    enps: float
    total_avaliacoes: int
