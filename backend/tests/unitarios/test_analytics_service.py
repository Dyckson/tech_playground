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

    # ====================
    # Task 7 - get_areas_scores_comparison - SUCESSO
    # ====================

    def test_get_areas_scores_comparison_success_with_empresa(self, service, mock_repository):
        """Testa comparação de scores por área com sucesso"""
        # Arrange
        mock_data = [
            {"id_area_detalhe": "a1", "area_nome": "Vendas", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Dir", "dimensao": "Liderança", "score_medio": 7.5, "total_funcionarios": 10, "total_respostas": 20},
            {"id_area_detalhe": "a1", "area_nome": "Vendas", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Dir", "dimensao": "Ambiente", "score_medio": 8.0, "total_funcionarios": 10, "total_respostas": 20},
            {"id_area_detalhe": "a2", "area_nome": "TI", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Dir", "dimensao": "Liderança", "score_medio": 6.5, "total_funcionarios": 15, "total_respostas": 30},
        ]
        mock_repository.get_areas_scores_comparison.return_value = mock_data

        # Act
        result = service.get_areas_scores_comparison(EMPRESA_ID)

        # Assert
        assert "areas" in result
        assert len(result["areas"]) == 2  # 2 áreas únicas
        assert result["areas"][0]["area_nome"] == "Vendas"
        assert len(result["areas"][0]["dimensoes"]) == 2
        assert result["areas"][0]["score_medio_geral"] == 7.75  # (7.5 + 8.0) / 2
        assert result["areas"][1]["area_nome"] == "TI"
        assert result["areas"][1]["score_medio_geral"] == 6.5
        mock_repository.get_areas_scores_comparison.assert_called_once_with(EMPRESA_ID)

    def test_get_areas_scores_comparison_success_without_empresa(self, service, mock_repository):
        """Testa comparação de scores sem filtro de empresa"""
        # Arrange
        mock_data = [
            {"id_area_detalhe": "a3", "area_nome": "RH", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Dir", "dimensao": "Liderança", "score_medio": 8.5, "total_funcionarios": 12, "total_respostas": 24},
        ]
        mock_repository.get_areas_scores_comparison.return_value = mock_data

        # Act
        result = service.get_areas_scores_comparison(None)

        # Assert
        assert len(result["areas"]) == 1
        assert result["areas"][0]["score_medio_geral"] == 8.5
        mock_repository.get_areas_scores_comparison.assert_called_once_with(None)

    def test_get_areas_scores_comparison_empty(self, service, mock_repository):
        """Testa comparação quando não há dados"""
        # Arrange
        mock_repository.get_areas_scores_comparison.return_value = []

        # Act
        result = service.get_areas_scores_comparison(EMPRESA_ID)

        # Assert
        assert result["areas"] == []

    # ====================
    # Task 7 - get_areas_enps_comparison - SUCESSO
    # ====================

    def test_get_areas_enps_comparison_success(self, service, mock_repository):
        """Testa comparação de eNPS por área com sucesso"""
        # Arrange
        mock_data = [
            {"id_area_detalhe": "a1", "area_nome": "Marketing", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Comercial", "promotores": 60, "neutros": 30, "detratores": 10, "promotores_percentual": 60.0, "neutros_percentual": 30.0, "detratores_percentual": 10.0, "total_respostas": 100},
            {"id_area_detalhe": "a2", "area_nome": "Financeiro", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Administrativo", "promotores": 30, "neutros": 40, "detratores": 30, "promotores_percentual": 30.0, "neutros_percentual": 40.0, "detratores_percentual": 30.0, "total_respostas": 100},
        ]
        mock_repository.get_areas_enps_comparison.return_value = mock_data

        # Act
        result = service.get_areas_enps_comparison(EMPRESA_ID)

        # Assert
        assert "areas" in result
        assert "melhor_area" in result
        assert "pior_area" in result
        assert "enps_medio" in result
        assert len(result["areas"]) == 2
        assert result["areas"][0]["enps_score"] == 50.0  # (60 - 10)
        assert result["areas"][1]["enps_score"] == 0.0  # (30 - 30)
        assert result["melhor_area"]["area_nome"] == "Marketing"
        assert result["melhor_area"]["enps_score"] == 50.0
        assert result["pior_area"]["area_nome"] == "Financeiro"
        assert result["enps_medio"] == 25.0  # (50 + 0) / 2
        mock_repository.get_areas_enps_comparison.assert_called_once_with(EMPRESA_ID)

    def test_get_areas_enps_comparison_single_area(self, service, mock_repository):
        """Testa eNPS quando há apenas uma área"""
        # Arrange
        mock_data = [
            {"id_area_detalhe": "a1", "area_nome": "Única", "nome_coordenacao": "Coord", "nome_gerencia": "Ger", "nome_diretoria": "Geral", "promotores": 70, "neutros": 20, "detratores": 10, "promotores_percentual": 70.0, "neutros_percentual": 20.0, "detratores_percentual": 10.0, "total_respostas": 100}
        ]
        mock_repository.get_areas_enps_comparison.return_value = mock_data

        # Act
        result = service.get_areas_enps_comparison(None)

        # Assert
        assert len(result["areas"]) == 1
        assert result["melhor_area"]["area_nome"] == "Única"
        assert result["pior_area"]["area_nome"] == "Única"
        assert result["enps_medio"] == 60.0

    def test_get_areas_enps_comparison_empty(self, service, mock_repository):
        """Testa eNPS quando não há dados"""
        # Arrange
        mock_repository.get_areas_enps_comparison.return_value = []

        # Act
        result = service.get_areas_enps_comparison(EMPRESA_ID)

        # Assert
        assert result["areas"] == []
        assert result["melhor_area"] is None
        assert result["pior_area"] is None
        assert result["enps_medio"] == 0

    # ====================
    # Task 7 - get_area_detailed_metrics - SUCESSO
    # ====================

    def test_get_area_detailed_metrics_success(self, service, mock_repository):
        """Testa métricas detalhadas de área com sucesso"""
        # Arrange
        area_id = "area-123"
        mock_data = {
            "area_info": {
                "area_nome": "Logística",
                "nome_coordenacao": "Coord Logística",
                "nome_gerencia": "Ger Operações",
                "nome_diretoria": "Dir Operações",
                "total_funcionarios": 25,
            },
            "enps": {
                "promotores": 15,
                "neutros": 8,
                "detratores": 2,
            },
            "area_scores": [
                {"dimensao": "Liderança", "score_medio": 7.2, "total_respostas": 20, "total_funcionarios": 25},
                {"dimensao": "Ambiente", "score_medio": 8.0, "total_respostas": 20, "total_funcionarios": 25},
            ],
            "company_averages": [
                {"dimensao": "Liderança", "score_medio": 6.8},
                {"dimensao": "Ambiente", "score_medio": 7.5},
            ],
        }
        mock_repository.get_area_detailed_metrics.return_value = mock_data

        # Act
        result = service.get_area_detailed_metrics(area_id)

        # Assert
        assert "area_info" in result
        assert "enps" in result
        assert "scores_comparison" in result
        assert result["area_info"]["area_nome"] == "Logística"
        assert result["enps"]["enps_score"] == 52.0  # (15/25)*100 - (2/25)*100
        assert result["enps"]["promotores"] == 15
        assert len(result["scores_comparison"]) == 2
        mock_repository.get_area_detailed_metrics.assert_called_once_with(area_id)

    def test_get_area_detailed_metrics_no_funcionarios(self, service, mock_repository):
        """Testa métricas quando área não tem funcionários"""
        # Arrange
        area_id = "area-empty"
        mock_data = {
            "area_info": {
                "area_nome": "Nova Área",
                "nome_coordenacao": "Coord Expansão",
                "nome_gerencia": "Ger Expansão",
                "nome_diretoria": "Dir Expansão",
                "total_funcionarios": 0,
            },
            "enps": {
                "promotores": 0,
                "neutros": 0,
                "detratores": 0,
            },
            "area_scores": [],
            "company_averages": [],
        }
        mock_repository.get_area_detailed_metrics.return_value = mock_data

        # Act
        result = service.get_area_detailed_metrics(area_id)

        # Assert
        assert result["area_info"]["total_funcionarios"] == 0
        assert result["enps"]["enps_score"] == 0
        assert len(result["scores_comparison"]) == 0

    def test_get_area_detailed_metrics_area_not_found(self, service, mock_repository):
        """Testa métricas quando área não existe"""
        # Arrange
        area_id = "area-404"
        mock_data = {
            "area_info": None,
            "enps": {"promotores": 0, "neutros": 0, "detratores": 0},
            "area_scores": [],
            "company_averages": [],
        }
        mock_repository.get_area_detailed_metrics.return_value = mock_data

        # Act
        result = service.get_area_detailed_metrics(area_id)

        # Assert
        assert result["area_info"] is None
