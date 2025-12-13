"""
Testes de integridade dos dados
Valida a integridade dos dados reais no banco de dados
"""
import pytest


class TestDataCounts:
    """Testes de contagem de registros"""
    
    def test_total_funcionarios(self, db_cursor):
        """Verifica se há pelo menos 500 funcionários"""
        db_cursor.execute("SELECT COUNT(*) as count FROM funcionario")
        result = db_cursor.fetchone()
        
        assert result['count'] >= 500, "Deve haver pelo menos 500 funcionários"
    
    def test_total_empresas(self, db_cursor):
        """Verifica se há empresas cadastradas"""
        db_cursor.execute("SELECT COUNT(*) as count FROM empresa")
        result = db_cursor.fetchone()
        
        assert result['count'] > 0, "Deve haver pelo menos uma empresa"
    
    def test_total_areas(self, db_cursor):
        """Verifica se há áreas cadastradas"""
        db_cursor.execute("SELECT COUNT(*) as count FROM area_detalhe")
        result = db_cursor.fetchone()
        
        assert result['count'] > 0, "Deve haver áreas cadastradas"
    
    def test_total_cargos(self, db_cursor):
        """Verifica se há cargos cadastrados"""
        db_cursor.execute("SELECT COUNT(*) as count FROM cargo")
        result = db_cursor.fetchone()
        
        assert result['count'] > 0, "Deve haver cargos cadastrados"


class TestDataIntegrity:
    """Testes de integridade referencial"""
    
    def test_todos_funcionarios_tem_area(self, db_cursor):
        """Verifica se todos os funcionários têm área"""
        db_cursor.execute("""
            SELECT COUNT(*) as count 
            FROM funcionario 
            WHERE id_area_detalhe IS NULL
        """)
        result = db_cursor.fetchone()
        
        assert result['count'] == 0, "Todos os funcionários devem ter área"
    
    def test_todos_funcionarios_tem_cargo(self, db_cursor):
        """Verifica se todos os funcionários têm cargo"""
        db_cursor.execute("""
            SELECT COUNT(*) as count 
            FROM funcionario 
            WHERE id_cargo IS NULL
        """)
        result = db_cursor.fetchone()
        
        assert result['count'] == 0, "Todos os funcionários devem ter cargo"
    
    def test_todos_funcionarios_tem_email_valido(self, db_cursor):
        """Verifica se todos os emails são válidos"""
        db_cursor.execute("""
            SELECT COUNT(*) as count 
            FROM funcionario 
            WHERE email IS NULL 
            OR email = '' 
            OR email NOT LIKE '%@%'
        """)
        result = db_cursor.fetchone()
        
        assert result['count'] == 0, "Todos os funcionários devem ter email válido"
    
    def test_emails_unicos(self, db_cursor):
        """Verifica se não há emails duplicados"""
        db_cursor.execute("""
            SELECT email, COUNT(*) as count 
            FROM funcionario 
            GROUP BY email 
            HAVING COUNT(*) > 1
        """)
        duplicates = db_cursor.fetchall()
        
        assert len(duplicates) == 0, f"Encontrados {len(duplicates)} emails duplicados"
    
    def test_todas_areas_tem_coordenacao(self, db_cursor):
        """Verifica se todas as áreas pertencem a uma coordenação"""
        db_cursor.execute("""
            SELECT COUNT(*) as count 
            FROM area_detalhe 
            WHERE id_coordenacao IS NULL
        """)
        result = db_cursor.fetchone()
        
        assert result['count'] == 0, "Todas as áreas devem ter coordenação"
    
    def test_foreign_keys_funcionario(self, db_cursor):
        """Verifica se todas as FKs de funcionário são válidas"""
        # Verifica id_area_detalhe
        db_cursor.execute("""
            SELECT COUNT(*) as count
            FROM funcionario f
            LEFT JOIN area_detalhe ad ON f.id_area_detalhe = ad.id_area_detalhe
            WHERE f.id_area_detalhe IS NOT NULL 
            AND ad.id_area_detalhe IS NULL
        """)
        result = db_cursor.fetchone()
        assert result['count'] == 0, "Todas as áreas devem existir"
        
        # Verifica id_cargo
        db_cursor.execute("""
            SELECT COUNT(*) as count
            FROM funcionario f
            LEFT JOIN cargo c ON f.id_cargo = c.id_cargo
            WHERE f.id_cargo IS NOT NULL 
            AND c.id_cargo IS NULL
        """)
        result = db_cursor.fetchone()
        assert result['count'] == 0, "Todos os cargos devem existir"


