"""
Pydantic Schemas
Modelos de validação para API
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID


# ========== HIERARQUIA ==========

class EmpresaBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255)


class EmpresaCreate(EmpresaBase):
    pass


class EmpresaResponse(EmpresaBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class DiretoriaResponse(BaseModel):
    id: UUID
    empresa_id: UUID
    nome: str
    created_at: datetime


class GerenciaResponse(BaseModel):
    id: UUID
    diretoria_id: UUID
    nome: str
    created_at: datetime


class CoordenacaoResponse(BaseModel):
    id: UUID
    gerencia_id: UUID
    nome: str
    created_at: datetime


class AreaDetalheResponse(BaseModel):
    id: UUID
    coordenacao_id: UUID
    nome_area_detalhe: str
    ativo: bool


class HierarquiaCompleta(BaseModel):
    """Hierarquia completa de uma área"""
    empresa: str
    diretoria: str
    gerencia: str
    coordenacao: str
    area: str
    empresa_id: UUID
    diretoria_id: UUID
    gerencia_id: UUID
    coordenacao_id: UUID
    area_id: UUID


# ========== FUNCIONÁRIO ==========

class FuncionarioBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    email_corporativo: Optional[EmailStr] = None
    funcao: str = Field(..., description="profissional ou gestor")


class FuncionarioCreate(FuncionarioBase):
    empresa_id: UUID
    area_detalhe_id: UUID
    cargo_id: UUID
    genero_id: UUID
    geracao_id: UUID
    tempo_empresa_id: UUID
    localidade_id: UUID


class FuncionarioResponse(FuncionarioBase):
    id: UUID
    empresa_id: UUID
    area_detalhe_id: UUID
    cargo_id: UUID
    genero_id: UUID
    geracao_id: UUID
    tempo_empresa_id: UUID
    localidade_id: UUID
    ativo: bool
    created_at: datetime
    
    # Dados expandidos (joins)
    cargo_nome: Optional[str] = None
    area_nome: Optional[str] = None
    localidade_nome: Optional[str] = None
    genero_nome: Optional[str] = None
    geracao_nome: Optional[str] = None
    tempo_empresa_nome: Optional[str] = None
    
    class Config:
        from_attributes = True


class FuncionarioPaginada(BaseModel):
    """Resposta paginada de funcionários"""
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[FuncionarioResponse]


# ========== AVALIAÇÃO ==========

class DimensaoRespostaBase(BaseModel):
    dimensao_avaliacao_id: UUID
    valor_resposta: int = Field(..., ge=0, le=10)
    comentario: Optional[str] = None


class DimensaoRespostaCreate(DimensaoRespostaBase):
    pass


class DimensaoRespostaResponse(DimensaoRespostaBase):
    id: UUID
    avaliacao_id: UUID
    dimensao_nome: Optional[str] = None
    dimensao_numero: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class AvaliacaoBase(BaseModel):
    funcionario_id: UUID
    data_resposta: date


class AvaliacaoCreate(AvaliacaoBase):
    dimensoes: List[DimensaoRespostaCreate] = Field(..., min_length=7, max_length=7)


class AvaliacaoResponse(AvaliacaoBase):
    id: UUID
    enps_calculado: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class AvaliacaoCompleta(AvaliacaoResponse):
    """Avaliação com todas as dimensões"""
    dimensoes: List[DimensaoRespostaResponse]
    funcionario: Optional[FuncionarioResponse] = None


# ========== ANALYTICS ==========

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


# ========== FILTROS E AGREGAÇÕES ==========

class AreaUnica(BaseModel):
    """Área única para filtro"""
    id: UUID
    nome: str


class CargoUnico(BaseModel):
    """Cargo único para filtro"""
    id: UUID
    nome: str


class LocalidadeUnica(BaseModel):
    """Localidade única para filtro"""
    id: UUID
    nome: str


class ContagemPorArea(BaseModel):
    """Contagem de funcionários por área"""
    area_id: UUID
    area_nome: str
    total_funcionarios: int


class FiltroOpcao(BaseModel):
    """Opção genérica para filtros"""
    id: UUID
    nome: str


# ========== HEALTH CHECK ==========

class HealthCheck(BaseModel):
    """Health check da API"""
    status: str
    environment: str
    version: str
    database: str
    timestamp: datetime
