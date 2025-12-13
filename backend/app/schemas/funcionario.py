"""
Schemas de Funcionário
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


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
