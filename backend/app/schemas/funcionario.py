"""
Schemas de Funcionário
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class FuncionarioBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    email_corporativo: EmailStr | None = None
    funcao: str | None = Field(None, description="profissional ou gestor")


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
    cargo_nome: str | None = None
    area_nome: str | None = None
    localidade_nome: str | None = None
    genero_nome: str | None = None
    geracao_nome: str | None = None
    tempo_empresa_nome: str | None = None
    
    # Scores e eNPS
    score_medio_geral: float | None = Field(None, description="Score médio geral das 7 dimensões (1-7)")
    expectativa_permanencia: float | None = Field(None, description="Score de expectativa de permanência (1-7)")

    class Config:
        from_attributes = True


class FuncionarioPaginada(BaseModel):
    """Resposta paginada de funcionários"""

    total: int
    page: int
    page_size: int
    total_pages: int
    items: list[FuncionarioResponse]
