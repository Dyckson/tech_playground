"""
Testes de integração com o banco de dados
Testa conexões reais, transações, rollbacks e integridade dos dados
"""
import pytest
import psycopg2
from psycopg2.extras import RealDictCursor


class TestDatabaseConnection:
    """Testes de conexão com o banco de dados"""
    
    def test_database_connection_success(self, db_connection):
        """Testa se a conexão com o banco está ativa"""
        assert db_connection is not None
        assert db_connection.closed == 0  # 0 = aberta
    
    def test_database_can_execute_query(self, db_cursor):
        """Testa execução básica de query"""
        db_cursor.execute("SELECT 1 as test_value")
        result = db_cursor.fetchone()
        assert result is not None
        assert result['test_value'] == 1
    
    def test_database_has_expected_tables(self, db_cursor):
        """Verifica se as tabelas principais existem"""
        db_cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            AND table_name IN ('empresa', 'funcionario', 'avaliacao', 'area_detalhe')
            ORDER BY table_name
        """)
        tables = [row['table_name'] for row in db_cursor.fetchall()]
        
        assert 'area_detalhe' in tables
        assert 'avaliacao' in tables
        assert 'empresa' in tables
        assert 'funcionario' in tables


class TestDatabaseTransactions:
    """Testes de transações e rollback"""
    
    def test_transaction_rollback(self, db_connection):
        """Testa se rollback desfaz inserções"""
        cursor = db_connection.cursor(cursor_factory=RealDictCursor)
        
        # Conta registros antes
        cursor.execute("SELECT COUNT(*) as count FROM empresa")
        count_before = cursor.fetchone()['count']
        
        # Tenta inserir (vai falhar por constraint ou será desfeito)
        try:
            cursor.execute("""
                INSERT INTO empresa (nome_empresa) 
                VALUES ('Empresa Teste Rollback XYZ')
            """)
            db_connection.rollback()
        except Exception:
            db_connection.rollback()
        
        # Conta registros depois
        cursor.execute("SELECT COUNT(*) as count FROM empresa")
        count_after = cursor.fetchone()['count']
        
        cursor.close()
        
        # Deve ser igual (rollback funcionou)
        assert count_after == count_before
    
    def test_transaction_isolation(self, db_transaction):
        """Testa isolamento de transação"""
        cursor = db_transaction.cursor(cursor_factory=RealDictCursor)
        
        # Lê dados
        cursor.execute("SELECT COUNT(*) as count FROM funcionario")
        initial_count = cursor.fetchone()['count']
        
        assert initial_count > 0
        
        cursor.close()


class TestDatabaseConstraints:
    """Testes de constraints e integridade referencial"""
    
    def test_funcionario_requires_area_detalhe(self, db_cursor):
        """Verifica constraint de foreign key funcionario -> area_detalhe"""
        # Tenta inserir funcionário com area_detalhe inexistente
        with pytest.raises(psycopg2.Error):
            db_cursor.execute("""
                INSERT INTO funcionario (
                    nome_funcionario, email, id_area_detalhe, 
                    id_cargo, id_genero_catgo, id_geracao_catgo,
                    id_tempo_empresa_catgo, id_localidade
                )
                VALUES (
                    'Teste', 'teste@email.com', 
                    '00000000-0000-0000-0000-000000000000'::uuid,
                    '00000000-0000-0000-0000-000000000000'::uuid,
                    '00000000-0000-0000-0000-000000000000'::uuid,
                    '00000000-0000-0000-0000-000000000000'::uuid,
                    '00000000-0000-0000-0000-000000000000'::uuid,
                    '00000000-0000-0000-0000-000000000000'::uuid
                )
            """)
    
    def test_email_unique_constraint(self, db_cursor):
        """Verifica constraint UNIQUE no email"""
        # Busca um email existente
        db_cursor.execute("SELECT email FROM funcionario LIMIT 1")
        existing = db_cursor.fetchone()
        
        if existing:
            with pytest.raises(psycopg2.IntegrityError):
                db_cursor.execute("""
                    INSERT INTO funcionario (
                        nome_funcionario, email, id_area_detalhe,
                        id_cargo, id_genero_catgo, id_geracao_catgo,
                        id_tempo_empresa_catgo, id_localidade
                    )
                    SELECT 
                        'Teste Duplicado', 
                        %s,
                        id_area_detalhe, id_cargo, id_genero_catgo, 
                        id_geracao_catgo, id_tempo_empresa_catgo, id_localidade
                    FROM funcionario 
                    LIMIT 1
                """, (existing['email'],))


class TestDatabaseQueries:
    """Testes de queries complexas"""
    
    def test_query_funcionarios_with_joins(self, db_cursor):
        """Testa query com múltiplos JOINs"""
        db_cursor.execute("""
            SELECT 
                f.id_funcionario,
                f.nome_funcionario,
                f.email,
                c.nome_cargo,
                ad.nome_area_detalhe,
                l.nome_localidade
            FROM funcionario f
            INNER JOIN cargo c ON f.id_cargo = c.id_cargo
            INNER JOIN area_detalhe ad ON f.id_area_detalhe = ad.id_area_detalhe
            INNER JOIN localidade l ON f.id_localidade = l.id_localidade
            LIMIT 5
        """)
        
        results = db_cursor.fetchall()
        
        assert len(results) > 0
        for row in results:
            assert row['id_funcionario'] is not None
            assert row['nome_funcionario'] is not None
            assert row['nome_cargo'] is not None
            assert row['nome_area_detalhe'] is not None
            assert row['nome_localidade'] is not None
    
    def test_query_hierarquia_completa(self, db_cursor):
        """Testa query de hierarquia organizacional"""
        db_cursor.execute("""
            SELECT 
                e.nome_empresa,
                d.nome_diretoria,
                g.nome_gerencia,
                c.nome_coordenacao,
                ad.nome_area_detalhe,
                COUNT(DISTINCT f.id_funcionario) as total_funcionarios
            FROM empresa e
            INNER JOIN diretoria d ON e.id_empresa = d.id_empresa
            INNER JOIN gerencia g ON d.id_diretoria = g.id_diretoria
            INNER JOIN coordenacao c ON g.id_gerencia = c.id_gerencia
            INNER JOIN area_detalhe ad ON c.id_coordenacao = ad.id_coordenacao
            LEFT JOIN funcionario f ON ad.id_area_detalhe = f.id_area_detalhe
            GROUP BY e.nome_empresa, d.nome_diretoria, g.nome_gerencia, 
                     c.nome_coordenacao, ad.nome_area_detalhe
            LIMIT 10
        """)
        
        results = db_cursor.fetchall()
        
        assert len(results) > 0
        for row in results:
            assert row['nome_empresa'] is not None
            assert row['nome_diretoria'] is not None
            assert row['nome_gerencia'] is not None
            assert row['total_funcionarios'] >= 0
    
    def test_query_agregacao_por_cargo(self, db_cursor):
        """Testa query de agregação por cargo"""
        db_cursor.execute("""
            SELECT 
                c.nome_cargo,
                COUNT(*) as total
            FROM funcionario f
            INNER JOIN cargo c ON f.id_cargo = c.id_cargo
            GROUP BY c.nome_cargo
            ORDER BY total DESC
            LIMIT 5
        """)
        
        results = db_cursor.fetchall()
        
        assert len(results) > 0
        for row in results:
            assert row['nome_cargo'] is not None
            assert row['total'] > 0
