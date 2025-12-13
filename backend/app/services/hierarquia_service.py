"""
Hierarquia Service
Lógica de negócio para estrutura organizacional
"""

from uuid import UUID

from app.repositories.hierarquia_repository import HierarquiaRepository
from app.schemas.schemas import ContagemPorArea, EmpresaResponse, HierarquiaCompleta


class HierarquiaService:
    """Serviço para gerenciar hierarquia organizacional"""

    def __init__(self):
        self.repository = HierarquiaRepository()

    def get_all_empresas(self) -> list[EmpresaResponse]:
        """Lista todas as empresas"""
        empresas = self.repository.get_all_empresas()
        return [EmpresaResponse(**empresa) for empresa in empresas]

    def get_empresa(self, empresa_id: UUID) -> EmpresaResponse | None:
        """Busca empresa por ID"""
        empresa = self.repository.get_empresa_by_id(empresa_id)
        return EmpresaResponse(**empresa) if empresa else None

    def get_arvore_hierarquica(self, empresa_id: UUID) -> list[dict]:
        """
        Retorna árvore hierárquica estruturada
        Organiza em formato de árvore aninhada
        """
        nodes = self.repository.get_arvore_hierarquica(empresa_id)

        if not nodes:
            return []

        arvore = {}

        for node in nodes:
            dir_id = str(node["diretoria_id"])
            ger_id = str(node["gerencia_id"])
            coord_id = str(node["coordenacao_id"])

            if dir_id not in arvore:
                arvore[dir_id] = {
                    "id": node["diretoria_id"],
                    "nome": node["diretoria_nome"],
                    "tipo": "diretoria",
                    "gerencias": {},
                }

            if ger_id not in arvore[dir_id]["gerencias"]:
                arvore[dir_id]["gerencias"][ger_id] = {
                    "id": node["gerencia_id"],
                    "nome": node["gerencia_nome"],
                    "tipo": "gerencia",
                    "coordenacoes": {},
                }

            if coord_id not in arvore[dir_id]["gerencias"][ger_id]["coordenacoes"]:
                arvore[dir_id]["gerencias"][ger_id]["coordenacoes"][coord_id] = {
                    "id": node["coordenacao_id"],
                    "nome": node["coordenacao_nome"],
                    "tipo": "coordenacao",
                    "areas": [],
                }

            if node["area_id"]:
                arvore[dir_id]["gerencias"][ger_id]["coordenacoes"][coord_id]["areas"].append(
                    {"id": node["area_id"], "nome": node["area_nome"], "tipo": "area"}
                )

        # Converter dicionários em listas
        result = []
        for diretoria in arvore.values():
            diretoria["gerencias"] = list(diretoria["gerencias"].values())
            for gerencia in diretoria["gerencias"]:
                gerencia["coordenacoes"] = list(gerencia["coordenacoes"].values())
            result.append(diretoria)

        return result

    def get_areas(self, empresa_id: UUID) -> list[HierarquiaCompleta]:
        """Lista todas as áreas com hierarquia completa"""
        areas = self.repository.get_areas_by_empresa(empresa_id)

        return [
            HierarquiaCompleta(
                empresa=area["empresa_nome"],
                diretoria=area["diretoria_nome"],
                gerencia=area["gerencia_nome"],
                coordenacao=area["coordenacao_nome"],
                area=area["nome"],
                empresa_id=area["empresa_id"],
                diretoria_id=area["diretoria_id"],
                gerencia_id=area["gerencia_id"],
                coordenacao_id=area["coordenacao_id"],
                area_id=area["id"],
            )
            for area in areas
        ]

    def get_area_hierarquia(self, area_id: UUID) -> HierarquiaCompleta | None:
        """Busca hierarquia completa de uma área"""
        area = self.repository.get_area_hierarquia(area_id)

        if not area:
            return None

        return HierarquiaCompleta(**area)

    def get_contagem_funcionarios(self, empresa_id: UUID) -> list[ContagemPorArea]:
        """Retorna contagem de funcionários por área"""
        contagens = self.repository.count_funcionarios_by_area(empresa_id)

        return [
            ContagemPorArea(area_id=c["area_id"], area_nome=c["area_nome"], total_funcionarios=c["total_funcionarios"])
            for c in contagens
        ]
