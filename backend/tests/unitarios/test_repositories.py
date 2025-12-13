"""
Testes unitários para FuncionarioRepository e HierarquiaRepository
"""

from uuid import UUID

import pytest

from app.repositories.funcionario_repository import FuncionarioRepository
from app.repositories.hierarquia_repository import HierarquiaRepository
from tests.conftest import AREA_ID, CARGO_ID, EMPRESA_ID, FUNCIONARIO_ID


class TestFuncionarioRepository:
    """Testes para FuncionarioRepository"""

    @pytest.fixture
    def repository(self):
        """Instância do FuncionarioRepository"""
        return FuncionarioRepository()

    def test_get_funcionarios_paginado_success(
        self, repository, mock_db_connection, mock_cursor, fake_funcionarios_list
    ):
        """Testa get_funcionarios_paginado com sucesso"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 5}
        mock_cursor.fetchall.return_value = fake_funcionarios_list

        # Act
        result, total = repository.get_funcionarios_paginado(empresa_id=EMPRESA_ID, page=1, page_size=10)

        # Assert
        assert total == 5
        assert len(result) == 5
        assert mock_cursor.execute.call_count == 2  # COUNT + SELECT

    def test_get_funcionarios_paginado_with_filters(
        self, repository, mock_db_connection, mock_cursor, funcionario_data
    ):
        """Testa get_funcionarios_paginado com filtros"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 1}
        mock_cursor.fetchall.return_value = [funcionario_data]

        areas = [AREA_ID]
        cargos = [CARGO_ID]

        # Act
        result, total = repository.get_funcionarios_paginado(
            empresa_id=EMPRESA_ID, page=1, page_size=20, areas=areas, cargos=cargos
        )

        # Assert
        assert total == 1
        assert len(result) == 1
        # Verificar que os filtros foram aplicados na query
        call_args = mock_cursor.execute.call_args_list
        assert any(str(AREA_ID) in str(args) for args in call_args)
        assert any(str(CARGO_ID) in str(args) for args in call_args)

    def test_get_funcionarios_paginado_empty_result(self, repository, mock_db_connection, mock_cursor):
        """Testa get_funcionarios_paginado sem resultados"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 0}
        mock_cursor.fetchall.return_value = []

        # Act
        result, total = repository.get_funcionarios_paginado(empresa_id=EMPRESA_ID, page=1, page_size=10)

        # Assert
        assert total == 0
        assert len(result) == 0

    def test_get_funcionarios_paginado_with_all_filters(
        self, repository, mock_db_connection, mock_cursor, funcionario_data
    ):
        """Testa get_funcionarios_paginado com todos os filtros"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 1}
        mock_cursor.fetchall.return_value = [funcionario_data]

        localidade_id = UUID("23ab9902-15a0-417a-9d60-b0bca3d8dde2")

        # Act
        result, total = repository.get_funcionarios_paginado(
            empresa_id=EMPRESA_ID, page=2, page_size=5, areas=[AREA_ID], cargos=[CARGO_ID], localidades=[localidade_id]
        )

        # Assert
        assert total == 1
        assert len(result) == 1

    def test_buscar_funcionarios_by_nome(self, repository, mock_db_connection, mock_cursor, funcionario_data):
        """Testa buscar_funcionarios por nome"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 1}
        mock_cursor.fetchall.return_value = [funcionario_data]

        # Act
        result, total = repository.buscar_funcionarios(
            empresa_id=EMPRESA_ID, termo_busca="Patricia", page=1, page_size=10
        )

        # Assert
        assert total == 1
        assert len(result) == 1
        # Verificar padrão ILIKE na query
        call_args = str(mock_cursor.execute.call_args_list)
        assert "%Patricia%" in call_args

    def test_buscar_funcionarios_by_email(self, repository, mock_db_connection, mock_cursor, funcionario_data):
        """Testa buscar_funcionarios por email"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 1}
        mock_cursor.fetchall.return_value = [funcionario_data]

        # Act
        result, total = repository.buscar_funcionarios(
            empresa_id=EMPRESA_ID, termo_busca="email.com", page=1, page_size=10
        )

        # Assert
        assert total == 1
        assert len(result) == 1

    def test_buscar_funcionarios_no_results(self, repository, mock_db_connection, mock_cursor):
        """Testa buscar_funcionarios sem resultados"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 0}
        mock_cursor.fetchall.return_value = []

        # Act
        result, total = repository.buscar_funcionarios(
            empresa_id=EMPRESA_ID, termo_busca="NaoExiste", page=1, page_size=10
        )

        # Assert
        assert total == 0
        assert len(result) == 0

    def test_get_funcionario_by_id_found(self, repository, mock_db_connection, mock_cursor, funcionario_data):
        """Testa get_funcionario_by_id encontrando funcionário"""
        # Arrange
        mock_cursor.fetchone.return_value = funcionario_data

        # Act
        result = repository.get_funcionario_by_id(FUNCIONARIO_ID)

        # Assert
        assert result is not None
        assert result["id"] == str(FUNCIONARIO_ID)
        assert result["nome"] == "Patricia Lima"
        mock_cursor.execute.assert_called_once()

    def test_get_funcionario_by_id_not_found(self, repository, mock_db_connection, mock_cursor):
        """Testa get_funcionario_by_id não encontrando funcionário"""
        # Arrange
        mock_cursor.fetchone.return_value = None

        # Act
        result = repository.get_funcionario_by_id(UUID("00000000-0000-0000-0000-000000000000"))

        # Assert
        assert result is None

    def test_get_areas_unicas(self, repository, mock_db_connection, mock_cursor):
        """Testa get_areas_unicas"""
        # Arrange
        areas = [{"id": str(AREA_ID), "nome": "AWS"}, {"id": str(UUID(int=2)), "nome": "Azure"}]
        mock_cursor.fetchall.return_value = areas

        # Act
        result = repository.get_areas_unicas(EMPRESA_ID)

        # Assert
        assert len(result) == 2
        assert result[0]["nome"] == "AWS"
        mock_cursor.execute.assert_called_once()

    def test_get_cargos_unicos(self, repository, mock_db_connection, mock_cursor):
        """Testa get_cargos_unicos"""
        # Arrange
        cargos = [
            {"id": str(CARGO_ID), "nome": "DevOps Engineer"},
            {"id": str(UUID(int=3)), "nome": "Desenvolvedor Sênior"},
        ]
        mock_cursor.fetchall.return_value = cargos

        # Act
        result = repository.get_cargos_unicos(EMPRESA_ID)

        # Assert
        assert len(result) == 2
        assert result[0]["nome"] == "DevOps Engineer"

    def test_get_localidades_unicas(self, repository, mock_db_connection, mock_cursor):
        """Testa get_localidades_unicas"""
        # Arrange
        localidades = [
            {"id": str(UUID(int=5)), "nome": "Remoto - Brasil"},
            {"id": str(UUID(int=6)), "nome": "São Paulo - SP"},
        ]
        mock_cursor.fetchall.return_value = localidades

        # Act
        result = repository.get_localidades_unicas(EMPRESA_ID)

        # Assert
        assert len(result) == 2
        assert "Remoto - Brasil" in [loc["nome"] for loc in result]

    def test_criar_funcionario_success(self, repository, mock_db_connection, mock_cursor):
        """Testa criar_funcionario com sucesso"""
        # Arrange
        new_id = "new-funcionario-uuid"
        mock_cursor.fetchone.return_value = {"id": new_id}

        dados = {
            "nome": "Novo Funcionário",
            "email": "novo@email.com",
            "email_corporativo": "novo@empresa.com",
            "funcao": "CLT",
            "area_detalhe_id": AREA_ID,
            "cargo_id": CARGO_ID,
            "genero_id": UUID(int=1),
            "geracao_id": UUID(int=2),
            "tempo_empresa_id": UUID(int=3),
            "localidade_id": UUID(int=4),
        }

        # Act
        result = repository.criar_funcionario(dados)

        # Assert
        assert result == new_id
        mock_cursor.execute.assert_called_once()
        mock_db_connection.commit.assert_called_once()


class TestHierarquiaRepository:
    """Testes para HierarquiaRepository"""

    @pytest.fixture
    def repository(self):
        """Instância do HierarquiaRepository"""
        return HierarquiaRepository()

    def test_get_all_empresas(self, repository, mock_db_connection, mock_cursor, empresa_data):
        """Testa get_all_empresas"""
        # Arrange
        empresas = [empresa_data, {**empresa_data, "id": str(UUID(int=2)), "nome": "Outra Empresa"}]
        mock_cursor.fetchall.return_value = empresas

        # Act
        result = repository.get_all_empresas()

        # Assert
        assert len(result) == 2
        assert result[0]["nome"] == "CloudServices XYZ"
        mock_cursor.execute.assert_called_once()

    def test_get_all_empresas_empty(self, repository, mock_db_connection, mock_cursor):
        """Testa get_all_empresas sem empresas"""
        # Arrange
        mock_cursor.fetchall.return_value = []

        # Act
        result = repository.get_all_empresas()

        # Assert
        assert len(result) == 0

    def test_get_empresa_by_id_found(self, repository, mock_db_connection, mock_cursor, empresa_data):
        """Testa get_empresa_by_id encontrando empresa"""
        # Arrange
        mock_cursor.fetchone.return_value = empresa_data

        # Act
        result = repository.get_empresa_by_id(EMPRESA_ID)

        # Assert
        assert result is not None
        assert result["id"] == str(EMPRESA_ID)
        assert result["nome"] == "CloudServices XYZ"

    def test_get_empresa_by_id_not_found(self, repository, mock_db_connection, mock_cursor):
        """Testa get_empresa_by_id não encontrando empresa"""
        # Arrange
        mock_cursor.fetchone.return_value = None

        # Act
        result = repository.get_empresa_by_id(UUID("00000000-0000-0000-0000-000000000000"))

        # Assert
        assert result is None

    def test_get_arvore_hierarquica(self, repository, mock_db_connection, mock_cursor):
        """Testa get_arvore_hierarquica"""
        # Arrange
        arvore = [
            {
                "empresa_id": str(EMPRESA_ID),
                "empresa_nome": "CloudServices XYZ",
                "diretoria_id": str(UUID(int=1)),
                "diretoria_nome": "Operações",
                "gerencia_id": str(UUID(int=2)),
                "gerencia_nome": "Cloud Infrastructure",
                "coordenacao_id": str(UUID(int=3)),
                "coordenacao_nome": "Infrastructure",
                "area_id": str(AREA_ID),
                "area_nome": "AWS",
            }
        ]
        mock_cursor.fetchall.return_value = arvore

        # Act
        result = repository.get_arvore_hierarquica(EMPRESA_ID)

        # Assert
        assert len(result) == 1
        assert result[0]["empresa_nome"] == "CloudServices XYZ"
        assert result[0]["area_nome"] == "AWS"

    def test_get_areas_by_empresa(self, repository, mock_db_connection, mock_cursor, area_hierarquia_data):
        """Testa get_areas_by_empresa"""
        # Arrange
        areas = [area_hierarquia_data, {**area_hierarquia_data, "id": str(UUID(int=2)), "nome": "Azure"}]
        mock_cursor.fetchall.return_value = areas

        # Act
        result = repository.get_areas_by_empresa(EMPRESA_ID)

        # Assert
        assert len(result) == 2
        assert result[0]["empresa"] == "CloudServices XYZ"

    def test_get_area_hierarquia_found(self, repository, mock_db_connection, mock_cursor, area_hierarquia_data):
        """Testa get_area_hierarquia encontrando área"""
        # Arrange
        mock_cursor.fetchone.return_value = area_hierarquia_data

        # Act
        result = repository.get_area_hierarquia(AREA_ID)

        # Assert
        assert result is not None
        assert result["area"] == "AWS"
        assert result["empresa"] == "CloudServices XYZ"

    def test_get_area_hierarquia_not_found(self, repository, mock_db_connection, mock_cursor):
        """Testa get_area_hierarquia não encontrando área"""
        # Arrange
        mock_cursor.fetchone.return_value = None

        # Act
        result = repository.get_area_hierarquia(UUID("00000000-0000-0000-0000-000000000000"))

        # Assert
        assert result is None

    def test_get_diretorias_by_empresa(self, repository, mock_db_connection, mock_cursor):
        """Testa get_diretorias_by_empresa"""
        # Arrange
        diretorias = [
            {"id": str(UUID(int=1)), "nome": "Operações", "empresa_id": str(EMPRESA_ID)},
            {"id": str(UUID(int=2)), "nome": "Tecnologia", "empresa_id": str(EMPRESA_ID)},
        ]
        mock_cursor.fetchall.return_value = diretorias

        # Act
        result = repository.get_diretorias_by_empresa(EMPRESA_ID)

        # Assert
        assert len(result) == 2
        assert result[0]["nome"] == "Operações"

    def test_get_gerencias_by_diretoria(self, repository, mock_db_connection, mock_cursor):
        """Testa get_gerencias_by_diretoria"""
        # Arrange
        diretoria_id = UUID(int=1)
        gerencias = [
            {"id": str(UUID(int=10)), "nome": "Cloud Infrastructure", "diretoria_id": str(diretoria_id)},
            {"id": str(UUID(int=11)), "nome": "Security", "diretoria_id": str(diretoria_id)},
        ]
        mock_cursor.fetchall.return_value = gerencias

        # Act
        result = repository.get_gerencias_by_diretoria(diretoria_id)

        # Assert
        assert len(result) == 2
        assert result[0]["nome"] == "Cloud Infrastructure"

    def test_get_coordenacoes_by_gerencia(self, repository, mock_db_connection, mock_cursor):
        """Testa get_coordenacoes_by_gerencia"""
        # Arrange
        gerencia_id = UUID(int=10)
        coordenacoes = [
            {"id": str(UUID(int=20)), "nome": "Infrastructure", "gerencia_id": str(gerencia_id)},
            {"id": str(UUID(int=21)), "nome": "DevOps", "gerencia_id": str(gerencia_id)},
        ]
        mock_cursor.fetchall.return_value = coordenacoes

        # Act
        result = repository.get_coordenacoes_by_gerencia(gerencia_id)

        # Assert
        assert len(result) == 2
        assert result[0]["nome"] == "Infrastructure"

    def test_count_funcionarios_by_area(self, repository, mock_db_connection, mock_cursor):
        """Testa count_funcionarios_by_area"""
        # Arrange
        contagem = [
            {"area_id": str(AREA_ID), "area_nome": "AWS", "total_funcionarios": 10},
            {"area_id": str(UUID(int=2)), "area_nome": "Azure", "total_funcionarios": 5},
            {"area_id": str(UUID(int=3)), "area_nome": "GCP", "total_funcionarios": 0},
        ]
        mock_cursor.fetchall.return_value = contagem

        # Act
        result = repository.count_funcionarios_by_area(EMPRESA_ID)

        # Assert
        assert len(result) == 3
        assert result[0]["total_funcionarios"] == 10
        assert result[2]["total_funcionarios"] == 0


class TestRepositoriesFailureCases:
    """Testes de casos de falha para repositories"""

    def test_get_funcionarios_paginado_database_error(self, mock_db_connection, mock_cursor):
        """Testa get_funcionarios_paginado com erro de database"""
        # Arrange
        from app.repositories.funcionario_repository import FuncionarioRepository

        repository = FuncionarioRepository()
        mock_cursor.execute.side_effect = Exception("Database connection lost")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.get_funcionarios_paginado(EMPRESA_ID, page=1, page_size=10)

        assert "Database connection lost" in str(exc_info.value)

    def test_criar_funcionario_duplicate_key(self, mock_db_connection, mock_cursor, funcionario_data):
        """Testa criar_funcionario com violação de unique constraint"""
        # Arrange
        from app.repositories.funcionario_repository import FuncionarioRepository

        repository = FuncionarioRepository()
        mock_cursor.execute.side_effect = Exception("duplicate key value violates unique constraint")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.criar_funcionario(funcionario_data)

        assert "duplicate key" in str(exc_info.value)
        mock_db_connection.rollback.assert_called_once()

    def test_get_funcionario_by_id_invalid_uuid_format(self, mock_db_connection, mock_cursor):
        """Testa get_funcionario_by_id com UUID mal formatado"""
        # Arrange
        from app.repositories.funcionario_repository import FuncionarioRepository

        repository = FuncionarioRepository()
        mock_cursor.execute.side_effect = Exception("invalid input syntax for type uuid")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.get_funcionario_by_id("not-a-valid-uuid")

        assert "invalid input syntax" in str(exc_info.value)

    def test_get_arvore_hierarquica_query_timeout(self, mock_db_connection, mock_cursor):
        """Testa get_arvore_hierarquica com timeout"""
        # Arrange
        from app.repositories.hierarquia_repository import HierarquiaRepository

        repository = HierarquiaRepository()
        mock_cursor.execute.side_effect = Exception("Query execution timeout")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.get_arvore_hierarquica(EMPRESA_ID)

        assert "timeout" in str(exc_info.value).lower()

    def test_buscar_funcionarios_sql_error(self, mock_db_connection, mock_cursor):
        """Testa buscar_funcionarios com erro SQL"""
        # Arrange
        from app.repositories.funcionario_repository import FuncionarioRepository

        repository = FuncionarioRepository()
        mock_cursor.execute.side_effect = Exception("column 'nome_invalido' does not exist")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            repository.buscar_funcionarios(EMPRESA_ID, "teste", page=1, page_size=10)

        assert "does not exist" in str(exc_info.value)
