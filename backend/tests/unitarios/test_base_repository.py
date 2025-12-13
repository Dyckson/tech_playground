"""
Testes unitários para BaseRepository
"""

import pytest

from app.repositories.base_repository import BaseRepository


class TestBaseRepository:
    """Testes para métodos da classe BaseRepository"""

    @pytest.fixture
    def repository(self):
        """Instância do BaseRepository para testes"""
        return BaseRepository()

    def test_execute_query_success(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_query com sucesso"""
        # Arrange
        mock_cursor.fetchall.return_value = [{"id": "1", "nome": "Teste 1"}, {"id": "2", "nome": "Teste 2"}]

        # Act
        result = repository.execute_query("SELECT * FROM tabela", ("param1",))

        # Assert
        assert len(result) == 2
        assert result[0]["id"] == "1"
        assert result[1]["nome"] == "Teste 2"
        mock_cursor.execute.assert_called_once_with("SELECT * FROM tabela", ("param1",))
        mock_cursor.close.assert_called_once()

    def test_execute_query_empty_result(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_query retornando lista vazia"""
        # Arrange
        mock_cursor.fetchall.return_value = []

        # Act
        result = repository.execute_query("SELECT * FROM tabela WHERE id = %s", ("999",))

        # Assert
        assert result == []
        mock_cursor.execute.assert_called_once()

    def test_execute_query_without_params(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_query sem parâmetros"""
        # Arrange
        mock_cursor.fetchall.return_value = [{"count": 10}]

        # Act
        result = repository.execute_query("SELECT COUNT(*) FROM tabela")

        # Assert
        assert len(result) == 1
        mock_cursor.execute.assert_called_once_with("SELECT COUNT(*) FROM tabela", ())

    def test_execute_one_success(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_one retornando um registro"""
        # Arrange
        mock_cursor.fetchone.return_value = {"id": "1", "nome": "Teste"}

        # Act
        result = repository.execute_one("SELECT * FROM tabela WHERE id = %s", ("1",))

        # Assert
        assert result is not None
        assert result["id"] == "1"
        assert result["nome"] == "Teste"
        mock_cursor.execute.assert_called_once()

    def test_execute_one_not_found(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_one quando não encontra registro"""
        # Arrange
        mock_cursor.fetchone.return_value = None

        # Act
        result = repository.execute_one("SELECT * FROM tabela WHERE id = %s", ("999",))

        # Assert
        assert result is None

    def test_execute_insert_success(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_insert com sucesso"""
        # Arrange
        mock_cursor.fetchone.return_value = {"id": "new-uuid-123"}

        # Act
        result = repository.execute_insert("INSERT INTO tabela (nome) VALUES (%s) RETURNING id", ("Novo Registro",))

        # Assert
        assert result == "new-uuid-123"
        mock_cursor.execute.assert_called_once()
        mock_db_connection.commit.assert_called_once()

    def test_execute_insert_error_rollback(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_insert com erro e rollback"""
        # Arrange
        mock_cursor.execute.side_effect = Exception("Erro de INSERT")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.execute_insert("INSERT INTO tabela (nome) VALUES (%s)", ("Teste",))

        assert "Erro de INSERT" in str(exc_info.value)
        mock_db_connection.rollback.assert_called_once()

    def test_execute_update_success(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_update com sucesso"""
        # Arrange
        mock_cursor.rowcount = 3

        # Act
        affected = repository.execute_update("UPDATE tabela SET ativo = %s WHERE status = %s", (True, "pendente"))

        # Assert
        assert affected == 3
        mock_db_connection.commit.assert_called_once()

    def test_execute_update_no_rows_affected(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_update sem linhas afetadas"""
        # Arrange
        mock_cursor.rowcount = 0

        # Act
        affected = repository.execute_update("UPDATE tabela SET nome = %s WHERE id = %s", ("Novo", "999"))

        # Assert
        assert affected == 0

    def test_execute_delete_success(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_delete com sucesso"""
        # Arrange
        mock_cursor.rowcount = 5

        # Act
        deleted = repository.execute_delete("DELETE FROM tabela WHERE ativo = %s", (False,))

        # Assert
        assert deleted == 5
        mock_db_connection.commit.assert_called_once()

    def test_execute_scalar_with_dict_result(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_scalar retornando valor escalar de dicionário"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 42}

        # Act
        result = repository.execute_scalar("SELECT COUNT(*) as count FROM tabela")

        # Assert
        assert result == 42

    def test_execute_scalar_with_tuple_result(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_scalar retornando valor escalar de tupla"""
        # Arrange
        mock_cursor.fetchone.return_value = (100,)

        # Act
        result = repository.execute_scalar("SELECT MAX(id) FROM tabela")

        # Assert
        assert result == 100

    def test_execute_scalar_none_result(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_scalar quando não há resultado"""
        # Arrange
        mock_cursor.fetchone.return_value = None

        # Act
        result = repository.execute_scalar("SELECT AVG(valor) FROM tabela WHERE 1=0")

        # Assert
        assert result is None

    def test_execute_count_with_where(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_count com cláusula WHERE"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 15}

        # Act
        count = repository.execute_count("funcionario", "ativo = %s", (True,))

        # Assert
        assert count == 15
        mock_cursor.execute.assert_called_once()

    def test_execute_count_without_where(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_count sem cláusula WHERE"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 100}

        # Act
        count = repository.execute_count("funcionario")

        # Assert
        assert count == 100

    def test_build_pagination(self, repository):
        """Testa build_pagination com diferentes valores"""
        # Page 1
        limit, offset = repository.build_pagination(1, 20)
        assert limit == 20
        assert offset == 0

        # Page 2
        limit, offset = repository.build_pagination(2, 20)
        assert limit == 20
        assert offset == 20

        # Page 5, size 10
        limit, offset = repository.build_pagination(5, 10)
        assert limit == 10
        assert offset == 40

    def test_build_where_clause_empty_filters(self, repository):
        """Testa build_where_clause com filtros vazios"""
        # Act
        where, params = repository.build_where_clause({})

        # Assert
        assert where == ""
        assert params == ()

    def test_build_where_clause_single_filter(self, repository):
        """Testa build_where_clause com um filtro"""
        # Act
        where, params = repository.build_where_clause({"ativo": True})

        # Assert
        assert where == "ativo = %s"
        assert params == (True,)

    def test_build_where_clause_multiple_filters(self, repository):
        """Testa build_where_clause com múltiplos filtros"""
        # Act
        where, params = repository.build_where_clause({"ativo": True, "tipo": "PJ", "empresa_id": "uuid-123"})

        # Assert
        assert "ativo = %s" in where
        assert "tipo = %s" in where
        assert "empresa_id = %s" in where
        assert " AND " in where
        assert len(params) == 3
        assert True in params
        assert "PJ" in params

    def test_build_where_clause_with_list(self, repository):
        """Testa build_where_clause com filtro de lista (IN)"""
        # Act
        where, params = repository.build_where_clause({"id": ["uuid-1", "uuid-2", "uuid-3"]})

        # Assert
        assert "id IN (%s,%s,%s)" in where
        assert params == ("uuid-1", "uuid-2", "uuid-3")

    def test_build_where_clause_ignore_none_values(self, repository):
        """Testa build_where_clause ignorando valores None"""
        # Act
        where, params = repository.build_where_clause({"ativo": True, "nome": None, "tipo": "CLT"})

        # Assert
        assert "ativo = %s" in where
        assert "tipo = %s" in where
        assert "nome" not in where
        assert len(params) == 2

    # ==================== TESTES DE FALHA E ERROS ====================

    def test_execute_query_sql_syntax_error(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_query com erro de sintaxe SQL"""
        # Arrange
        mock_cursor.execute.side_effect = Exception("syntax error at or near 'FORM'")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.execute_query("SELECT * FORM tabela")  # typo proposital

        assert "syntax error" in str(exc_info.value)

    def test_execute_update_database_error_rollback(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_update com erro e rollback"""
        # Arrange
        mock_cursor.execute.side_effect = Exception("Foreign key constraint violation")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.execute_update("UPDATE tabela SET campo = %s", ("valor",))

        assert "Foreign key constraint" in str(exc_info.value)
        mock_db_connection.rollback.assert_called_once()

    def test_execute_delete_constraint_violation(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_delete com violação de constraint"""
        # Arrange
        mock_cursor.execute.side_effect = Exception("Cannot delete: referenced by other table")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.execute_delete("DELETE FROM empresa WHERE id = %s", ("uuid-123",))

        assert "Cannot delete" in str(exc_info.value)
        mock_db_connection.rollback.assert_called_once()

    def test_execute_one_database_timeout(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_one com timeout de query"""
        # Arrange
        mock_cursor.execute.side_effect = Exception("Query timeout exceeded")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.execute_one("SELECT * FROM tabela WHERE id = %s", ("uuid",))

        assert "timeout" in str(exc_info.value).lower()

    def test_execute_scalar_invalid_column(self, repository, mock_db_connection, mock_cursor):
        """Testa execute_scalar com coluna inexistente"""
        # Arrange
        mock_cursor.execute.side_effect = Exception("column 'nonexistent' does not exist")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.execute_scalar("SELECT nonexistent FROM tabela")

        assert "does not exist" in str(exc_info.value)
