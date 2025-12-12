"""
Funcionário Service
"""
from typing import List, Optional
from uuid import UUID
from app.repositories.funcionario_repository import FuncionarioRepository
from app.schemas.schemas import (
    FuncionarioResponse,
    FuncionarioPaginada,
    FuncionarioCreate,
    FiltroOpcao
)


class FuncionarioService:
    
    def __init__(self):
        self.repository = FuncionarioRepository()
    
    def listar_funcionarios(
        self,
        empresa_id: UUID,
        page: int = 1,
        page_size: int = 20,
        areas: Optional[List[UUID]] = None,
        cargos: Optional[List[UUID]] = None,
        localidades: Optional[List[UUID]] = None
    ) -> FuncionarioPaginada:
        """Lista funcionários com paginação e filtros"""
        funcionarios_data, total = self.repository.get_funcionarios_paginado(
            empresa_id=empresa_id,
            page=page,
            page_size=page_size,
            areas=areas,
            cargos=cargos,
            localidades=localidades
        )
        
        funcionarios = [
            FuncionarioResponse(**func) for func in funcionarios_data
        ]
        
        return FuncionarioPaginada(
            items=funcionarios,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size
        )
    
    def buscar_funcionarios(
        self,
        empresa_id: UUID,
        termo: str,
        page: int = 1,
        page_size: int = 20,
        areas: Optional[List[UUID]] = None,
        cargos: Optional[List[UUID]] = None,
        localidades: Optional[List[UUID]] = None
    ) -> FuncionarioPaginada:
        """Busca funcionários por nome ou email"""
        funcionarios_data, total = self.repository.buscar_funcionarios(
            empresa_id=empresa_id,
            termo_busca=termo,
            page=page,
            page_size=page_size,
            areas=areas,
            cargos=cargos,
            localidades=localidades
        )
        
        funcionarios = [
            FuncionarioResponse(**func) for func in funcionarios_data
        ]
        
        return FuncionarioPaginada(
            items=funcionarios,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size
        )
    
    def obter_funcionario(self, funcionario_id: UUID) -> Optional[FuncionarioResponse]:
        """Obtém funcionário por ID"""
        funcionario_data = self.repository.get_funcionario_by_id(funcionario_id)
        
        if funcionario_data:
            return FuncionarioResponse(**funcionario_data)
        return None
    
    def obter_filtros_disponiveis(self, empresa_id: UUID) -> dict:
        """Obtém todas as opções de filtro disponíveis"""
        areas = self.repository.get_areas_unicas(empresa_id)
        cargos = self.repository.get_cargos_unicos(empresa_id)
        localidades = self.repository.get_localidades_unicas(empresa_id)
        
        return {
            "areas": [FiltroOpcao(**a) for a in areas],
            "cargos": [FiltroOpcao(**c) for c in cargos],
            "localidades": [FiltroOpcao(**l) for l in localidades]
        }
    
    def criar_funcionario(self, funcionario: FuncionarioCreate) -> str:
        """Cria novo funcionário"""
        return self.repository.criar_funcionario(funcionario.model_dump())
