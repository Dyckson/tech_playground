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
                        WHEN rd.valor_resposta <= 4 THEN 'detratores'
                        WHEN rd.valor_resposta = 5 THEN 'neutros'
                        WHEN rd.valor_resposta >= 6 THEN 'promotores'
                    END as categoria
                FROM resposta_dimensao rd
                JOIN avaliacao av ON av.id_avaliacao = rd.id_avaliacao
                JOIN dimensao_avaliacao da ON da.id_dimensao_avaliacao = rd.id_dimensao_avaliacao
                {empresa_filter}
                AND (da.nome_dimensao = 'Expectativa de Permanência (eNPS)' 
                     OR da.nome_dimensao = 'Expectativa de Permanência')
            )
            SELECT 
                categoria,
                COUNT(*) as quantidade,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentual
            FROM enps_data
            WHERE categoria IS NOT NULL
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

    def get_employee_detailed_analytics(self, funcionario_id: UUID) -> dict:
        """
        Retorna analytics detalhado de um funcionário individual
        Inclui: scores por dimensão, comparação com médias, histórico, comentários
        """
        # 1. Scores do funcionário por dimensão (última avaliação)
        query_scores = """
            SELECT 
                da.nome_dimensao as dimensao,
                rd.valor_resposta as score,
                da.tipo_escala,
                rd.comentario
            FROM resposta_dimensao rd
            JOIN dimensao_avaliacao da ON da.id_dimensao_avaliacao = rd.id_dimensao_avaliacao
            JOIN avaliacao av ON av.id_avaliacao = rd.id_avaliacao
            WHERE av.id_funcionario = %s
            ORDER BY da.ordem_exibicao
        """
        employee_scores = self.execute_query(query_scores, (str(funcionario_id),))

        # 2. Médias da empresa (todas dimensões)
        query_company_avg = """
            SELECT 
                da.nome_dimensao as dimensao,
                ROUND(AVG(rd.valor_resposta), 2) as score_medio
            FROM dimensao_avaliacao da
            LEFT JOIN resposta_dimensao rd ON rd.id_dimensao_avaliacao = da.id_dimensao_avaliacao
            LEFT JOIN avaliacao av ON av.id_avaliacao = rd.id_avaliacao
            JOIN funcionario f ON f.id_funcionario = av.id_funcionario
            WHERE f.ativo = true
            GROUP BY da.nome_dimensao, da.ordem_exibicao
            ORDER BY da.ordem_exibicao
        """
        company_averages = self.execute_query(query_company_avg, ())

        # 3. Médias da área do funcionário
        query_area_avg = """
            SELECT 
                da.nome_dimensao as dimensao,
                ROUND(AVG(rd.valor_resposta), 2) as score_medio
            FROM dimensao_avaliacao da
            LEFT JOIN resposta_dimensao rd ON rd.id_dimensao_avaliacao = da.id_dimensao_avaliacao
            LEFT JOIN avaliacao av ON av.id_avaliacao = rd.id_avaliacao
            JOIN funcionario f ON f.id_funcionario = av.id_funcionario
            WHERE f.ativo = true 
            AND f.id_area_detalhe = (
                SELECT id_area_detalhe FROM funcionario WHERE id_funcionario = %s
            )
            GROUP BY da.nome_dimensao, da.ordem_exibicao
            ORDER BY da.ordem_exibicao
        """
        area_averages = self.execute_query(query_area_avg, (str(funcionario_id),))

        # 4. Histórico de avaliações (se houver múltiplas)
        query_history = """
            SELECT 
                av.data_avaliacao,
                av.periodo_avaliacao,
                av.comentario_geral,
                COUNT(rd.id_resposta_dimensao) as total_dimensoes,
                ROUND(AVG(rd.valor_resposta), 2) as score_medio_geral
            FROM avaliacao av
            LEFT JOIN resposta_dimensao rd ON rd.id_avaliacao = av.id_avaliacao
            WHERE av.id_funcionario = %s
            GROUP BY av.id_avaliacao, av.data_avaliacao, av.periodo_avaliacao, av.comentario_geral
            ORDER BY av.data_avaliacao DESC
        """
        history = self.execute_query(query_history, (str(funcionario_id),))

        # 5. Comentários detalhados por dimensão
        query_comments = """
            SELECT 
                da.nome_dimensao as dimensao,
                rd.valor_resposta as score,
                rd.comentario,
                av.data_avaliacao
            FROM resposta_dimensao rd
            JOIN dimensao_avaliacao da ON da.id_dimensao_avaliacao = rd.id_dimensao_avaliacao
            JOIN avaliacao av ON av.id_avaliacao = rd.id_avaliacao
            WHERE av.id_funcionario = %s
            AND rd.comentario IS NOT NULL
            AND rd.comentario != ''
            ORDER BY av.data_avaliacao DESC, da.ordem_exibicao
        """
        comments = self.execute_query(query_comments, (str(funcionario_id),))

        return {
            "employee_scores": employee_scores,
            "company_averages": company_averages,
            "area_averages": area_averages,
            "history": history,
            "comments": comments,
        }

    def get_areas_scores_comparison(self, empresa_id: UUID | None = None) -> list[dict]:
        """
        Retorna scores médios por dimensão para cada área
        Usado para comparação entre áreas/departamentos
        """
        empresa_filter = ""
        params = []

        if empresa_id:
            empresa_filter = "AND d.id_empresa = %s"
            params.append(str(empresa_id))

        query = f"""
            SELECT 
                ad.id_area_detalhe,
                ad.nome_area_detalhe as area_nome,
                co.nome_coordenacao,
                g.nome_gerencia,
                d.nome_diretoria,
                da.nome_dimensao as dimensao,
                ROUND(AVG(rd.valor_resposta), 2) as score_medio,
                COUNT(DISTINCT f.id_funcionario) as total_funcionarios,
                COUNT(rd.id_resposta_dimensao) as total_respostas
            FROM area_detalhe ad
            JOIN coordenacao co ON co.id_coordenacao = ad.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = co.id_gerencia
            JOIN diretoria d ON d.id_diretoria = g.id_diretoria
            JOIN funcionario f ON f.id_area_detalhe = ad.id_area_detalhe AND f.ativo = true
            JOIN avaliacao av ON av.id_funcionario = f.id_funcionario
            JOIN resposta_dimensao rd ON rd.id_avaliacao = av.id_avaliacao
            JOIN dimensao_avaliacao da ON da.id_dimensao_avaliacao = rd.id_dimensao_avaliacao
            WHERE 1=1 {empresa_filter}
            GROUP BY ad.id_area_detalhe, ad.nome_area_detalhe, co.nome_coordenacao, 
                     g.nome_gerencia, d.nome_diretoria, da.nome_dimensao, da.ordem_exibicao
            ORDER BY ad.nome_area_detalhe, da.ordem_exibicao
        """

        return self.execute_query(query, tuple(params) if params else ())

    def get_areas_enps_comparison(self, empresa_id: UUID | None = None) -> list[dict]:
        """
        Retorna eNPS por área para comparação entre departamentos
        """
        empresa_filter = ""
        params = []

        if empresa_id:
            empresa_filter = "AND d.id_empresa = %s"
            params.append(str(empresa_id))

        query = f"""
            WITH area_enps AS (
                SELECT 
                    ad.id_area_detalhe,
                    ad.nome_area_detalhe as area_nome,
                    co.nome_coordenacao,
                    g.nome_gerencia,
                    d.nome_diretoria,
                    rd.valor_resposta,
                    CASE 
                        WHEN rd.valor_resposta <= 4 THEN 'detratores'
                        WHEN rd.valor_resposta = 5 THEN 'neutros'
                        WHEN rd.valor_resposta >= 6 THEN 'promotores'
                    END as categoria,
                    COUNT(DISTINCT f.id_funcionario) as total_funcionarios
                FROM area_detalhe ad
                JOIN coordenacao co ON co.id_coordenacao = ad.id_coordenacao
                JOIN gerencia g ON g.id_gerencia = co.id_gerencia
                JOIN diretoria d ON d.id_diretoria = g.id_diretoria
                JOIN funcionario f ON f.id_area_detalhe = ad.id_area_detalhe AND f.ativo = true
                JOIN avaliacao av ON av.id_funcionario = f.id_funcionario
                JOIN resposta_dimensao rd ON rd.id_avaliacao = av.id_avaliacao
                JOIN dimensao_avaliacao da ON da.id_dimensao_avaliacao = rd.id_dimensao_avaliacao
                WHERE (da.nome_dimensao = 'Expectativa de Permanência (eNPS)' 
                       OR da.nome_dimensao = 'Expectativa de Permanência')
                {empresa_filter}
                GROUP BY ad.id_area_detalhe, ad.nome_area_detalhe, co.nome_coordenacao,
                         g.nome_gerencia, d.nome_diretoria, rd.valor_resposta, categoria
            )
            SELECT 
                id_area_detalhe,
                area_nome,
                nome_coordenacao,
                nome_gerencia,
                nome_diretoria,
                MAX(total_funcionarios) as total_funcionarios,
                SUM(CASE WHEN categoria = 'promotores' THEN 1 ELSE 0 END) as promotores,
                SUM(CASE WHEN categoria = 'neutros' THEN 1 ELSE 0 END) as neutros,
                SUM(CASE WHEN categoria = 'detratores' THEN 1 ELSE 0 END) as detratores,
                ROUND(
                    (SUM(CASE WHEN categoria = 'promotores' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) - 
                    (SUM(CASE WHEN categoria = 'detratores' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)),
                    2
                ) as enps_score
            FROM area_enps
            GROUP BY id_area_detalhe, area_nome, nome_coordenacao, nome_gerencia, nome_diretoria
            ORDER BY enps_score DESC
        """

        return self.execute_query(query, tuple(params) if params else ())

    def get_area_detailed_metrics(self, area_id: UUID) -> dict:
        """
        Retorna métricas detalhadas de uma área específica
        Inclui: scores por dimensão, eNPS, distribuição de funcionários
        """
        # 1. Informações básicas da área
        query_area_info = """
            SELECT 
                ad.id_area_detalhe,
                ad.nome_area_detalhe as area_nome,
                ad.sigla_area,
                ad.responsavel_nome,
                ad.responsavel_email,
                co.nome_coordenacao,
                g.nome_gerencia,
                d.nome_diretoria,
                COUNT(DISTINCT f.id_funcionario) as total_funcionarios
            FROM area_detalhe ad
            JOIN coordenacao co ON co.id_coordenacao = ad.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = co.id_gerencia
            JOIN diretoria d ON d.id_diretoria = g.id_diretoria
            LEFT JOIN funcionario f ON f.id_area_detalhe = ad.id_area_detalhe AND f.ativo = true
            WHERE ad.id_area_detalhe = %s
            GROUP BY ad.id_area_detalhe, ad.nome_area_detalhe, ad.sigla_area, 
                     ad.responsavel_nome, ad.responsavel_email, co.nome_coordenacao,
                     g.nome_gerencia, d.nome_diretoria
        """
        area_info = self.execute_one(query_area_info, (str(area_id),))

        # 2. Scores por dimensão
        query_scores = """
            SELECT 
                da.nome_dimensao as dimensao,
                da.tipo_escala,
                ROUND(AVG(rd.valor_resposta), 2) as score_medio,
                COUNT(rd.id_resposta_dimensao) as total_respostas
            FROM dimensao_avaliacao da
            LEFT JOIN resposta_dimensao rd ON rd.id_dimensao_avaliacao = da.id_dimensao_avaliacao
            LEFT JOIN avaliacao av ON av.id_avaliacao = rd.id_avaliacao
            LEFT JOIN funcionario f ON f.id_funcionario = av.id_funcionario
            WHERE f.id_area_detalhe = %s AND f.ativo = true
            GROUP BY da.nome_dimensao, da.tipo_escala, da.ordem_exibicao
            ORDER BY da.ordem_exibicao
        """
        scores = self.execute_query(query_scores, (str(area_id),))

        # 3. Distribuição eNPS
        query_enps = """
            SELECT 
                CASE 
                    WHEN rd.valor_resposta <= 4 THEN 'detratores'
                    WHEN rd.valor_resposta = 5 THEN 'neutros'
                    WHEN rd.valor_resposta >= 6 THEN 'promotores'
                END as categoria,
                COUNT(*) as quantidade
            FROM resposta_dimensao rd
            JOIN avaliacao av ON av.id_avaliacao = rd.id_avaliacao
            JOIN funcionario f ON f.id_funcionario = av.id_funcionario
            JOIN dimensao_avaliacao da ON da.id_dimensao_avaliacao = rd.id_dimensao_avaliacao
            WHERE f.id_area_detalhe = %s 
            AND f.ativo = true
            AND (da.nome_dimensao = 'Expectativa de Permanência (eNPS)' 
                 OR da.nome_dimensao = 'Expectativa de Permanência')
            GROUP BY categoria
        """
        enps_dist = self.execute_query(query_enps, (str(area_id),))

        return {
            "area_info": area_info,
            "scores_por_dimensao": scores,
            "enps_distribution": enps_dist,
        }

    def get_areas_scores_comparison(self, empresa_id: UUID | None = None) -> list[dict]:
        """
        Retorna scores médios por dimensão para cada área
        Usado para comparação entre áreas (Task 7 - Visualização 1)
        """
        empresa_filter = ""
        params = []

        if empresa_id:
            empresa_filter = """
                AND d.id_empresa = %s
            """
            params.append(str(empresa_id))

        query = f"""
            SELECT 
                ad.id_area_detalhe,
                ad.nome_area_detalhe as area_nome,
                co.nome_coordenacao,
                g.nome_gerencia,
                dir.nome_diretoria,
                da.nome_dimensao as dimensao,
                ROUND(AVG(rd.valor_resposta), 2) as score_medio,
                COUNT(rd.id_resposta_dimensao) as total_respostas,
                COUNT(DISTINCT f.id_funcionario) as total_funcionarios
            FROM area_detalhe ad
            JOIN coordenacao co ON co.id_coordenacao = ad.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = co.id_gerencia
            JOIN diretoria dir ON dir.id_diretoria = g.id_diretoria
            JOIN funcionario f ON f.id_area_detalhe = ad.id_area_detalhe AND f.ativo = true
            LEFT JOIN avaliacao av ON av.id_funcionario = f.id_funcionario
            LEFT JOIN resposta_dimensao rd ON rd.id_avaliacao = av.id_avaliacao
            LEFT JOIN dimensao_avaliacao da ON da.id_dimensao_avaliacao = rd.id_dimensao_avaliacao
            WHERE ad.ativo = true
            {empresa_filter}
            GROUP BY ad.id_area_detalhe, ad.nome_area_detalhe, co.nome_coordenacao, 
                     g.nome_gerencia, dir.nome_diretoria, da.nome_dimensao, da.ordem_exibicao
            ORDER BY ad.nome_area_detalhe, da.ordem_exibicao
        """

        return self.execute_query(query, tuple(params) if params else ())

    def get_areas_enps_comparison(self, empresa_id: UUID | None = None) -> list[dict]:
        """
        Retorna eNPS segmentado por área
        Usado para comparação de engajamento entre áreas (Task 7 - Visualização 2)
        """
        empresa_filter = ""
        params = []

        if empresa_id:
            empresa_filter = """
                AND d.id_empresa = %s
            """
            params.append(str(empresa_id))

        query = f"""
            WITH enps_by_area AS (
                SELECT 
                    ad.id_area_detalhe,
                    ad.nome_area_detalhe as area_nome,
                    co.nome_coordenacao,
                    g.nome_gerencia,
                    dir.nome_diretoria,
                    rd.valor_resposta,
                    CASE 
                        WHEN rd.valor_resposta <= 4 THEN 'detratores'
                        WHEN rd.valor_resposta = 5 THEN 'neutros'
                        WHEN rd.valor_resposta >= 6 THEN 'promotores'
                    END as categoria
                FROM area_detalhe ad
                JOIN coordenacao co ON co.id_coordenacao = ad.id_coordenacao
                JOIN gerencia g ON g.id_gerencia = co.id_gerencia
                JOIN diretoria dir ON dir.id_diretoria = g.id_diretoria
                JOIN funcionario f ON f.id_area_detalhe = ad.id_area_detalhe AND f.ativo = true
                LEFT JOIN avaliacao av ON av.id_funcionario = f.id_funcionario
                LEFT JOIN resposta_dimensao rd ON rd.id_avaliacao = av.id_avaliacao
                LEFT JOIN dimensao_avaliacao da ON da.id_dimensao_avaliacao = rd.id_dimensao_avaliacao
                WHERE ad.ativo = true
                AND (da.nome_dimensao = 'Expectativa de Permanência (eNPS)' 
                     OR da.nome_dimensao = 'Expectativa de Permanência')
                {empresa_filter}
            )
            SELECT 
                id_area_detalhe,
                area_nome,
                nome_coordenacao,
                nome_gerencia,
                nome_diretoria,
                COUNT(CASE WHEN categoria = 'promotores' THEN 1 END) as promotores,
                COUNT(CASE WHEN categoria = 'neutros' THEN 1 END) as neutros,
                COUNT(CASE WHEN categoria = 'detratores' THEN 1 END) as detratores,
                ROUND(COUNT(CASE WHEN categoria = 'promotores' THEN 1 END) * 100.0 / 
                      NULLIF(COUNT(categoria), 0), 2) as promotores_percentual,
                ROUND(COUNT(CASE WHEN categoria = 'neutros' THEN 1 END) * 100.0 / 
                      NULLIF(COUNT(categoria), 0), 2) as neutros_percentual,
                ROUND(COUNT(CASE WHEN categoria = 'detratores' THEN 1 END) * 100.0 / 
                      NULLIF(COUNT(categoria), 0), 2) as detratores_percentual,
                COUNT(categoria) as total_respostas
            FROM enps_by_area
            WHERE categoria IS NOT NULL
            GROUP BY id_area_detalhe, area_nome, nome_coordenacao, nome_gerencia, nome_diretoria
            ORDER BY area_nome
        """

        return self.execute_query(query, tuple(params) if params else ())

    def get_area_detailed_metrics(self, area_id: UUID) -> dict:
        """
        Retorna métricas detalhadas de uma área específica
        Incluindo scores por dimensão, eNPS, e comparação com empresa
        """
        # 1. Scores por dimensão da área
        query_area_scores = """
            SELECT 
                da.nome_dimensao as dimensao,
                ROUND(AVG(rd.valor_resposta), 2) as score_medio,
                COUNT(rd.id_resposta_dimensao) as total_respostas,
                COUNT(DISTINCT f.id_funcionario) as total_funcionarios
            FROM dimensao_avaliacao da
            LEFT JOIN resposta_dimensao rd ON rd.id_dimensao_avaliacao = da.id_dimensao_avaliacao
            LEFT JOIN avaliacao av ON av.id_avaliacao = rd.id_avaliacao
            LEFT JOIN funcionario f ON f.id_funcionario = av.id_funcionario
            WHERE f.id_area_detalhe = %s AND f.ativo = true
            GROUP BY da.nome_dimensao, da.ordem_exibicao
            ORDER BY da.ordem_exibicao
        """
        area_scores = self.execute_query(query_area_scores, (str(area_id),))

        # 2. Médias da empresa para comparação
        query_company_avg = """
            SELECT 
                da.nome_dimensao as dimensao,
                ROUND(AVG(rd.valor_resposta), 2) as score_medio
            FROM dimensao_avaliacao da
            LEFT JOIN resposta_dimensao rd ON rd.id_dimensao_avaliacao = da.id_dimensao_avaliacao
            LEFT JOIN avaliacao av ON av.id_avaliacao = rd.id_avaliacao
            JOIN funcionario f ON f.id_funcionario = av.id_funcionario
            WHERE f.ativo = true
            GROUP BY da.nome_dimensao, da.ordem_exibicao
            ORDER BY da.ordem_exibicao
        """
        company_averages = self.execute_query(query_company_avg, ())

        # 3. eNPS da área
        query_enps = """
            SELECT 
                COUNT(CASE WHEN rd.valor_resposta <= 4 THEN 1 END) as detratores,
                COUNT(CASE WHEN rd.valor_resposta = 5 THEN 1 END) as neutros,
                COUNT(CASE WHEN rd.valor_resposta >= 6 THEN 1 END) as promotores
            FROM funcionario f
            LEFT JOIN avaliacao av ON av.id_funcionario = f.id_funcionario
            LEFT JOIN resposta_dimensao rd ON rd.id_avaliacao = av.id_avaliacao
            LEFT JOIN dimensao_avaliacao da ON da.id_dimensao_avaliacao = rd.id_dimensao_avaliacao
            WHERE f.id_area_detalhe = %s 
            AND f.ativo = true
            AND (da.nome_dimensao = 'Expectativa de Permanência (eNPS)' 
                 OR da.nome_dimensao = 'Expectativa de Permanência')
        """
        enps_data = self.execute_query(query_enps, (str(area_id),))

        # 4. Informações da área
        query_area_info = """
            SELECT 
                ad.nome_area_detalhe as area_nome,
                co.nome_coordenacao,
                g.nome_gerencia,
                dir.nome_diretoria,
                COUNT(DISTINCT f.id_funcionario) as total_funcionarios
            FROM area_detalhe ad
            JOIN coordenacao co ON co.id_coordenacao = ad.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = co.id_gerencia
            JOIN diretoria dir ON dir.id_diretoria = g.id_diretoria
            LEFT JOIN funcionario f ON f.id_area_detalhe = ad.id_area_detalhe AND f.ativo = true
            WHERE ad.id_area_detalhe = %s
            GROUP BY ad.nome_area_detalhe, co.nome_coordenacao, g.nome_gerencia, dir.nome_diretoria
        """
        area_info = self.execute_query(query_area_info, (str(area_id),))

        return {
            "area_info": area_info[0] if area_info else None,
            "area_scores": area_scores,
            "company_averages": company_averages,
            "enps": enps_data[0] if enps_data else {"promotores": 0, "neutros": 0, "detratores": 0},
        }