class TestDataDistribution:
    """Testes de distribuição de dados"""
    
    def test_funcionarios_distribuidos_por_empresa(self, db_cursor):
        """Verifica se funcionários estão distribuídos nas empresas"""
        db_cursor.execute("""
            SELECT 
                e.nome_empresa,
                COUNT(DISTINCT f.id_funcionario) as total_funcionarios
            FROM empresa e
            LEFT JOIN diretoria d ON e.id_empresa = d.id_empresa
            LEFT JOIN gerencia g ON d.id_diretoria = g.id_diretoria
            LEFT JOIN coordenacao c ON g.id_gerencia = c.id_gerencia
            LEFT JOIN area_detalhe ad ON c.id_coordenacao = ad.id_coordenacao
            LEFT JOIN funcionario f ON ad.id_area_detalhe = f.id_area_detalhe
            GROUP BY e.nome_empresa, e.id_empresa
            ORDER BY total_funcionarios DESC
        """)
        results = db_cursor.fetchall()
        
        assert len(results) > 0, "Deve haver empresas com funcionários"
        
        # Verifica se pelo menos uma empresa tem funcionários
        has_funcionarios = any(row['total_funcionarios'] > 0 for row in results)
        assert has_funcionarios, "Pelo menos uma empresa deve ter funcionários"
    
    def test_cargos_distribuidos(self, db_cursor):
        """Verifica distribuição de funcionários por cargo"""
        db_cursor.execute("""
            SELECT 
                c.nome_cargo,
                COUNT(*) as total
            FROM funcionario f
            INNER JOIN cargo c ON f.id_cargo = c.id_cargo
            GROUP BY c.nome_cargo
            ORDER BY total DESC
        """)
        results = db_cursor.fetchall()
        
        assert len(results) > 0, "Deve haver cargos com funcionários"
        
        # Verifica se há pelo menos 3 cargos diferentes
        assert len(results) >= 3, "Deve haver pelo menos 3 cargos diferentes"
    
    def test_areas_distribuidas(self, db_cursor):
        """Verifica distribuição de funcionários por área"""
        db_cursor.execute("""
            SELECT 
                ad.nome_area_detalhe,
                COUNT(*) as total
            FROM funcionario f
            INNER JOIN area_detalhe ad ON f.id_area_detalhe = ad.id_area_detalhe
            GROUP BY ad.nome_area_detalhe
            ORDER BY total DESC
        """)
        results = db_cursor.fetchall()
        
        assert len(results) > 0, "Deve haver áreas com funcionários"


class TestHierarchyIntegrity:
    """Testes de integridade da hierarquia organizacional"""
    
    def test_hierarquia_completa(self, db_cursor):
        """Verifica se a hierarquia está completa (empresa → diretoria → gerência → coordenação → área)"""
        db_cursor.execute("""
            SELECT 
                e.nome_empresa,
                d.nome_diretoria,
                g.nome_gerencia,
                c.nome_coordenacao,
                ad.nome_area_detalhe
            FROM empresa e
            INNER JOIN diretoria d ON e.id_empresa = d.id_empresa
            INNER JOIN gerencia g ON d.id_diretoria = g.id_diretoria
            INNER JOIN coordenacao c ON g.id_gerencia = c.id_gerencia
            INNER JOIN area_detalhe ad ON c.id_coordenacao = ad.id_coordenacao
            LIMIT 10
        """)
        results = db_cursor.fetchall()
        
        assert len(results) > 0, "Deve haver hierarquia completa"
        
        for row in results:
            assert row['nome_empresa'] is not None
            assert row['nome_diretoria'] is not None
            assert row['nome_gerencia'] is not None
            assert row['nome_coordenacao'] is not None
            assert row['nome_area_detalhe'] is not None
    
    def test_coordenacoes_tem_gerencia(self, db_cursor):
        """Verifica se todas as coordenações pertencem a uma gerência"""
        db_cursor.execute("""
            SELECT COUNT(*) as count
            FROM coordenacao
            WHERE id_gerencia IS NULL
        """)
        result = db_cursor.fetchone()
        
        assert result['count'] == 0, "Todas as coordenações devem ter gerência"
    
    def test_gerencias_tem_diretoria(self, db_cursor):
        """Verifica se todas as gerências pertencem a uma diretoria"""
        db_cursor.execute("""
            SELECT COUNT(*) as count
            FROM gerencia
            WHERE id_diretoria IS NULL
        """)
        result = db_cursor.fetchone()
        
        assert result['count'] == 0, "Todas as gerências devem ter diretoria"
    
    def test_diretorias_tem_empresa(self, db_cursor):
        """Verifica se todas as diretorias pertencem a uma empresa"""
        db_cursor.execute("""
            SELECT COUNT(*) as count
            FROM diretoria
            WHERE id_empresa IS NULL
        """)
        result = db_cursor.fetchone()
        
        assert result['count'] == 0, "Todas as diretorias devem ter empresa"


class TestAvaliacoesIntegrity:
    """Testes de integridade das avaliações"""
    
    def test_avaliacoes_tem_funcionario(self, db_cursor):
        """Verifica se todas as avaliações têm funcionário válido"""
        db_cursor.execute("""
            SELECT COUNT(*) as count
            FROM avaliacao a
            LEFT JOIN funcionario f ON a.id_funcionario = f.id_funcionario
            WHERE f.id_funcionario IS NULL
        """)
        result = db_cursor.fetchone()
        
        assert result['count'] == 0, "Todas as avaliações devem ter funcionário válido"
    
    def test_respostas_tem_avaliacao(self, db_cursor):
        """Verifica se todas as respostas pertencem a uma avaliação"""
        db_cursor.execute("""
            SELECT COUNT(*) as count
            FROM resposta_dimensao rd
            LEFT JOIN avaliacao a ON rd.id_avaliacao = a.id_avaliacao
            WHERE a.id_avaliacao IS NULL
        """)
        result = db_cursor.fetchone()
        
        assert result['count'] == 0, "Todas as respostas devem ter avaliação válida"
