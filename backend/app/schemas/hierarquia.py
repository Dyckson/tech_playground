"""
Schemas de Hierarquia Organizacional
Empresa → Diretoria → Gerência → Coordenação → Área
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


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
