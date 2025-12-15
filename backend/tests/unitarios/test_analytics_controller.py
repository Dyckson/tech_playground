"""
Testes unitários para AnalyticsController
"""

from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.main import app
from tests.conftest import EMPRESA_ID


@pytest.fixture
def client():
    """Cliente de teste FastAPI"""
    return TestClient(app)


class TestAnalyticsController:
    """Testes para AnalyticsController"""

    # ====================
    # GET /analytics/enps - SUCESSO
    # ====================

    def test_get_enps_distribution_success_with_empresa(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/enps com empresa"""
        # Arrange
        mock_data = [
            {"categoria": "promotores", "quantidade": 45, "percentual": 45.0},
            {"categoria": "neutros", "quantidade": 30, "percentual": 30.0},
            {"categoria": "detratores", "quantidade": 25, "percentual": 25.0},
        ]
        mock_cursor.fetchall.return_value = mock_data

        # Act
        response = client.get(f"/api/v1/analytics/enps?empresa_id={EMPRESA_ID}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "enps_score" in data
        assert "promotores" in data
        assert "total_respostas" in data
        assert data["promotores"] == 45
        assert data["enps_score"] == 20.0  # 45% - 25%

    def test_get_enps_distribution_success_without_empresa(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/enps sem empresa"""
        # Arrange
        mock_data = [{"categoria": "Promotor", "quantidade": 100}]
        mock_cursor.fetchall.return_value = mock_data

        # Act
        response = client.get("/api/v1/analytics/enps")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "total_respostas" in data

    # ====================
    # GET /analytics/enps - FALHA
    # ====================

    def test_get_enps_distribution_empty(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/enps sem dados"""
        # Arrange
        mock_cursor.fetchall.return_value = []

        # Act
        response = client.get("/api/v1/analytics/enps")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total_respostas"] == 0
        assert data["enps_score"] == 0

    def test_get_enps_distribution_invalid_empresa_id(self, client):
        """Testa GET /analytics/enps com empresa_id inválido"""
        # Act
        response = client.get("/api/v1/analytics/enps?empresa_id=invalid-uuid")

        # Assert
        assert response.status_code == 422  # Validation error

    # ====================
    # GET /analytics/tenure-distribution - SUCESSO
    # ====================

    def test_get_tenure_distribution_success(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/tenure-distribution com sucesso"""
        # Arrange
        mock_data = [
            {"categoria": "menos de 1 ano", "quantidade": 50},
            {"categoria": "entre 2 e 5 anos", "quantidade": 120},
        ]
        mock_cursor.fetchall.return_value = mock_data

        # Act
        response = client.get(f"/api/v1/analytics/tenure-distribution?empresa_id={EMPRESA_ID}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "distribuicao" in data
        assert "total_funcionarios" in data
        assert data["total_funcionarios"] == 170

    def test_get_tenure_distribution_without_empresa(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/tenure-distribution sem empresa"""
        # Arrange
        mock_data = [{"categoria": "mais de 5 anos", "quantidade": 200}]
        mock_cursor.fetchall.return_value = mock_data

        # Act
        response = client.get("/api/v1/analytics/tenure-distribution")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total_funcionarios"] == 200

    # ====================
    # GET /analytics/tenure-distribution - FALHA
    # ====================

    def test_get_tenure_distribution_empty(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/tenure-distribution sem dados"""
        # Arrange
        mock_cursor.fetchall.return_value = []

        # Act
        response = client.get("/api/v1/analytics/tenure-distribution")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total_funcionarios"] == 0
        assert data["distribuicao"] == []

    def test_get_tenure_distribution_invalid_empresa_id(self, client):
        """Testa GET /analytics/tenure-distribution com empresa_id inválido"""
        # Act
        response = client.get("/api/v1/analytics/tenure-distribution?empresa_id=not-a-uuid")

        # Assert
        assert response.status_code == 422

    # ====================
    # GET /analytics/satisfaction-scores - SUCESSO
    # ====================

    def test_get_satisfaction_scores_success(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/satisfaction-scores com sucesso"""
        # Arrange
        mock_data = [
            {"dimensao": "Interesse no Cargo", "score_medio": 6.5},
            {"dimensao": "Contribuição", "score_medio": 6.8},
        ]
        mock_cursor.fetchall.return_value = mock_data

        # Act
        response = client.get(f"/api/v1/analytics/satisfaction-scores?empresa_id={EMPRESA_ID}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "dimensoes" in data
        assert "score_geral" in data
        assert "total_dimensoes" in data
        assert len(data["dimensoes"]) == 2
        assert data["score_geral"] == 6.65

    def test_get_satisfaction_scores_without_empresa(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/satisfaction-scores sem empresa"""
        # Arrange
        mock_data = [{"dimensao": "Feedback", "score_medio": 6.2}]
        mock_cursor.fetchall.return_value = mock_data

        # Act
        response = client.get("/api/v1/analytics/satisfaction-scores")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["score_geral"] == 6.2
        assert data["total_dimensoes"] == 1

    # ====================
    # GET /analytics/satisfaction-scores - FALHA
    # ====================

    def test_get_satisfaction_scores_empty(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/satisfaction-scores sem dados"""
        # Arrange
        mock_cursor.fetchall.return_value = []

        # Act
        response = client.get("/api/v1/analytics/satisfaction-scores")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["score_geral"] == 0
        assert data["dimensoes"] == []
        assert data["total_dimensoes"] == 0

    def test_get_satisfaction_scores_invalid_empresa_id(self, client):
        """Testa GET /analytics/satisfaction-scores com empresa_id inválido"""
        # Act
        response = client.get("/api/v1/analytics/satisfaction-scores?empresa_id=bad-uuid")

        # Assert
        assert response.status_code == 422

    # ====================
    # Task 7 - GET /analytics/areas/scores-comparison - SUCESSO
    # ====================

    def test_get_areas_scores_comparison_success_with_empresa(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/areas/scores-comparison com empresa"""
        # Arrange
        mock_cursor.fetchall.return_value = [
            {"id_area_detalhe": "a1", "area_nome": "Vendas", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Dir", "dimensao": "Liderança", "score_medio": 7.5, "total_funcionarios": 10, "total_respostas": 20},
            {"id_area_detalhe": "a1", "area_nome": "Vendas", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Dir", "dimensao": "Ambiente", "score_medio": 8.0, "total_funcionarios": 10, "total_respostas": 20},
        ]

        # Act
        response = client.get(f"/api/v1/analytics/areas/scores-comparison?empresa_id={EMPRESA_ID}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "areas" in data
        assert len(data["areas"]) == 1
        assert data["areas"][0]["area_nome"] == "Vendas"
        assert data["areas"][0]["score_medio_geral"] == 7.75

    def test_get_areas_scores_comparison_success_without_empresa(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/areas/scores-comparison sem empresa"""
        # Arrange
        mock_cursor.fetchall.return_value = [
            {"id_area_detalhe": "a2", "area_nome": "TI", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Dir", "dimensao": "Liderança", "score_medio": 8.5, "total_funcionarios": 15, "total_respostas": 30},
        ]

        # Act
        response = client.get("/api/v1/analytics/areas/scores-comparison")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["areas"]) == 1
        assert data["areas"][0]["score_medio_geral"] == 8.5

    def test_get_areas_scores_comparison_empty(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/areas/scores-comparison sem dados"""
        # Arrange
        mock_cursor.fetchall.return_value = []

        # Act
        response = client.get("/api/v1/analytics/areas/scores-comparison")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["areas"] == []

    def test_get_areas_scores_comparison_invalid_empresa_id(self, client):
        """Testa GET /analytics/areas/scores-comparison com empresa_id inválido"""
        # Act
        response = client.get("/api/v1/analytics/areas/scores-comparison?empresa_id=invalid-uuid")

        # Assert
        assert response.status_code == 422

    # ====================
    # Task 7 - GET /analytics/areas/enps-comparison - SUCESSO
    # ====================

    def test_get_areas_enps_comparison_success_with_empresa(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/areas/enps-comparison com empresa"""
        # Arrange
        mock_cursor.fetchall.return_value = [
            {"id_area_detalhe": "a1", "area_nome": "Marketing", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Comercial", "promotores": 60, "neutros": 30, "detratores": 10, "promotores_percentual": 60.0, "neutros_percentual": 30.0, "detratores_percentual": 10.0, "total_respostas": 100},
            {"id_area_detalhe": "a2", "area_nome": "Financeiro", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Admin", "promotores": 30, "neutros": 40, "detratores": 30, "promotores_percentual": 30.0, "neutros_percentual": 40.0, "detratores_percentual": 30.0, "total_respostas": 100},
        ]

        # Act
        response = client.get(f"/api/v1/analytics/areas/enps-comparison?empresa_id={EMPRESA_ID}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "areas" in data
        assert "melhor_area" in data
        assert "pior_area" in data
        assert "enps_medio" in data
        assert len(data["areas"]) == 2
        assert data["areas"][0]["enps_score"] == 50.0
        assert data["melhor_area"]["area_nome"] == "Marketing"

    def test_get_areas_enps_comparison_success_without_empresa(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/areas/enps-comparison sem empresa"""
        # Arrange
        mock_cursor.fetchall.return_value = [
            {"id_area_detalhe": "a1", "area_nome": "RH", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Pessoas", "promotores": 70, "neutros": 20, "detratores": 10, "promotores_percentual": 70.0, "neutros_percentual": 20.0, "detratores_percentual": 10.0, "total_respostas": 100},
        ]

        # Act
        response = client.get("/api/v1/analytics/areas/enps-comparison")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["areas"]) == 1
        assert data["areas"][0]["enps_score"] == 60.0

    def test_get_areas_enps_comparison_empty(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/areas/enps-comparison sem dados"""
        # Arrange
        mock_cursor.fetchall.return_value = []

        # Act
        response = client.get("/api/v1/analytics/areas/enps-comparison")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["areas"] == []
        assert data["melhor_area"] is None
        assert data["enps_medio"] == 0

    def test_get_areas_enps_comparison_invalid_empresa_id(self, client):
        """Testa GET /analytics/areas/enps-comparison com empresa_id inválido"""
        # Act
        response = client.get("/api/v1/analytics/areas/enps-comparison?empresa_id=not-a-uuid")

        # Assert
        assert response.status_code == 422

    # ====================
    # Task 7 - GET /analytics/areas/{area_id}/detailed-metrics - SUCESSO
    # ====================

    def test_get_area_detailed_metrics_success(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/areas/{area_id}/detailed-metrics com sucesso"""
        # Arrange
        area_id = "550e8400-e29b-41d4-a716-446655440001"
        mock_cursor.fetchall.side_effect = [
            # area_scores
            [{"dimensao": "Liderança", "score_medio": 7.2, "total_respostas": 20, "total_funcionarios": 25}],
            # company_averages
            [{"dimensao": "Liderança", "score_medio": 6.8}],
            # enps
            [{"detratores": 2, "neutros": 8, "promotores": 15}],
            # area_info
            [{"area_nome": "Logística", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Operações", "total_funcionarios": 25}],
        ]

        # Act
        response = client.get(f"/api/v1/analytics/areas/{area_id}/detailed-metrics")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "area_info" in data
        assert "enps" in data
        assert "scores_comparison" in data
        assert data["area_info"]["area_nome"] == "Logística"
        assert data["enps"]["enps_score"] == 52.0

    def test_get_area_detailed_metrics_no_funcionarios(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/areas/{area_id}/detailed-metrics sem funcionários"""
        # Arrange
        area_id = "550e8400-e29b-41d4-a716-446655440002"
        mock_cursor.fetchall.side_effect = [
            [],  # area_scores
            [{"dimensao": "Liderança", "score_medio": 7.0}],  # company_averages
            [{"detratores": 0, "neutros": 0, "promotores": 0}],  # enps
            [{"area_nome": "Nova Área", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Expansão", "total_funcionarios": 0}],  # area_info
        ]

        # Act
        response = client.get(f"/api/v1/analytics/areas/{area_id}/detailed-metrics")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["area_info"]["total_funcionarios"] == 0
        assert data["enps"]["enps_score"] == 0

    def test_get_area_detailed_metrics_area_not_found(self, client, mock_db_connection, mock_cursor):
        """Testa GET /analytics/areas/{area_id}/detailed-metrics com área inexistente"""
        # Arrange
        area_id = "550e8400-e29b-41d4-a716-446655440099"
        mock_cursor.fetchall.side_effect = [
            [],  # area_scores
            [{"dimensao": "Liderança", "score_medio": 7.0}],  # company_averages
            [{"detratores": 0, "neutros": 0, "promotores": 0}],  # enps
            [],  # area_info (vazio = não encontrada)
        ]

        # Act
        response = client.get(f"/api/v1/analytics/areas/{area_id}/detailed-metrics")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["area_info"] is None

    def test_get_area_detailed_metrics_invalid_area_id(self, client):
        """Testa GET /analytics/areas/{area_id}/detailed-metrics com area_id inválido"""
        # Act
        response = client.get("/api/v1/analytics/areas/invalid-uuid/detailed-metrics")

        # Assert
        assert response.status_code == 422
