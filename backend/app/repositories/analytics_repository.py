"""
Analytics Repository
Queries para análises e métricas
"""

from uuid import UUID

from app.repositories.base_repository import BaseRepository


class AnalyticsRepository(BaseRepository):
    def get_enps_distribution(self, empresa_id: UUID | None = None) -> dict:
        """
        Retorna distribuição eNPS (Promotores, Neutros, Detratores)
        eNPS é calculado da dimensão 7 (Recomendação)
        Escala: 0-6=Detratores, 7-8=Neutros, 9-10=Promotores
        """
        empresa_filter = ""
        params = []

        if empresa_id:
            empresa_filter = """
                JOIN funcionario f ON f.id_funcionario = av.id_funcionario
                JOIN area_detalhe ad ON ad.id_area_detalhe = f.id_area_detalhe
                JOIN coordenacao co ON co.id_coordenacao = ad.id_coordenacao
                JOIN gerencia g ON g.id_gerencia = co.id_gerencia
                JOIN diretoria d ON d.id_diretoria = g.id_diretoria
                WHERE d.id_empresa = %s AND f.ativo = true
            """
            params.append(str(empresa_id))
        else:
            empresa_filter = """
                JOIN funcionario f ON f.id_funcionario = av.id_funcionario
                WHERE f.ativo = true
            """

        query = f"""
            WITH enps_data AS (
                SELECT 
                    rd.valor_resposta,
                    CASE 
                        WHEN rd.valor_resposta <= 6 THEN 'detratores'
                        WHEN rd.valor_resposta BETWEEN 7 AND 8 THEN 'neutros'
                        WHEN rd.valor_resposta >= 9 THEN 'promotores'
                    END as categoria
                FROM resposta_dimensao rd
                JOIN avaliacao av ON av.id_avaliacao = rd.id_avaliacao
                JOIN dimensao_avaliacao da ON da.id_dimensao_avaliacao = rd.id_dimensao_avaliacao
                {empresa_filter}
                AND da.nome_dimensao = 'Expectativa de Permanência (eNPS)'
            )
            SELECT 
                categoria,
                COUNT(*) as quantidade,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentual
            FROM enps_data
            GROUP BY categoria
            ORDER BY 
                CASE categoria 
                    WHEN 'promotores' THEN 1 
                    WHEN 'neutros' THEN 2 
                    WHEN 'detratores' THEN 3 
                END
        """

        result = self.execute_query(query, tuple(params) if params else ())

        # Garantir que todas as categorias existam
        categorias = {row["categoria"]: row for row in result}
        
        return {
            "promotores": categorias.get("promotores", {"quantidade": 0, "percentual": 0})["quantidade"],
            "neutros": categorias.get("neutros", {"quantidade": 0, "percentual": 0})["quantidade"],
            "detratores": categorias.get("detratores", {"quantidade": 0, "percentual": 0})["quantidade"],
            "promotores_percentual": float(categorias.get("promotores", {"percentual": 0})["percentual"]),
            "neutros_percentual": float(categorias.get("neutros", {"percentual": 0})["percentual"]),
            "detratores_percentual": float(categorias.get("detratores", {"percentual": 0})["percentual"]),
        }

    def get_tenure_distribution(self, empresa_id: UUID | None = None) -> list[dict]:
        """
        Retorna distribuição de funcionários por tempo de casa
        """
        empresa_filter = ""
        params = []

        if empresa_id:
            empresa_filter = """
                JOIN area_detalhe ad ON ad.id_area_detalhe = f.id_area_detalhe
                JOIN coordenacao co ON co.id_coordenacao = ad.id_coordenacao
                JOIN gerencia g ON g.id_gerencia = co.id_gerencia
                JOIN diretoria d ON d.id_diretoria = g.id_diretoria
                WHERE d.id_empresa = %s AND f.ativo = true
            """
            params.append(str(empresa_id))
        else:
            empresa_filter = "WHERE f.ativo = true"

        query = f"""
            SELECT 
                tc.nome_tempo_empresa as categoria,
                COUNT(f.id_funcionario) as quantidade,
                ROUND(COUNT(f.id_funcionario) * 100.0 / SUM(COUNT(f.id_funcionario)) OVER (), 2) as percentual
            FROM funcionario f
            JOIN tempo_empresa_catgo tc ON tc.id_tempo_empresa_catgo = f.id_tempo_empresa_catgo
            {empresa_filter}
            GROUP BY tc.nome_tempo_empresa, tc.meses_min
            ORDER BY tc.meses_min
        """

        return self.execute_query(query, tuple(params) if params else ())

    def get_satisfaction_scores(self, empresa_id: UUID | None = None) -> list[dict]:
        """
        Retorna scores médios por dimensão de avaliação
        """
        empresa_filter = ""
        params = []

        if empresa_id:
            empresa_filter = """
                JOIN funcionario f ON f.id_funcionario = av.id_funcionario
                JOIN area_detalhe ad ON ad.id_area_detalhe = f.id_area_detalhe
                JOIN coordenacao co ON co.id_coordenacao = ad.id_coordenacao
                JOIN gerencia g ON g.id_gerencia = co.id_gerencia
                JOIN diretoria d ON d.id_diretoria = g.id_diretoria
                WHERE d.id_empresa = %s AND f.ativo = true
            """
            params.append(str(empresa_id))
        else:
            empresa_filter = """
                JOIN funcionario f ON f.id_funcionario = av.id_funcionario
                WHERE f.ativo = true
            """

        query = f"""
            SELECT 
                da.nome_dimensao as dimensao,
                ROUND(AVG(rd.valor_resposta), 2) as score_medio,
                COUNT(rd.id_resposta_dimensao) as total_respostas
            FROM dimensao_avaliacao da
            LEFT JOIN resposta_dimensao rd ON rd.id_dimensao_avaliacao = da.id_dimensao_avaliacao
            LEFT JOIN avaliacao av ON av.id_avaliacao = rd.id_avaliacao
            {empresa_filter}
            GROUP BY da.nome_dimensao, da.ordem_exibicao
            ORDER BY da.ordem_exibicao
        """

        return self.execute_query(query, tuple(params) if params else ())
