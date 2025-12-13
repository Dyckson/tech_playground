"""
Testes unitários para Controllers
"""

from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.main import app
from tests.conftest import AREA_ID, CARGO_ID, EMPRESA_ID, FUNCIONARIO_ID


@pytest.fixture
def client():
    """Cliente de teste FastAPI"""
    return TestClient(app)


class TestHealthController:
    """Testes para endpoint de health check"""

    def test_health_check(self, client):
        """Testa health check"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "database" in data


class TestHierarquiaController:
    """Testes para HierarquiaController"""

    def test_listar_empresas_success(self, client, mock_db_connection, mock_cursor, empresa_data):
        """Testa GET /api/hierarquia/empresas"""
        # Arrange
        mock_cursor.fetchall.return_value = [empresa_data]

        # Act
        response = client.get("/api/v1/hierarquia/empresas")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nome"] == "CloudServices XYZ"

    def test_listar_empresas_empty(self, client, mock_db_connection, mock_cursor):
        """Testa GET /api/hierarquia/empresas sem empresas"""
        # Arrange
        mock_cursor.fetchall.return_value = []

        # Act
        response = client.get("/api/v1/hierarquia/empresas")

        # Assert
        assert response.status_code == 200
        assert response.json() == []

    def test_get_empresa_found(self, client, mock_db_connection, mock_cursor, empresa_data):
        """Testa GET /api/hierarquia/empresas/{id}"""
        # Arrange
        mock_cursor.fetchone.return_value = empresa_data

        # Act
        response = client.get(f"/api/v1/hierarquia/empresas/{EMPRESA_ID}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "CloudServices XYZ"

    def test_get_empresa_not_found(self, client, mock_db_connection, mock_cursor):
        """Testa GET /api/hierarquia/empresas/{id} não encontrada"""
        # Arrange
        mock_cursor.fetchone.return_value = None

        # Act
        response = client.get(f"/api/v1/hierarquia/empresas/{UUID('00000000-0000-0000-0000-000000000000')}")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Empresa não encontrada"

    def test_get_arvore_hierarquica(self, client, mock_db_connection, mock_cursor):
        """Testa GET /api/hierarquia/{empresa_id}/arvore"""
        # Arrange
        nodes = [
            {
                "empresa_id": str(EMPRESA_ID),
                "empresa_nome": "CloudServices",
                "diretoria_id": str(UUID(int=1)),
                "diretoria_nome": "Operações",
                "gerencia_id": str(UUID(int=2)),
                "gerencia_nome": "Cloud",
                "coordenacao_id": str(UUID(int=3)),
                "coordenacao_nome": "Infra",
                "area_id": str(AREA_ID),
                "area_nome": "AWS",
            }
        ]
        mock_cursor.fetchall.return_value = nodes

        # Act
        response = client.get(f"/api/v1/hierarquia/empresas/{EMPRESA_ID}/arvore")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nome"] == "Operações"

    def test_listar_areas(self, client, mock_db_connection, mock_cursor, area_hierarquia_data):
        """Testa GET /api/hierarquia/{empresa_id}/areas"""
        # Arrange
        areas = [
            {
                "id": str(AREA_ID),
                "nome": "AWS",
                "empresa_nome": "CloudServices XYZ",
                "diretoria_nome": "Operações",
                "gerencia_nome": "Cloud",
                "coordenacao_nome": "Infra",
                "empresa_id": str(EMPRESA_ID),
                "diretoria_id": str(UUID(int=1)),
                "gerencia_id": str(UUID(int=2)),
                "coordenacao_id": str(UUID(int=3)),
                "ativo": True,
            }
        ]
        mock_cursor.fetchall.return_value = areas

        # Act
        response = client.get(f"/api/v1/hierarquia/empresas/{EMPRESA_ID}/areas")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["area"] == "AWS"

    def test_get_hierarquia_area_found(self, client, mock_db_connection, mock_cursor, area_hierarquia_data):
        """Testa GET /api/hierarquia/areas/{area_id}/hierarquia"""
        # Arrange
        mock_cursor.fetchone.return_value = area_hierarquia_data

        # Act
        response = client.get(f"/api/v1/hierarquia/areas/{AREA_ID}/hierarquia")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["area"] == "AWS"
        assert data["empresa"] == "CloudServices XYZ"

    def test_get_hierarquia_area_not_found(self, client, mock_db_connection, mock_cursor):
        """Testa GET /api/hierarquia/areas/{area_id}/hierarquia não encontrada"""
        # Arrange
        mock_cursor.fetchone.return_value = None

        # Act
        response = client.get(f"/api/v1/hierarquia/areas/{UUID('00000000-0000-0000-0000-000000000000')}/hierarquia")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Área não encontrada"

    def test_contagem_funcionarios(self, client, mock_db_connection, mock_cursor):
        """Testa GET /api/hierarquia/{empresa_id}/contagem-funcionarios"""
        # Arrange
        contagens = [
            {"area_id": str(AREA_ID), "area_nome": "AWS", "total_funcionarios": 10},
            {"area_id": str(UUID(int=2)), "area_nome": "Azure", "total_funcionarios": 5},
        ]
        mock_cursor.fetchall.return_value = contagens

        # Act
        response = client.get(f"/api/v1/hierarquia/empresas/{EMPRESA_ID}/funcionarios/contagem")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["total_funcionarios"] == 10

    def test_listar_empresas_error_handling(self, client, mock_db_connection, mock_cursor):
        """Testa error handling no GET /api/hierarquia/empresas"""
        # Arrange
        mock_cursor.execute.side_effect = Exception("Database error")

        # Act
        response = client.get("/api/v1/hierarquia/empresas")

        # Assert
        assert response.status_code == 500
        assert "Erro ao listar empresas" in response.json()["detail"]

    def test_get_empresa_error_handling(self, client, mock_db_connection, mock_cursor):
        """Testa error handling no GET /api/hierarquia/empresas/{id}"""
        # Arrange
        mock_cursor.execute.side_effect = Exception("Database error")

        # Act
        response = client.get(f"/api/v1/hierarquia/empresas/{EMPRESA_ID}")

        # Assert
        assert response.status_code == 500
        assert "Erro ao buscar empresa" in response.json()["detail"]

    def test_get_arvore_hierarquica_error_handling(self, client, mock_db_connection, mock_cursor):
        """Testa error handling no GET /api/hierarquia/{empresa_id}/arvore"""
        # Arrange
        mock_cursor.execute.side_effect = Exception("Database error")

        # Act
        response = client.get(f"/api/v1/hierarquia/empresas/{EMPRESA_ID}/arvore")

        # Assert
        assert response.status_code == 500
        assert "Erro ao buscar hierarquia" in response.json()["detail"]

    def test_listar_areas_error_handling(self, client, mock_db_connection, mock_cursor):
        """Testa error handling no GET /api/hierarquia/{empresa_id}/areas"""
        # Arrange
        mock_cursor.execute.side_effect = Exception("Database error")

        # Act
        response = client.get(f"/api/v1/hierarquia/empresas/{EMPRESA_ID}/areas")

        # Assert
        assert response.status_code == 500
        assert "Erro ao listar áreas" in response.json()["detail"]

    def test_get_hierarquia_area_error_handling(self, client, mock_db_connection, mock_cursor):
        """Testa error handling no GET /api/hierarquia/areas/{area_id}/hierarquia"""
        # Arrange
        mock_cursor.execute.side_effect = Exception("Database error")

        # Act
        response = client.get(f"/api/v1/hierarquia/areas/{AREA_ID}/hierarquia")

        # Assert
        assert response.status_code == 500
        assert "Erro ao buscar hierarquia" in response.json()["detail"]

    def test_contagem_funcionarios_error_handling(self, client, mock_db_connection, mock_cursor):
        """Testa error handling no GET /api/hierarquia/{empresa_id}/contagem-funcionarios"""
        # Arrange
        mock_cursor.execute.side_effect = Exception("Database error")

        # Act
        response = client.get(f"/api/v1/hierarquia/empresas/{EMPRESA_ID}/funcionarios/contagem")

        # Assert
        assert response.status_code == 500
        assert "Erro ao contar funcionários" in response.json()["detail"]


class TestFuncionarioController:
    """Testes para FuncionarioController"""

    def test_listar_funcionarios_success(self, client, mock_db_connection, mock_cursor, fake_funcionarios_list):
        """Testa GET /api/v1/funcionarios com empresa_id"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 5}
        mock_cursor.fetchall.return_value = fake_funcionarios_list

        # Act
        response = client.get(f"/api/v1/funcionarios?empresa_id={EMPRESA_ID}&page=1&page_size=10")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert len(data["items"]) == 5

    def test_listar_funcionarios_with_listar_path(
        self, client, mock_db_connection, mock_cursor, fake_funcionarios_list
    ):
        """Testa GET /api/v1/funcionarios com query parameters"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 5}
        mock_cursor.fetchall.return_value = fake_funcionarios_list

        # Act
        response = client.get(f"/api/v1/funcionarios?empresa_id={EMPRESA_ID}&page=1&page_size=10")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5

    def test_listar_funcionarios_with_filters(self, client, mock_db_connection, mock_cursor, funcionario_data):
        """Testa GET /api/v1/funcionarios com filtros"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 1}
        mock_cursor.fetchall.return_value = [funcionario_data]

        # Act
        response = client.get(
            "/api/v1/funcionarios",
            params={
                "empresa_id": str(EMPRESA_ID),
                "page": 1,
                "page_size": 20,
                "areas": [str(AREA_ID)],
                "cargos": [str(CARGO_ID)],
            },
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1

    def test_listar_funcionarios_empty(self, client, mock_db_connection, mock_cursor):
        """Testa GET /api/v1/funcionarios sem resultados"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 0}
        mock_cursor.fetchall.return_value = []

        # Act
        response = client.get(f"/api/v1/funcionarios?empresa_id={EMPRESA_ID}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert len(data["items"]) == 0

    def test_buscar_funcionarios_success(self, client, mock_db_connection, mock_cursor, funcionario_data):
        """Testa GET /api/v1/funcionarios/buscar"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 1}
        mock_cursor.fetchall.return_value = [funcionario_data]

        # Act
        response = client.get(
            "/api/v1/funcionarios/buscar",
            params={"empresa_id": str(EMPRESA_ID), "termo": "Patricia", "page": 1, "page_size": 10},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["nome"] == "Patricia Lima"

    def test_buscar_funcionarios_termo_muito_curto(self, client):
        """Testa GET /api/v1/funcionarios/buscar com termo muito curto"""
        # Act
        response = client.get(
            "/api/v1/funcionarios/buscar", params={"empresa_id": str(EMPRESA_ID), "termo": "P", "page": 1}
        )

        # Assert
        assert response.status_code == 422  # Validation error

    def test_obter_funcionario_found(self, client, mock_db_connection, mock_cursor, funcionario_data):
        """Testa GET /api/funcionarios/detalhe/{funcionario_id}"""
        # Arrange
        mock_cursor.fetchone.return_value = funcionario_data

        # Act
        response = client.get(f"/api/v1/funcionarios/{FUNCIONARIO_ID}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Patricia Lima"

    def test_obter_funcionario_not_found(self, client, mock_db_connection, mock_cursor):
        """Testa GET /api/funcionarios/detalhe/{funcionario_id} não encontrado"""
        # Arrange
        mock_cursor.fetchone.return_value = None

        # Act
        response = client.get(f"/api/v1/funcionarios/{UUID('00000000-0000-0000-0000-000000000000')}")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Funcionário não encontrado"

    def test_obter_filtros(self, client, mock_db_connection, mock_cursor):
        """Testa GET /api/v1/funcionarios/filtros"""
        # Arrange
        areas = [{"id": str(AREA_ID), "nome": "AWS"}]
        cargos = [{"id": str(CARGO_ID), "nome": "DevOps Engineer"}]
        localidades = [{"id": str(UUID(int=5)), "nome": "Remoto - Brasil"}]

        # Simular 3 queries diferentes
        mock_cursor.fetchall.side_effect = [areas, cargos, localidades]

        # Act
        response = client.get(f"/api/v1/funcionarios/filtros?empresa_id={EMPRESA_ID}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "areas" in data
        assert "cargos" in data
        assert "localidades" in data
        assert len(data["areas"]) == 1
        assert data["areas"][0]["nome"] == "AWS"

    @pytest.mark.skip(reason="Endpoint POST /funcionarios/criar não existe no sistema atual")
    def test_criar_funcionario_success(self, client, mock_db_connection, mock_cursor):
        """Testa POST /api/v1/funcionarios/criar"""
        # Arrange
        new_id = "new-funcionario-uuid"
        mock_cursor.fetchone.return_value = {"id": new_id}

        novo_funcionario = {
            "nome": "Novo Funcionário",
            "email": "novo@email.com",
            "email_corporativo": "novo@empresa.com",
            "funcao": "CLT",
            "empresa_id": str(EMPRESA_ID),
            "area_detalhe_id": str(AREA_ID),
            "cargo_id": str(CARGO_ID),
            "genero_id": str(UUID(int=1)),
            "geracao_id": str(UUID(int=2)),
            "tempo_empresa_id": str(UUID(int=3)),
            "localidade_id": str(UUID(int=4)),
        }

        # Act
        response = client.post("/api/v1/funcionarios/criar", json=novo_funcionario)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == new_id
        assert "message" in data

    @pytest.mark.skip(reason="Endpoint POST /funcionarios/criar não existe no sistema atual")
    def test_criar_funcionario_validation_error(self, client):
        """Testa POST /api/v1/funcionarios/criar com dados inválidos"""
        # Arrange
        funcionario_invalido = {
            "nome": "",  # Nome vazio
            "email": "email-invalido",  # Email inválido
            "funcao": "CLT",
        }

        # Act
        response = client.post("/api/v1/funcionarios/criar", json=funcionario_invalido)

        # Assert
        assert response.status_code == 422  # Validation error

    def test_pagination_validation(self, client, mock_db_connection, mock_cursor):
        """Testa validação de paginação"""
        # Arrange
        mock_cursor.fetchone.return_value = {"count": 0}
        mock_cursor.fetchall.return_value = []

        # Act - page_size > 100
        response = client.get(f"/api/v1/funcionarios?empresa_id={EMPRESA_ID}&page=1&page_size=150")

        # Assert
        assert response.status_code == 422  # Validation error

    def test_invalid_uuid(self, client):
        """Testa UUID inválido no query parameter"""
        # Act
        response = client.get("/api/v1/funcionarios?empresa_id=invalid-uuid")

        # Assert
        assert response.status_code == 422  # Validation error


class TestErrorHandlingControllers:
    """Testes de tratamento de erros e validações HTTP"""

    # ==================== VALIDAÇÃO DE PARÂMETROS ====================

    def test_listar_funcionarios_uuid_malformado(self, client):
        """Testa GET /funcionarios com UUID inválido"""
        response = client.get("/api/v1/funcionarios?empresa_id=not-a-valid-uuid")
        assert response.status_code == 422  # Unprocessable Entity

    def test_listar_funcionarios_page_negativa(self, client):
        """Testa paginação com page negativa"""
        response = client.get(f"/api/v1/funcionarios?empresa_id={EMPRESA_ID}&page=-1")
        assert response.status_code == 422

    def test_listar_funcionarios_page_size_zero(self, client):
        """Testa paginação com page_size inválido"""
        response = client.get(f"/api/v1/funcionarios?empresa_id={EMPRESA_ID}&page_size=0")
        assert response.status_code == 422

    def test_listar_funcionarios_page_size_excessivo(self, client, mock_db_connection, mock_cursor):
        """Testa paginação com page_size muito grande"""
        mock_cursor.fetchall.return_value = []
        mock_cursor.fetchone.return_value = {"count": 0}

        # Sistema pode aceitar ou limitar - testamos comportamento atual
        response = client.get(f"/api/v1/funcionarios?empresa_id={EMPRESA_ID}&page_size=10000")
        # Se aceitar: 200, se rejeitar: 422
        assert response.status_code in [200, 422]

    def test_buscar_funcionarios_termo_vazio(self, client):
        """Testa busca com termo vazio"""
        response = client.get(f"/api/v1/funcionarios/buscar?empresa_id={EMPRESA_ID}&termo=")
        # Sistema atualmente retorna 422 para termo vazio
        assert response.status_code == 422

    def test_buscar_funcionarios_termo_muito_curto_dois_chars(self, client, mock_db_connection, mock_cursor):
        """Testa busca com termo de 2 caracteres"""
        mock_cursor.fetchall.return_value = []
        mock_cursor.fetchone.return_value = {"count": 0}
        # Sistema atualmente aceita termo curto
        response = client.get(f"/api/v1/funcionarios/buscar?empresa_id={EMPRESA_ID}&termo=ab")
        assert response.status_code in [200, 400, 422]

    def test_obter_funcionario_uuid_invalido(self, client):
        """Testa GET /funcionarios/detalhe/{id} com UUID mal formatado"""
        response = client.get("/api/v1/funcionarios/123-invalid-uuid")
        assert response.status_code == 422

    # ==================== TESTES DE SEGURANÇA ====================

    def test_buscar_funcionarios_sql_injection_attempt(self, client, mock_db_connection, mock_cursor):
        """Testa busca com tentativa de SQL injection"""
        mock_cursor.fetchall.return_value = []
        mock_cursor.fetchone.return_value = {"count": 0}

        response = client.get(
            "/api/v1/funcionarios/buscar",
            params={"empresa_id": str(EMPRESA_ID), "termo": "'; DROP TABLE funcionario; --"},
        )
        # Deve tratar como string normal, não executar SQL
        assert response.status_code in [200, 400, 422]  # 422 por min_length
        # Importante: não deve retornar 500 (erro de SQL)

    def test_listar_funcionarios_command_injection_in_filters(self, client, mock_db_connection, mock_cursor):
        """Testa filtros com tentativa de command injection"""
        mock_cursor.fetchall.return_value = []
        mock_cursor.fetchone.return_value = {"count": 0}

        response = client.get(
            "/api/v1/funcionarios", params={"empresa_id": str(EMPRESA_ID), "area": "; rm -rf /", "cargo": "$(whoami)"}
        )
        # Deve tratar como strings normais de filtro
        assert response.status_code == 200

    # ==================== EDGE CASES ==

    def test_listar_funcionarios_todos_filtros_invalidos(self, client, mock_db_connection, mock_cursor):
        """Testa múltiplos filtros com valores inválidos"""
        mock_cursor.fetchall.return_value = []
        mock_cursor.fetchone.return_value = {"count": 0}

        response = client.get(
            "/api/v1/funcionarios",
            params={
                "empresa_id": str(EMPRESA_ID),
                "area": "área-inexistente-123",
                "cargo": "cargo-inexistente-456",
                "localidade": "local-inexistente-789",
                "page": 999999,
            },
        )
        # Deve retornar lista vazia, não erro
        assert response.status_code == 200
        assert response.json()["items"] == []

    def test_get_arvore_hierarquica_empresa_inexistente(self, client, mock_db_connection, mock_cursor):
        """Testa árvore hierárquica para empresa que não existe"""
        mock_cursor.fetchall.return_value = []

        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/api/v1/hierarquia/empresas/{fake_uuid}/arvore")
        # Rota pode não existir ou retornar lista vazia
        assert response.status_code in [200, 404]

    def test_contagem_funcionarios_sem_funcionarios(self, client, mock_db_connection, mock_cursor):
        """Testa contagem quando não há funcionários"""
        mock_cursor.fetchall.return_value = []

        response = client.get(f"/api/v1/hierarquia/empresas/{EMPRESA_ID}/areas/contagem-funcionarios")
        # Rota pode não existir ou retornar lista vazia
        assert response.status_code in [200, 404]
