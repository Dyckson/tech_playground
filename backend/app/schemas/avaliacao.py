"""
Schemas de Avaliação e Dimensões
"""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .funcionario import FuncionarioResponse


class DimensaoRespostaBase(BaseModel):
    dimensao_avaliacao_id: UUID
    valor_resposta: int = Field(..., ge=1, le=7, description="Escala de 1 a 7")
    comentario: str | None = None


class DimensaoRespostaCreate(DimensaoRespostaBase):
    pass


class DimensaoRespostaResponse(DimensaoRespostaBase):
    id: UUID
    avaliacao_id: UUID
    dimensao_nome: str | None = None
    dimensao_numero: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class AvaliacaoBase(BaseModel):
    funcionario_id: UUID
    data_resposta: date


class AvaliacaoCreate(AvaliacaoBase):
    dimensoes: list[DimensaoRespostaCreate] = Field(..., min_length=7, max_length=7)


class AvaliacaoResponse(AvaliacaoBase):
    id: UUID
    enps_calculado: float | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class AvaliacaoCompleta(AvaliacaoResponse):
    """Avaliação com todas as dimensões"""

    dimensoes: list[DimensaoRespostaResponse]
    funcionario: FuncionarioResponse | None = None
