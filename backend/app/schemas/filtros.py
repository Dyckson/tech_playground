"""
Schemas de Filtros e Agregações
"""
from pydantic import BaseModel
from uuid import UUID


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
