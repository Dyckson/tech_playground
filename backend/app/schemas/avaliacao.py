"""
Schemas de Avaliação e Dimensões
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID

from .funcionario import FuncionarioResponse


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
