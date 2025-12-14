"""
Testes unitários para AnalyticsService
"""

from unittest.mock import patch
from uuid import UUID

import pytest

from app.services.analytics_service import AnalyticsService
from tests.conftest import EMPRESA_ID, FUNCIONARIO_ID


class TestAnalyticsService:
    """Testes para AnalyticsService"""

    @pytest.fixture
    def service(self):
        """Instância do AnalyticsService"""
        return AnalyticsService()

    @pytest.fixture
    def mock_repository(self, service):
        """Mock do AnalyticsRepository"""
        with patch.object(service, "repository") as mock_repo:
            yield mock_repo

    # ====================
    # get_enps_distribution - SUCESSO
    # ====================

    def test_get_enps_distribution_success_with_empresa(self, service, mock_repository):
        """Testa get_enps_distribution com sucesso"""
        # Arrange
        mock_data = {
            "promotores": 45,
            "neutros": 30,
            "detratores": 25,
            "promotores_percentual": 45.0,
            "neutros_percentual": 30.0,
            "detratores_percentual": 25.0,
        }
        mock_repository.get_enps_distribution.return_value = mock_data

        # Act
        result = service.get_enps_distribution(EMPRESA_ID)

        # Assert
        assert "enps_score" in result
        assert "total_respostas" in result
        assert "promotores" in result
        assert "neutros" in result
        assert "detratores" in result
        assert result["promotores"] == 45
        assert result["neutros"] == 30
        assert result["detratores"] == 25
        assert result["total_respostas"] == 100
        assert result["enps_score"] == 20.0  # 45% - 25%
        mock_repository.get_enps_distribution.assert_called_once_with(EMPRESA_ID)

    def test_get_enps_distribution_success_without_empresa(self, service, mock_repository):
        """Testa get_enps_distribution sem empresa"""
        # Arrange
        mock_data = {
            "promotores": 60,
            "neutros": 20,
            "detratores": 20,
            "promotores_percentual": 60.0,
            "neutros_percentual": 20.0,
            "detratores_percentual": 20.0,
        }
        mock_repository.get_enps_distribution.return_value = mock_data

        # Act
        result = service.get_enps_distribution(None)

        # Assert
        assert result["enps_score"] == 40.0  # 60% - 20%
        assert result["total_respostas"] == 100
        mock_repository.get_enps_distribution.assert_called_once_with(None)

    # ====================
    # get_enps_distribution - FALHA
    # ====================

    def test_get_enps_distribution_empty(self, service, mock_repository):
        """Testa get_enps_distribution sem dados"""
        # Arrange
        mock_repository.get_enps_distribution.return_value = []

        # Act
        result = service.get_enps_distribution(EMPRESA_ID)

        # Assert
        assert result["total_respostas"] == 0
        assert result["promotores"] == 0
        assert result["neutros"] == 0
        assert result["detratores"] == 0
        assert result["enps_score"] == 0

    def test_get_enps_distribution_only_promotores(self, service, mock_repository):
        """Testa get_enps_distribution com apenas promotores"""
        # Arrange
        mock_data = {
            "promotores": 100,
            "neutros": 0,
            "detratores": 0,
            "promotores_percentual": 100.0,
            "neutros_percentual": 0.0,
            "detratores_percentual": 0.0,
        }
        mock_repository.get_enps_distribution.return_value = mock_data

        # Act
        result = service.get_enps_distribution(EMPRESA_ID)

        # Assert
        assert result["enps_score"] == 100.0  # 100% - 0%
        assert result["promotores"] == 100
        assert result["detratores"] == 0

    def test_get_enps_distribution_only_detratores(self, service, mock_repository):
        """Testa get_enps_distribution com apenas detratores"""
        # Arrange
        mock_data = {
            "promotores": 0,
            "neutros": 0,
            "detratores": 50,
            "promotores_percentual": 0.0,
            "neutros_percentual": 0.0,
            "detratores_percentual": 100.0,
        }
        mock_repository.get_enps_distribution.return_value = mock_data

        # Act
        result = service.get_enps_distribution(EMPRESA_ID)

        # Assert
        assert result["enps_score"] == -100.0  # 0% - 100%

    # ====================
    # get_tenure_distribution - SUCESSO
    # ====================

    def test_get_tenure_distribution_success(self, service, mock_repository):
        """Testa get_tenure_distribution com sucesso"""
        # Arrange
        mock_data = [
            {"categoria": "menos de 1 ano", "quantidade": 50},
            {"categoria": "entre 2 e 5 anos", "quantidade": 120},
        ]
        mock_repository.get_tenure_distribution.return_value = mock_data

        # Act
        result = service.get_tenure_distribution(EMPRESA_ID)

        # Assert
        assert "distribuicao" in result
        assert "total_funcionarios" in result
        assert result["total_funcionarios"] == 170
        assert len(result["distribuicao"]) == 2
        mock_repository.get_tenure_distribution.assert_called_once_with(EMPRESA_ID)

    # ====================
    # get_tenure_distribution - FALHA
    # ====================

    def test_get_enps_distribution_empty(self, service, mock_repository):
        """Testa get_enps_distribution sem dados"""
        # Arrange
        mock_data = {
            "promotores": 0,
            "neutros": 0,
            "detratores": 0,
            "promotores_percentual": 0.0,
            "neutros_percentual": 0.0,
            "detratores_percentual": 0.0,
        }
        mock_repository.get_enps_distribution.return_value = mock_data

        # Act
        result = service.get_enps_distribution(EMPRESA_ID)

        # Assert
        assert result["enps_score"] == 0.0
        assert result["total_respostas"] == 0

    # ====================
    # get_satisfaction_scores - SUCESSO
    # ====================

    def test_get_satisfaction_scores_success(self, service, mock_repository):
        """Testa get_satisfaction_scores com sucesso"""
        # Arrange
        mock_data = [
            {"dimensao": "Interesse no Cargo", "score_medio": 6.5},
            {"dimensao": "Contribuição", "score_medio": 6.8},
        ]
        mock_repository.get_satisfaction_scores.return_value = mock_data

        # Act
        result = service.get_satisfaction_scores(EMPRESA_ID)

        # Assert
        assert "dimensoes" in result
        assert "score_geral" in result
        assert len(result["dimensoes"]) == 2
        assert result["score_geral"] == 6.65  # (6.5 + 6.8) / 2
        assert result["total_dimensoes"] == 2
        mock_repository.get_satisfaction_scores.assert_called_once_with(EMPRESA_ID)

    # ====================
    # get_satisfaction_scores - FALHA
    # ====================

    def test_get_satisfaction_scores_empty(self, service, mock_repository):
        """Testa get_satisfaction_scores sem dados"""
        # Arrange
        mock_repository.get_satisfaction_scores.return_value = []

        # Act
        result = service.get_satisfaction_scores(EMPRESA_ID)

        # Assert
        assert result["score_geral"] == 0
        assert result["dimensoes"] == []
        assert result["total_dimensoes"] == 0
        assert result["total_dimensoes"] == 0

    # ====================
    # get_employee_detailed_profile - SUCESSO
    # ====================

    def test_get_employee_detailed_profile_success(self, service, mock_repository):
        """Testa get_employee_detailed_profile com sucesso"""
        # Arrange
        mock_analytics = {
            "employee_scores": [{"dimensao": "Interesse no Cargo", "score": 7.0, "tipo_escala": "NPS", "comentario": "Excelente"}],
            "company_averages": [{"dimensao": "Interesse no Cargo", "score_medio": 6.2}],
            "area_averages": [{"dimensao": "Interesse no Cargo", "score_medio": 6.5}],
            "history": [{"data_avaliacao": "2025-06-15", "score_medio_geral": 7.0}],
            "comments": [
                {
                    "dimensao": "Interesse no Cargo",
                    "score": 7,
                    "comentario": "Excelente",
                    "data_avaliacao": "2025-06-15",
                }
            ],
        }
        mock_repository.get_employee_detailed_analytics.return_value = mock_analytics

        # Act
        result = service.get_employee_detailed_profile(FUNCIONARIO_ID)

        # Assert
        assert "comparison" in result
        assert "history" in result
        assert "comments" in result
        assert "summary" in result
        assert len(result["comments"]) == 1
        assert len(result["comparison"]) == 1
        mock_repository.get_employee_detailed_analytics.assert_called_once_with(FUNCIONARIO_ID)

    # ====================
    # get_employee_detailed_profile - FALHA
    # ====================

    def test_get_employee_detailed_profile_no_data(self, service, mock_repository):
        """Testa get_employee_detailed_profile sem dados"""
        # Arrange
        mock_analytics = {
            "employee_scores": [],
            "company_averages": [],
            "area_averages": [],
            "history": [],
            "comments": [],
        }
        mock_repository.get_employee_detailed_analytics.return_value = mock_analytics

        # Act
        result = service.get_employee_detailed_profile(FUNCIONARIO_ID)

        # Assert
        assert result["comparison"] == []
        assert result["history"] == []
        assert result["summary"]["total_evaluations"] == 0
        assert result["comments"] == []
