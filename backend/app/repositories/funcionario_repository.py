"""
Funcionário Repository
"""
from typing import List, Dict, Optional, Tuple
from uuid import UUID
from app.repositories.base_repository import BaseRepository


class FuncionarioRepository(BaseRepository):
    
    def get_funcionarios_paginado(
        self,
        empresa_id: UUID,
        page: int,
        page_size: int,
        areas: Optional[List[UUID]] = None,
        cargos: Optional[List[UUID]] = None,
        localidades: Optional[List[UUID]] = None
    ) -> Tuple[List[Dict], int]:
        """Retorna funcionários com paginação e filtros"""
        
        params_list = [str(empresa_id)]
        area_filter = ""
        cargo_filter = ""
        localidade_filter = ""
        
        if areas:
            area_filter = " AND f.id_area_detalhe IN (" + ",".join(["%s"] * len(areas)) + ")"
            params_list.extend([str(a) for a in areas])
        if cargos:
            cargo_filter = " AND f.id_cargo IN (" + ",".join(["%s"] * len(cargos)) + ")"
            params_list.extend([str(c) for c in cargos])
        if localidades:
            localidade_filter = " AND f.id_localidade IN (" + ",".join(["%s"] * len(localidades)) + ")"
            params_list.extend([str(l) for l in localidades])
        
        count_query = f"""
            SELECT COUNT(*)
            FROM funcionario f
            JOIN area_detalhe a ON a.id_area_detalhe = f.id_area_detalhe
            JOIN coordenacao co ON co.id_coordenacao = a.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = co.id_gerencia
            JOIN diretoria d ON d.id_diretoria = g.id_diretoria
            WHERE d.id_empresa = %s AND f.ativo = true
            {area_filter}{cargo_filter}{localidade_filter}
        """
        
        total = self.execute_scalar(count_query, tuple(params_list))
        
        limit, offset = self.build_pagination(page, page_size)
        params_list.extend([limit, offset])
        
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
            WHERE d.id_empresa = %s AND f.ativo = true
            {area_filter}{cargo_filter}{localidade_filter}
            ORDER BY f.nome_funcionario
            LIMIT %s OFFSET %s
        """
        
        results = self.execute_query(query, tuple(params_list))
        return results, total
    
    def buscar_funcionarios(
        self,
        empresa_id: UUID,
        termo_busca: str,
        page: int,
        page_size: int,
        areas: Optional[List[UUID]] = None,
        cargos: Optional[List[UUID]] = None,
        localidades: Optional[List[UUID]] = None
    ) -> Tuple[List[Dict], int]:
        """Busca funcionários por nome ou email"""
        
        params_list = [str(empresa_id)]
        area_filter = ""
        cargo_filter = ""
        localidade_filter = ""
        
        if areas:
            area_filter = " AND f.id_area_detalhe IN (" + ",".join(["%s"] * len(areas)) + ")"
            params_list.extend([str(a) for a in areas])
        if cargos:
            cargo_filter = " AND f.id_cargo IN (" + ",".join(["%s"] * len(cargos)) + ")"
            params_list.extend([str(c) for c in cargos])
        if localidades:
            localidade_filter = " AND f.id_localidade IN (" + ",".join(["%s"] * len(localidades)) + ")"
            params_list.extend([str(l) for l in localidades])
        
        search_pattern = f"%{termo_busca}%"
        params_list.append(search_pattern)
        params_list.append(search_pattern)
        
        count_query = f"""
            SELECT COUNT(*)
            FROM funcionario f
            JOIN area_detalhe a ON a.id_area_detalhe = f.id_area_detalhe
            JOIN coordenacao co ON co.id_coordenacao = a.id_coordenacao
            JOIN gerencia g ON g.id_gerencia = co.id_gerencia
            JOIN diretoria d ON d.id_diretoria = g.id_diretoria
            WHERE d.id_empresa = %s AND f.ativo = true
            {area_filter}{cargo_filter}{localidade_filter}
            AND (f.nome_funcionario ILIKE %s OR f.email ILIKE %s)
        """
        
        total = self.execute_scalar(count_query, tuple(params_list))
        
        limit, offset = self.build_pagination(page, page_size)
        params_list.extend([limit, offset])
        
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
            WHERE d.id_empresa = %s AND f.ativo = true
            {area_filter}{cargo_filter}{localidade_filter}
            AND (f.nome_funcionario ILIKE %s OR f.email ILIKE %s)
            ORDER BY f.nome_funcionario
            LIMIT %s OFFSET %s
        """
        
        results = self.execute_query(query, tuple(params_list))
        return results, total
    
    def get_funcionario_by_id(self, funcionario_id: UUID) -> Optional[Dict]:
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
    
    def get_areas_unicas(self, empresa_id: UUID) -> List[Dict]:
        """Retorna áreas únicas da empresa"""
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
    
    def get_cargos_unicos(self, empresa_id: UUID) -> List[Dict]:
        """Retorna cargos únicos usados na empresa"""
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
    
    def get_localidades_unicas(self, empresa_id: UUID) -> List[Dict]:
        """Retorna localidades únicas usadas na empresa"""
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
    
    def criar_funcionario(self, dados: Dict) -> str:
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
            dados['nome'],
            dados['email'],
            dados.get('email_corporativo'),
            dados.get('funcao'),
            str(dados['area_detalhe_id']),
            str(dados['cargo_id']),
            str(dados['genero_id']),
            str(dados['geracao_id']),
            str(dados['tempo_empresa_id']),
            str(dados['localidade_id'])
        )
        return self.execute_insert(query, params)
