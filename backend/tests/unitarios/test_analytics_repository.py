"""
Testes unitários para AnalyticsRepository
"""

from uuid import UUID

import pytest

from app.repositories.analytics_repository import AnalyticsRepository
from tests.conftest import EMPRESA_ID, FUNCIONARIO_ID


class TestAnalyticsRepository:
    """Testes para AnalyticsRepository"""

    @pytest.fixture
    def repository(self):
        """Instância do AnalyticsRepository"""
        return AnalyticsRepository()

    # ====================
    # get_enps_distribution - SUCESSO
    # ====================

    def test_get_enps_distribution_with_empresa(
        self, repository, mock_db_connection, mock_cursor
    ):
        """Testa get_enps_distribution com empresa"""
        # Arrange
        mock_data = [
            {"categoria": "promotores", "quantidade": 45, "percentual": 45.0},
            {"categoria": "neutros", "quantidade": 30, "percentual": 30.0},
            {"categoria": "detratores", "quantidade": 25, "percentual": 25.0},
        ]
        mock_cursor.fetchall.return_value = mock_data

        # Act
        result = repository.get_enps_distribution(EMPRESA_ID)

        # Assert
        assert isinstance(result, dict)
        assert result["promotores"] == 45
        assert result["neutros"] == 30
        assert result["detratores"] == 25
        assert result["promotores_percentual"] == 45.0
        assert result["neutros_percentual"] == 30.0
        assert result["detratores_percentual"] == 25.0

    def test_get_enps_distribution_without_empresa(
        self, repository, mock_db_connection, mock_cursor
    ):
        """Testa get_enps_distribution sem empresa"""
        # Arrange
        mock_data = [{"categoria": "promotores", "quantidade": 150, "percentual": 100.0}]
        mock_cursor.fetchall.return_value = mock_data

        # Act
        result = repository.get_enps_distribution(None)

        # Assert
        assert isinstance(result, dict)
        assert result["promotores"] == 150
        assert result["promotores_percentual"] == 100.0

    # ====================
    # get_enps_distribution - FALHA
    # ====================

    def test_get_enps_distribution_empty(
        self, repository, mock_db_connection, mock_cursor
    ):
        """Testa get_enps_distribution sem dados"""
        # Arrange
        mock_cursor.fetchall.return_value = []

        # Act
        result = repository.get_enps_distribution(EMPRESA_ID)

        # Assert
        assert isinstance(result, dict)
        assert result["promotores"] == 0
        assert result["neutros"] == 0
        assert result["detratores"] == 0
        assert result["promotores_percentual"] == 0.0
        assert result["neutros_percentual"] == 0.0
        assert result["detratores_percentual"] == 0.0

    # ====================
    # get_tenure_distribution - SUCESSO
    # ====================

    def test_get_tenure_distribution_with_empresa(
        self, repository, mock_db_connection, mock_cursor
    ):
        """Testa get_tenure_distribution com empresa"""
        # Arrange
        mock_data = [
            {"categoria": "menos de 1 ano", "quantidade": 50},
            {"categoria": "entre 2 e 5 anos", "quantidade": 120},
        ]
        mock_cursor.fetchall.return_value = mock_data

        # Act
        result = repository.get_tenure_distribution(EMPRESA_ID)

        # Assert
        assert len(result) == 2
        assert result[1]["quantidade"] == 120

    def test_get_tenure_distribution_without_empresa(
        self, repository, mock_db_connection, mock_cursor
    ):
        """Testa get_tenure_distribution sem empresa"""
        # Arrange
        mock_data = [{"categoria": "mais de 5 anos", "quantidade": 200}]
        mock_cursor.fetchall.return_value = mock_data

        # Act
        result = repository.get_tenure_distribution(None)

        # Assert
        assert len(result) == 1

    # ====================
    # get_tenure_distribution - FALHA
    # ====================

    def test_get_tenure_distribution_empty(
        self, repository, mock_db_connection, mock_cursor
    ):
        """Testa get_tenure_distribution sem funcionários"""
        # Arrange
        mock_cursor.fetchall.return_value = []

        # Act
        result = repository.get_tenure_distribution(EMPRESA_ID)

        # Assert
        assert result == []

    # ====================
    # get_satisfaction_scores - SUCESSO
    # ====================

    def test_get_satisfaction_scores_with_empresa(
        self, repository, mock_db_connection, mock_cursor
    ):
        """Testa get_satisfaction_scores com empresa"""
        # Arrange
        mock_data = [
            {"dimensao": "Interesse no Cargo", "score_medio": 6.5},
            {"dimensao": "Contribuição", "score_medio": 6.8},
        ]
        mock_cursor.fetchall.return_value = mock_data

        # Act
        result = repository.get_satisfaction_scores(EMPRESA_ID)

        # Assert
        assert len(result) == 2
        assert result[0]["score_medio"] == 6.5

    def test_get_satisfaction_scores_without_empresa(
        self, repository, mock_db_connection, mock_cursor
    ):
        """Testa get_satisfaction_scores sem empresa"""
        # Arrange
        mock_data = [{"dimensao": "Feedback", "score_medio": 6.2}]
        mock_cursor.fetchall.return_value = mock_data

        # Act
        result = repository.get_satisfaction_scores(None)

        # Assert
        assert len(result) == 1

    # ====================
    # get_satisfaction_scores - FALHA
    # ====================

    def test_get_satisfaction_scores_empty(
        self, repository, mock_db_connection, mock_cursor
    ):
        """Testa get_satisfaction_scores sem avaliações"""
        # Arrange
        mock_cursor.fetchall.return_value = []

        # Act
        result = repository.get_satisfaction_scores(EMPRESA_ID)

        # Assert
        assert result == []

    # ====================
    # get_employee_detailed_analytics - SUCESSO
    # ====================

    def test_get_employee_detailed_analytics_complete(
        self, repository, mock_db_connection, mock_cursor
    ):
        """Testa get_employee_detailed_analytics completo"""
        # Arrange
        employee_scores = [{"dimensao": "Interesse no Cargo", "score_medio": 7.0}]
        company_averages = [{"dimensao": "Interesse no Cargo", "score_medio": 6.2}]
        area_averages = [{"dimensao": "Interesse no Cargo", "score_medio": 6.5}]
        history = [{"data_avaliacao": "2025-06-15", "score_medio": 7.0}]
        comments = [
            {
                "dimensao": "Interesse no Cargo",
                "score": 7,
                "comentario": "Excelente",
                "data_avaliacao": "2025-06-15",
            }
        ]

        mock_cursor.fetchall.side_effect = [
            employee_scores,
            company_averages,
            area_averages,
            history,
            comments,
        ]

        # Act
        result = repository.get_employee_detailed_analytics(FUNCIONARIO_ID)

        # Assert
        assert "employee_scores" in result
        assert "company_averages" in result
        assert "area_averages" in result
        assert "history" in result
        assert "comments" in result
        assert len(result["employee_scores"]) == 1
        assert len(result["comments"]) == 1

    # ====================
    # get_employee_detailed_analytics - FALHA
    # ====================

    def test_get_employee_detailed_analytics_no_evaluations(
        self, repository, mock_db_connection, mock_cursor
    ):
        """Testa get_employee_detailed_analytics sem avaliações"""
        # Arrange
        mock_cursor.fetchall.side_effect = [[], [], [], [], []]

        # Act
        result = repository.get_employee_detailed_analytics(FUNCIONARIO_ID)

        # Assert
        assert result["employee_scores"] == []
        assert result["company_averages"] == []
        assert result["history"] == []

    def test_get_employee_detailed_analytics_no_comments(
        self, repository, mock_db_connection, mock_cursor
    ):
        """Testa get_employee_detailed_analytics sem comentários"""
        # Arrange
        employee_scores = [{"dimensao": "Interesse no Cargo", "score_medio": 7.0}]
        mock_cursor.fetchall.side_effect = [
            employee_scores,
            employee_scores,
            employee_scores,
            [{"data_avaliacao": "2025-06-15", "score_medio": 7.0}],
            [],  # Sem comentários
        ]

        # Act
        result = repository.get_employee_detailed_analytics(FUNCIONARIO_ID)

        # Assert
        assert len(result["comments"]) == 0
        assert len(result["employee_scores"]) == 1
