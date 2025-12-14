"""
Funcionário Repository
"""

from uuid import UUID

from app.repositories.base_repository import BaseRepository


class FuncionarioRepository(BaseRepository):
    def get_funcionarios_paginado(
        self,
        empresa_id: UUID | None,
        page: int,
        page_size: int,
        areas: list[UUID] | None = None,
        cargos: list[UUID] | None = None,
        localidades: list[UUID] | None = None,
        tempo_casa: list[UUID] | None = None,
        score_min: float | None = None,
        score_max: float | None = None,
        enps_status: str | None = None,
        order_by: str = "nome",
        order_dir: str = "asc",
    ) -> tuple[list[dict], int]:
        """Retorna funcionários com paginação e filtros"""

        params_list = []
        empresa_filter = ""
        area_filter = ""
        cargo_filter = ""
        localidade_filter = ""
        tempo_casa_filter = ""
        score_filter = ""
        enps_filter = ""

        if empresa_id:
            empresa_filter = " AND d.id_empresa = %s"
            params_list.append(str(empresa_id))

        if areas:
            area_filter = " AND f.id_area_detalhe IN (" + ",".join(["%s"] * len(areas)) + ")"
            params_list.extend([str(area) for area in areas])
        if cargos:
            cargo_filter = " AND f.id_cargo IN (" + ",".join(["%s"] * len(cargos)) + ")"
            params_list.extend([str(cargo) for cargo in cargos])
        if localidades:
            localidade_filter = " AND f.id_localidade IN (" + ",".join(["%s"] * len(localidades)) + ")"
            params_list.extend([str(localidade) for localidade in localidades])
        
        if tempo_casa:
            tempo_casa_filter = " AND f.id_tempo_empresa_catgo IN (" + ",".join(["%s"] * len(tempo_casa)) + ")"
            params_list.extend([str(tc) for tc in tempo_casa])

        # Filtros de score e eNPS requerem subquery com avaliações
        score_subquery = ""
        enps_subquery = ""
        
        if score_min is not None or score_max is not None or enps_status:
            score_subquery = """
                LEFT JOIN (
                    SELECT 
                        av.id_funcionario,
                        AVG((r1.valor_resposta + r2.valor_resposta + r3.valor_resposta + 
                             r4.valor_resposta + r5.valor_resposta + r6.valor_resposta + 
                             r7.valor_resposta) / 7.0) as score_medio_geral,
                        AVG(r7.valor_resposta) as expectativa_permanencia
                    FROM avaliacao av
                    JOIN resposta_dimensao r1 ON r1.id_avaliacao = av.id_avaliacao AND r1.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Interesse no Cargo')
                    JOIN resposta_dimensao r2 ON r2.id_avaliacao = av.id_avaliacao AND r2.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Contribuição')
                    JOIN resposta_dimensao r3 ON r3.id_avaliacao = av.id_avaliacao AND r3.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Aprendizado e Desenvolvimento')
                    JOIN resposta_dimensao r4 ON r4.id_avaliacao = av.id_avaliacao AND r4.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Feedback')
                    JOIN resposta_dimensao r5 ON r5.id_avaliacao = av.id_avaliacao AND r5.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Interação com Gestor')
                    JOIN resposta_dimensao r6 ON r6.id_avaliacao = av.id_avaliacao AND r6.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Clareza sobre Possibilidades de Carreira')
                    JOIN resposta_dimensao r7 ON r7.id_avaliacao = av.id_avaliacao AND r7.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Expectativa de Permanência')
                    GROUP BY av.id_funcionario
                ) scores ON scores.id_funcionario = f.id_funcionario
            """
            
            if score_min is not None:
                score_filter += " AND scores.score_medio_geral >= %s"
                params_list.append(score_min)
            if score_max is not None:
                score_filter += " AND scores.score_medio_geral <= %s"
                params_list.append(score_max)
            
            if enps_status:
                if enps_status == "promotor":
                    enps_filter = " AND scores.expectativa_permanencia >= 6"
                elif enps_status == "neutro":
                    enps_filter = " AND scores.expectativa_permanencia = 5"
                elif enps_status == "detrator":
                    enps_filter = " AND scores.expectativa_permanencia <= 4"

        count_query = f"""
            SELECT COUNT(*)
            FROM funcionario f
            {score_subquery}
            JOIN area_detalhe a ON a.id_area_detalhe = f.id_area_detalhe
            JOIN coordenacao co ON co.id_coordenacao = a.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = co.id_gerencia
            JOIN diretoria d ON d.id_diretoria = g.id_diretoria
            WHERE f.ativo = true{empresa_filter}{area_filter}{cargo_filter}{localidade_filter}{tempo_casa_filter}{score_filter}{enps_filter}
        """

        total = self.execute_scalar(count_query, tuple(params_list))

        limit, offset = self.build_pagination(page, page_size)
        params_list.extend([limit, offset])
        
        # Mapear order_by para colunas reais
        order_map = {
            "nome": "f.nome_funcionario",
            "cargo": "c.nome_cargo",
            "area": "a.nome_area_detalhe",
            "tempo": "t.nome_tempo_empresa",
            "score": "scores.score_medio_geral",
        }
        order_column = order_map.get(order_by, "f.nome_funcionario")
        order_direction = "DESC" if order_dir.lower() == "desc" else "ASC"

        query = f"""
            SELECT
                f.id_funcionario as id,
                f.nome_funcionario as nome,
                f.email,
                f.email_corporativo,
                f.tipo_contratacao as funcao,
                d.id_empresa as empresa_id,
                f.id_area_detalhe as area_detalhe_id,
                f.id_cargo as cargo_id,
                f.id_genero_catgo as genero_id,
                f.id_geracao_catgo as geracao_id,
                f.id_tempo_empresa_catgo as tempo_empresa_id,
                f.id_localidade as localidade_id,
                f.ativo,
                f.created_at,
                c.nome_cargo as cargo_nome,
                a.nome_area_detalhe as area_nome,
                l.nome_localidade as localidade_nome,
                gen.nome_genero as genero_nome,
                ger.nome_geracao as geracao_nome,
                t.nome_tempo_empresa as tempo_empresa_nome,
                COALESCE(scores.score_medio_geral, 0) as score_medio_geral,
                COALESCE(scores.expectativa_permanencia, 0) as expectativa_permanencia
            FROM funcionario f
            LEFT JOIN (
                SELECT 
                    av.id_funcionario,
                    AVG((r1.valor_resposta + r2.valor_resposta + r3.valor_resposta + 
                         r4.valor_resposta + r5.valor_resposta + r6.valor_resposta + 
                         r7.valor_resposta) / 7.0) as score_medio_geral,
                    AVG(r7.valor_resposta) as expectativa_permanencia
                FROM avaliacao av
                JOIN resposta_dimensao r1 ON r1.id_avaliacao = av.id_avaliacao AND r1.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Interesse no Cargo')
                JOIN resposta_dimensao r2 ON r2.id_avaliacao = av.id_avaliacao AND r2.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Contribuição')
                JOIN resposta_dimensao r3 ON r3.id_avaliacao = av.id_avaliacao AND r3.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Aprendizado e Desenvolvimento')
                JOIN resposta_dimensao r4 ON r4.id_avaliacao = av.id_avaliacao AND r4.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Feedback')
                JOIN resposta_dimensao r5 ON r5.id_avaliacao = av.id_avaliacao AND r5.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Interação com Gestor')
                JOIN resposta_dimensao r6 ON r6.id_avaliacao = av.id_avaliacao AND r6.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Clareza sobre Possibilidades de Carreira')
                JOIN resposta_dimensao r7 ON r7.id_avaliacao = av.id_avaliacao AND r7.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Expectativa de Permanência')
                GROUP BY av.id_funcionario
            ) scores ON scores.id_funcionario = f.id_funcionario
            JOIN area_detalhe a ON a.id_area_detalhe = f.id_area_detalhe
            JOIN coordenacao co ON co.id_coordenacao = a.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = co.id_gerencia
            JOIN diretoria d ON d.id_diretoria = g.id_diretoria
            LEFT JOIN cargo c ON c.id_cargo = f.id_cargo
            LEFT JOIN localidade l ON l.id_localidade = f.id_localidade
            LEFT JOIN genero_catgo gen ON gen.id_genero_catgo = f.id_genero_catgo
            LEFT JOIN geracao_catgo ger ON ger.id_geracao_catgo = f.id_geracao_catgo
            LEFT JOIN tempo_empresa_catgo t ON t.id_tempo_empresa_catgo = f.id_tempo_empresa_catgo
            WHERE f.ativo = true{empresa_filter}{area_filter}{cargo_filter}{localidade_filter}{tempo_casa_filter}{score_filter}{enps_filter}
            ORDER BY {order_column} {order_direction}
            LIMIT %s OFFSET %s
        """

        results = self.execute_query(query, tuple(params_list))
        return results, total

    def buscar_funcionarios(
        self,
        empresa_id: UUID | None,
        termo_busca: str,
        page: int,
        page_size: int,
        areas: list[UUID] | None = None,
        cargos: list[UUID] | None = None,
        localidades: list[UUID] | None = None,
        tempo_casa: list[UUID] | None = None,
        score_min: float | None = None,
        score_max: float | None = None,
        enps_status: str | None = None,
        order_by: str = "nome",
        order_dir: str = "asc",
    ) -> tuple[list[dict], int]:
        """Busca funcionários por nome ou email com filtros avançados"""

        params_list = []
        empresa_filter = ""
        area_filter = ""
        cargo_filter = ""
        localidade_filter = ""
        tempo_casa_filter = ""
        score_filter = ""
        enps_filter = ""

        if empresa_id:
            empresa_filter = " AND d.id_empresa = %s"
            params_list.append(str(empresa_id))

        if areas:
            area_filter = " AND f.id_area_detalhe IN (" + ",".join(["%s"] * len(areas)) + ")"
            params_list.extend([str(area) for area in areas])
        if cargos:
            cargo_filter = " AND f.id_cargo IN (" + ",".join(["%s"] * len(cargos)) + ")"
            params_list.extend([str(cargo) for cargo in cargos])
        if localidades:
            localidade_filter = " AND f.id_localidade IN (" + ",".join(["%s"] * len(localidades)) + ")"
            params_list.extend([str(localidade) for localidade in localidades])
        
        if tempo_casa:
            tempo_casa_filter = " AND f.id_tempo_empresa_catgo IN (" + ",".join(["%s"] * len(tempo_casa)) + ")"
            params_list.extend([str(tc) for tc in tempo_casa])

        # Sempre incluir subquery de scores para retornar métricas
        score_subquery = """
            LEFT JOIN (
                SELECT 
                    av.id_funcionario,
                    AVG((r1.valor_resposta + r2.valor_resposta + r3.valor_resposta + 
                         r4.valor_resposta + r5.valor_resposta + r6.valor_resposta + 
                         r7.valor_resposta) / 7.0) as score_medio_geral,
                    AVG(r7.valor_resposta) as expectativa_permanencia
                FROM avaliacao av
                JOIN resposta_dimensao r1 ON r1.id_avaliacao = av.id_avaliacao AND r1.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Interesse no Cargo')
                JOIN resposta_dimensao r2 ON r2.id_avaliacao = av.id_avaliacao AND r2.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Contribuição')
                JOIN resposta_dimensao r3 ON r3.id_avaliacao = av.id_avaliacao AND r3.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Aprendizado e Desenvolvimento')
                JOIN resposta_dimensao r4 ON r4.id_avaliacao = av.id_avaliacao AND r4.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Feedback')
                JOIN resposta_dimensao r5 ON r5.id_avaliacao = av.id_avaliacao AND r5.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Interação com Gestor')
                JOIN resposta_dimensao r6 ON r6.id_avaliacao = av.id_avaliacao AND r6.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Clareza sobre Possibilidades de Carreira')
                JOIN resposta_dimensao r7 ON r7.id_avaliacao = av.id_avaliacao AND r7.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Expectativa de Permanência')
                GROUP BY av.id_funcionario
            ) scores ON scores.id_funcionario = f.id_funcionario
        """
        
        # Aplicar filtros condicionais sobre os scores
        if score_min is not None:
            score_filter += " AND scores.score_medio_geral >= %s"
            params_list.append(score_min)
        if score_max is not None:
            score_filter += " AND scores.score_medio_geral <= %s"
            params_list.append(score_max)
        
        if enps_status:
            if enps_status == "promotor":
                enps_filter = " AND scores.expectativa_permanencia >= 6"
            elif enps_status == "neutro":
                enps_filter = " AND scores.expectativa_permanencia = 5"
            elif enps_status == "detrator":
                enps_filter = " AND scores.expectativa_permanencia <= 4"

        search_pattern = f"%{termo_busca}%"
        params_list.append(search_pattern)
        params_list.append(search_pattern)
        params_list.append(search_pattern)

        count_query = f"""
            SELECT COUNT(*)
            FROM funcionario f
            {score_subquery}
            JOIN area_detalhe a ON a.id_area_detalhe = f.id_area_detalhe
            JOIN coordenacao co ON co.id_coordenacao = a.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = co.id_gerencia
            JOIN diretoria d ON d.id_diretoria = g.id_diretoria
            LEFT JOIN cargo c ON c.id_cargo = f.id_cargo
            WHERE f.ativo = true{empresa_filter}{area_filter}{cargo_filter}{localidade_filter}{tempo_casa_filter}{score_filter}{enps_filter}
            AND (f.nome_funcionario ILIKE %s OR f.email ILIKE %s OR c.nome_cargo ILIKE %s)
        """

        total = self.execute_scalar(count_query, tuple(params_list))

        limit, offset = self.build_pagination(page, page_size)
        params_list.extend([limit, offset])
        
        # Mapear order_by para colunas reais
        order_map = {
            "nome": "f.nome_funcionario",
            "cargo": "c.nome_cargo",
            "area": "a.nome_area_detalhe",
            "tempo": "t.nome_tempo_empresa",
            "score": "scores.score_medio_geral",
        }
        order_column = order_map.get(order_by, "f.nome_funcionario")
        order_direction = "DESC" if order_dir.lower() == "desc" else "ASC"

        query = f"""
            SELECT
                f.id_funcionario as id,
                f.nome_funcionario as nome,
                f.email,
                f.email_corporativo,
                f.tipo_contratacao as funcao,
                d.id_empresa as empresa_id,
                f.id_area_detalhe as area_detalhe_id,
                f.id_cargo as cargo_id,
                f.id_genero_catgo as genero_id,
                f.id_geracao_catgo as geracao_id,
                f.id_tempo_empresa_catgo as tempo_empresa_id,
                f.id_localidade as localidade_id,
                f.ativo,
                f.created_at,
                c.nome_cargo as cargo_nome,
                a.nome_area_detalhe as area_nome,
                l.nome_localidade as localidade_nome,
                gen.nome_genero as genero_nome,
                ger.nome_geracao as geracao_nome,
                t.nome_tempo_empresa as tempo_empresa_nome,
                scores.score_medio_geral,
                scores.expectativa_permanencia
            FROM funcionario f
            LEFT JOIN (
                SELECT 
                    av.id_funcionario,
                    AVG((r1.valor_resposta + r2.valor_resposta + r3.valor_resposta + 
                         r4.valor_resposta + r5.valor_resposta + r6.valor_resposta + 
                         r7.valor_resposta) / 7.0) as score_medio_geral,
                    AVG(r7.valor_resposta) as expectativa_permanencia
                FROM avaliacao av
                JOIN resposta_dimensao r1 ON r1.id_avaliacao = av.id_avaliacao AND r1.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Interesse no Cargo')
                JOIN resposta_dimensao r2 ON r2.id_avaliacao = av.id_avaliacao AND r2.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Contribuição')
                JOIN resposta_dimensao r3 ON r3.id_avaliacao = av.id_avaliacao AND r3.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Aprendizado e Desenvolvimento')
                JOIN resposta_dimensao r4 ON r4.id_avaliacao = av.id_avaliacao AND r4.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Feedback')
                JOIN resposta_dimensao r5 ON r5.id_avaliacao = av.id_avaliacao AND r5.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Interação com Gestor')
                JOIN resposta_dimensao r6 ON r6.id_avaliacao = av.id_avaliacao AND r6.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Clareza sobre Possibilidades de Carreira')
                JOIN resposta_dimensao r7 ON r7.id_avaliacao = av.id_avaliacao AND r7.id_dimensao_avaliacao = (SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE nome_dimensao = 'Expectativa de Permanência')
                GROUP BY av.id_funcionario
            ) scores ON scores.id_funcionario = f.id_funcionario
            JOIN area_detalhe a ON a.id_area_detalhe = f.id_area_detalhe
            JOIN coordenacao co ON co.id_coordenacao = a.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = co.id_gerencia
            JOIN diretoria d ON d.id_diretoria = g.id_diretoria
            LEFT JOIN cargo c ON c.id_cargo = f.id_cargo
            LEFT JOIN localidade l ON l.id_localidade = f.id_localidade
            LEFT JOIN genero_catgo gen ON gen.id_genero_catgo = f.id_genero_catgo
            LEFT JOIN geracao_catgo ger ON ger.id_geracao_catgo = f.id_geracao_catgo
            LEFT JOIN tempo_empresa_catgo t ON t.id_tempo_empresa_catgo = f.id_tempo_empresa_catgo
            WHERE f.ativo = true{empresa_filter}{area_filter}{cargo_filter}{localidade_filter}{tempo_casa_filter}{score_filter}{enps_filter}
            AND (f.nome_funcionario ILIKE %s OR f.email ILIKE %s OR c.nome_cargo ILIKE %s)
            ORDER BY {order_column} {order_direction}
            LIMIT %s OFFSET %s
        """

        results = self.execute_query(query, tuple(params_list))
        return results, total

    def get_funcionario_by_id(self, funcionario_id: UUID) -> dict | None:
        """Busca funcionário por ID"""
        query = """
            SELECT
                f.id_funcionario as id,
                f.nome_funcionario as nome,
                f.email,
                f.email_corporativo,
                f.tipo_contratacao as funcao,
                d.id_empresa as empresa_id,
                f.id_area_detalhe as area_detalhe_id,
                f.id_cargo as cargo_id,
                f.id_genero_catgo as genero_id,
                f.id_geracao_catgo as geracao_id,
                f.id_tempo_empresa_catgo as tempo_empresa_id,
                f.id_localidade as localidade_id,
                f.ativo,
                f.created_at,
                c.nome_cargo as cargo_nome,
                a.nome_area_detalhe as area_nome,
                l.nome_localidade as localidade_nome,
                gen.nome_genero as genero_nome,
                ger.nome_geracao as geracao_nome,
                t.nome_tempo_empresa as tempo_empresa_nome
            FROM funcionario f
            JOIN area_detalhe a ON a.id_area_detalhe = f.id_area_detalhe
            JOIN coordenacao co ON co.id_coordenacao = a.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = co.id_gerencia
            JOIN diretoria d ON d.id_diretoria = g.id_diretoria
            LEFT JOIN cargo c ON c.id_cargo = f.id_cargo
            LEFT JOIN localidade l ON l.id_localidade = f.id_localidade
            LEFT JOIN genero_catgo gen ON gen.id_genero_catgo = f.id_genero_catgo
            LEFT JOIN geracao_catgo ger ON ger.id_geracao_catgo = f.id_geracao_catgo
            LEFT JOIN tempo_empresa_catgo t ON t.id_tempo_empresa_catgo = f.id_tempo_empresa_catgo
            WHERE f.id_funcionario = %s
        """
        return self.execute_one(query, (str(funcionario_id),))

    def get_areas_unicas(self, empresa_id: UUID | None) -> list[dict]:
        """Retorna áreas únicas da empresa"""
        if empresa_id:
            query = """
                SELECT DISTINCT
                    a.id_area_detalhe as id,
                    a.nome_area_detalhe as nome
                FROM area_detalhe a
                JOIN coordenacao c ON c.id_coordenacao = a.id_coordenacao
                JOIN gerencia g ON g.id_gerencia = c.id_gerencia
                JOIN diretoria d ON d.id_diretoria = g.id_diretoria
                WHERE d.id_empresa = %s AND a.ativo = true
                ORDER BY a.nome_area_detalhe
            """
            return self.execute_query(query, (str(empresa_id),))
        query = """
                SELECT DISTINCT
                    a.id_area_detalhe as id,
                    a.nome_area_detalhe as nome
                FROM area_detalhe a
                WHERE a.ativo = true
                ORDER BY a.nome_area_detalhe
            """
        return self.execute_query(query)

    def get_cargos_unicos(self, empresa_id: UUID | None) -> list[dict]:
        """Retorna cargos únicos usados na empresa"""
        if empresa_id:
            query = """
                SELECT DISTINCT
                    c.id_cargo as id,
                    c.nome_cargo as nome
                FROM cargo c
                JOIN funcionario f ON f.id_cargo = c.id_cargo
                JOIN area_detalhe a ON a.id_area_detalhe = f.id_area_detalhe
                JOIN coordenacao co ON co.id_coordenacao = a.id_coordenacao
                JOIN gerencia g ON g.id_gerencia = co.id_gerencia
                JOIN diretoria d ON d.id_diretoria = g.id_diretoria
                WHERE d.id_empresa = %s AND f.ativo = true
                ORDER BY c.nome_cargo
            """
            return self.execute_query(query, (str(empresa_id),))
        query = """
                SELECT DISTINCT
                    c.id_cargo as id,
                    c.nome_cargo as nome
                FROM cargo c
                ORDER BY c.nome_cargo
            """
        return self.execute_query(query)

    def get_localidades_unicas(self, empresa_id: UUID | None) -> list[dict]:
        """Retorna localidades únicas usadas na empresa"""
        if empresa_id:
            query = """
                SELECT DISTINCT
                    l.id_localidade as id,
                    l.nome_localidade as nome
                FROM localidade l
                JOIN funcionario f ON f.id_localidade = l.id_localidade
                JOIN area_detalhe a ON a.id_area_detalhe = f.id_area_detalhe
                JOIN coordenacao co ON co.id_coordenacao = a.id_coordenacao
                JOIN gerencia g ON g.id_gerencia = co.id_gerencia
                JOIN diretoria d ON d.id_diretoria = g.id_diretoria
                WHERE d.id_empresa = %s AND f.ativo = true
                ORDER BY l.nome_localidade
            """
            return self.execute_query(query, (str(empresa_id),))
        query = """
                SELECT DISTINCT
                    l.id_localidade as id,
                    l.nome_localidade as nome
                FROM localidade l
                ORDER BY l.nome_localidade
            """
        return self.execute_query(query)

    def criar_funcionario(self, dados: dict) -> str:
        """Cria novo funcionário"""
        query = """
            INSERT INTO funcionario (
                nome_funcionario, email, email_corporativo, tipo_contratacao,
                id_area_detalhe, id_cargo,
                id_genero_catgo, id_geracao_catgo,
                id_tempo_empresa_catgo, id_localidade,
                data_admissao
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE)
            RETURNING id_funcionario as id
        """
        params = (
            dados["nome"],
            dados["email"],
            dados.get("email_corporativo"),
            dados.get("funcao"),
            str(dados["area_detalhe_id"]),
            str(dados["cargo_id"]),
            str(dados["genero_id"]),
            str(dados["geracao_id"]),
            str(dados["tempo_empresa_id"]),
            str(dados["localidade_id"]),
        )
        return self.execute_insert(query, params)
