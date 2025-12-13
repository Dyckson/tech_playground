"""
Hierarquia Repository
Acesso a dados da estrutura organizacional
"""

from uuid import UUID

from app.repositories.base_repository import BaseRepository


class HierarquiaRepository(BaseRepository):
    """Repositório para consultas de hierarquia organizacional"""

    def get_all_empresas(self) -> list[dict]:
        """Retorna todas as empresas"""
        query = """
            SELECT id_empresa as id, nome_empresa as nome, created_at
            FROM empresa
            WHERE ativo = true
            ORDER BY nome_empresa
        """
        return self.execute_query(query)

    def get_empresa_by_id(self, empresa_id: UUID) -> dict | None:
        """Busca empresa por ID"""
        query = """
            SELECT id_empresa as id, nome_empresa as nome, created_at
            FROM empresa
            WHERE id_empresa = %s AND ativo = true
        """
        return self.execute_one(query, (str(empresa_id),))

    def get_arvore_hierarquica(self, empresa_id: UUID) -> list[dict]:
        """
        Retorna árvore hierárquica completa de uma empresa
        empresa -> diretoria -> gerencia -> coordenacao -> area
        """
        query = """
            SELECT 
                e.id_empresa as empresa_id,
                e.nome_empresa as empresa_nome,
                d.id_diretoria as diretoria_id,
                d.nome_diretoria as diretoria_nome,
                g.id_gerencia as gerencia_id,
                g.nome_gerencia as gerencia_nome,
                c.id_coordenacao as coordenacao_id,
                c.nome_coordenacao as coordenacao_nome,
                a.id_area_detalhe as area_id,
                a.nome_area_detalhe as area_nome
            FROM empresa e
            LEFT JOIN diretoria d ON d.id_empresa = e.id_empresa
            LEFT JOIN gerencia g ON g.id_diretoria = d.id_diretoria
            LEFT JOIN coordenacao c ON c.id_gerencia = g.id_gerencia
            LEFT JOIN area_detalhe a ON a.id_coordenacao = c.id_coordenacao
            WHERE e.id_empresa = %s AND e.ativo = true
            ORDER BY d.nome_diretoria, g.nome_gerencia, c.nome_coordenacao, a.nome_area_detalhe
        """
        return self.execute_query(query, (str(empresa_id),))

    def get_areas_by_empresa(self, empresa_id: UUID) -> list[dict]:
        """Retorna todas as áreas de uma empresa com hierarquia completa"""
        query = """
            SELECT 
                a.id_area_detalhe as id,
                a.nome_area_detalhe as nome,
                a.ativo,
                c.id_coordenacao as coordenacao_id,
                c.nome_coordenacao as coordenacao_nome,
                g.id_gerencia as gerencia_id,
                g.nome_gerencia as gerencia_nome,
                d.id_diretoria as diretoria_id,
                d.nome_diretoria as diretoria_nome,
                e.id_empresa as empresa_id,
                e.nome_empresa as empresa_nome
            FROM area_detalhe a
            JOIN coordenacao c ON c.id_coordenacao = a.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = c.id_gerencia
            JOIN diretoria d ON d.id_diretoria = g.id_diretoria
            JOIN empresa e ON e.id_empresa = d.id_empresa
            WHERE e.id_empresa = %s AND a.ativo = true
            ORDER BY a.nome_area_detalhe
        """
        return self.execute_query(query, (str(empresa_id),))

    def get_area_hierarquia(self, area_id: UUID) -> dict | None:
        """Retorna hierarquia completa de uma área específica"""
        query = """
            SELECT 
                e.id_empresa as empresa_id,
                e.nome_empresa as empresa,
                d.id_diretoria as diretoria_id,
                d.nome_diretoria as diretoria,
                g.id_gerencia as gerencia_id,
                g.nome_gerencia as gerencia,
                c.id_coordenacao as coordenacao_id,
                c.nome_coordenacao as coordenacao,
                a.id_area_detalhe as area_id,
                a.nome_area_detalhe as area
            FROM area_detalhe a
            JOIN coordenacao c ON c.id_coordenacao = a.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = c.id_gerencia
            JOIN diretoria d ON d.id_diretoria = g.id_diretoria
            JOIN empresa e ON e.id_empresa = d.id_empresa
            WHERE a.id_area_detalhe = %s
        """
        return self.execute_one(query, (str(area_id),))

    def get_diretorias_by_empresa(self, empresa_id: UUID) -> list[dict]:
        """Retorna todas as diretorias de uma empresa"""
        query = """
            SELECT id_diretoria as id, nome_diretoria as nome, id_empresa as empresa_id, created_at
            FROM diretoria
            WHERE id_empresa = %s AND ativo = true
            ORDER BY nome_diretoria
        """
        return self.execute_query(query, (str(empresa_id),))

    def get_gerencias_by_diretoria(self, diretoria_id: UUID) -> list[dict]:
        """Retorna todas as gerências de uma diretoria"""
        query = """
            SELECT id_gerencia as id, nome_gerencia as nome, id_diretoria as diretoria_id, created_at
            FROM gerencia
            WHERE id_diretoria = %s AND ativo = true
            ORDER BY nome_gerencia
        """
        return self.execute_query(query, (str(diretoria_id),))

    def get_coordenacoes_by_gerencia(self, gerencia_id: UUID) -> list[dict]:
        """Retorna todas as coordenações de uma gerência"""
        query = """
            SELECT id_coordenacao as id, nome_coordenacao as nome, id_gerencia as gerencia_id, created_at
            FROM coordenacao
            WHERE id_gerencia = %s AND ativo = true
            ORDER BY nome_coordenacao
        """
        return self.execute_query(query, (str(gerencia_id),))

    def count_funcionarios_by_area(self, empresa_id: UUID) -> list[dict]:
        """Conta funcionários por área"""
        query = """
            SELECT 
                a.id_area_detalhe as area_id,
                a.nome_area_detalhe as area_nome,
                COUNT(f.id_funcionario) as total_funcionarios
            FROM area_detalhe a
            JOIN coordenacao c ON c.id_coordenacao = a.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = c.id_gerencia
            JOIN diretoria d ON d.id_diretoria = g.id_diretoria
            LEFT JOIN funcionario f ON f.id_area_detalhe = a.id_area_detalhe AND f.ativo = true
            WHERE d.id_empresa = %s
            GROUP BY a.id_area_detalhe, a.nome_area_detalhe
            ORDER BY total_funcionarios DESC, a.nome_area_detalhe
        """
        return self.execute_query(query, (str(empresa_id),))
