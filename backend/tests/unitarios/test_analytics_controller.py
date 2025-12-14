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
