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


    # ============================================
    # Tests para Task 7 - Area Level Analytics
    # ============================================

    def test_get_areas_scores_comparison_with_empresa(self, repository, mock_db_connection, mock_cursor):
        """Testa comparação de scores por área com filtro de empresa"""
        # Arrange
        empresa_id = "550e8400-e29b-41d4-a716-446655440000"
        mock_cursor.fetchall.return_value = [
            {
                "id_area_detalhe": "area-123",
                "area_nome": "Vendas",
                "nome_coordenacao": "Coord Vendas",
                "nome_gerencia": "Ger Comercial",
                "nome_diretoria": "Dir Comercial",
                "dimensao": "Liderança",
                "score_medio": 7.5,
                "total_funcionarios": 10,
                "total_respostas": 20,
            },
            {
                "id_area_detalhe": "area-123",
                "area_nome": "Vendas",
                "nome_coordenacao": "Coord Vendas",
                "nome_gerencia": "Ger Comercial",
                "nome_diretoria": "Dir Comercial",
                "dimensao": "Ambiente",
                "score_medio": 8.0,
                "total_funcionarios": 10,
                "total_respostas": 20,
            },
        ]

        # Act
        result = repository.get_areas_scores_comparison(empresa_id)

        # Assert
        assert len(result) == 2
        assert result[0]["area_nome"] == "Vendas"
        assert result[0]["score_medio"] == 7.5
        mock_cursor.execute.assert_called_once()
        assert empresa_id in str(mock_cursor.execute.call_args)


    def test_get_areas_scores_comparison_without_empresa(self, repository, mock_db_connection, mock_cursor):
        """Testa comparação de scores por área sem filtro de empresa"""
        # Arrange
        mock_cursor.fetchall.return_value = [
        {
            "id_area_detalhe": "area-456",
            "area_nome": "TI",
            "nome_coordenacao": "Coord TI",
            "nome_gerencia": "Ger Tecnologia",
            "nome_diretoria": "Dir Tecnologia",
            "dimensao": "Liderança",
            "score_medio": 6.5,
            "total_funcionarios": 15,
            "total_respostas": 30,
        }
        ]

        # Act
        result = repository.get_areas_scores_comparison(None)

        # Assert
        assert len(result) == 1
        assert result[0]["area_nome"] == "TI"
        mock_cursor.execute.assert_called_once()

    def test_get_areas_scores_comparison_empty(self, repository, mock_db_connection, mock_cursor):
        """Testa comparação de scores quando não há dados"""
        # Arrange
        mock_cursor.fetchall.return_value = []

        # Act
        result = repository.get_areas_scores_comparison(None)

        # Assert
        assert len(result) == 0
        mock_cursor.execute.assert_called_once()

    def test_get_areas_enps_comparison_with_empresa(self, repository, mock_db_connection, mock_cursor):
        """Testa comparação de eNPS por área com filtro de empresa"""
        # Arrange
        empresa_id = "550e8400-e29b-41d4-a716-446655440000"
        mock_cursor.fetchall.return_value = [
        {
            "id_area_detalhe": "area-789",
            "area_nome": "Marketing",
            "nome_coordenacao": "Coord Marketing",
            "nome_gerencia": "Ger Comercial",
            "nome_diretoria": "Dir Comercial",
            "promotores": 60,
            "neutros": 30,
            "detratores": 10,
            "promotores_percentual": 60.0,
            "neutros_percentual": 30.0,
            "detratores_percentual": 10.0,
            "total_respostas": 100,
        }
        ]

        # Act
        result = repository.get_areas_enps_comparison(empresa_id)

        # Assert
        assert len(result) == 1
        assert result[0]["area_nome"] == "Marketing"
        assert result[0]["promotores"] == 60
        assert result[0]["detratores"] == 10
        mock_cursor.execute.assert_called_once()
        assert empresa_id in str(mock_cursor.execute.call_args)


    def test_get_areas_enps_comparison_without_empresa(self, repository, mock_db_connection, mock_cursor):
        """Testa comparação de eNPS por área sem filtro"""
        # Arrange
        mock_cursor.fetchall.return_value = [
        {
            "id_area_detalhe": "area-101",
            "area_nome": "RH",
            "nome_coordenacao": "Coord RH",
            "nome_gerencia": "Ger Pessoas",
            "nome_diretoria": "Dir Pessoas",
            "promotores": 40,
            "neutros": 40,
            "detratores": 20,
            "promotores_percentual": 40.0,
            "neutros_percentual": 40.0,
            "detratores_percentual": 20.0,
            "total_respostas": 50,
        }
        ]

        # Act
        result = repository.get_areas_enps_comparison(None)

        # Assert
        assert len(result) == 1
        assert result[0]["area_nome"] == "RH"
        mock_cursor.execute.assert_called_once()


    def test_get_areas_enps_comparison_empty(self, repository, mock_db_connection, mock_cursor):
        """Testa comparação de eNPS quando não há dados"""
        # Arrange
        mock_cursor.fetchall.return_value = []

        # Act
        result = repository.get_areas_enps_comparison(None)

        # Assert
        assert len(result) == 0


    def test_get_areas_enps_comparison_only_promotores(self, repository, mock_db_connection, mock_cursor):
        """Testa eNPS quando só há promotores (eNPS = 100)"""
        # Arrange
        mock_cursor.fetchall.return_value = [
        {
            "id_area_detalhe": "area-202",
            "area_nome": "Inovação",
            "nome_coordenacao": "Coord Inovação",
            "nome_gerencia": "Ger Tecnologia",
            "nome_diretoria": "Dir Tecnologia",
            "promotores": 50,
            "neutros": 0,
            "detratores": 0,
            "promotores_percentual": 100.0,
            "neutros_percentual": 0.0,
            "detratores_percentual": 0.0,
            "total_respostas": 50,
        }
        ]

        # Act
        result = repository.get_areas_enps_comparison(None)

        # Assert
        assert result[0]["promotores"] == 50
        assert result[0]["detratores"] == 0


    def test_get_area_detailed_metrics_complete(self, repository, mock_db_connection, mock_cursor):
        """Testa métricas detalhadas de área com dados completos"""
        # Arrange
        area_id = "area-303"
        mock_cursor.fetchall.side_effect = [
        # area_scores
        [
            {"dimensao": "Liderança", "score_medio": 7.2, "total_respostas": 20, "total_funcionarios": 25},
            {"dimensao": "Ambiente", "score_medio": 8.0, "total_respostas": 20, "total_funcionarios": 25},
        ],
        # company_averages
        [
            {"dimensao": "Liderança", "score_medio": 6.8},
            {"dimensao": "Ambiente", "score_medio": 7.5},
        ],
        # enps
        [{"detratores": 2, "neutros": 8, "promotores": 15}],
        # area_info
        [
            {
                "area_nome": "Logística",
                "nome_coordenacao": "Coord Logística",
                "nome_gerencia": "Ger Operações",
                "nome_diretoria": "Dir Operações",
                "total_funcionarios": 25,
            }
        ],
        ]

        # Act
        result = repository.get_area_detailed_metrics(area_id)

        # Assert
        assert result["area_info"]["area_nome"] == "Logística"
        assert result["area_info"]["total_funcionarios"] == 25
        assert result["enps"]["promotores"] == 15
        assert len(result["area_scores"]) == 2
        assert mock_cursor.execute.call_count == 4


    def test_get_area_detailed_metrics_no_funcionarios(self, repository, mock_db_connection, mock_cursor):
        """Testa métricas de área sem funcionários"""
        # Arrange
        area_id = "area-404"
        mock_cursor.fetchall.side_effect = [
        [],  # area_scores
        [{"dimensao": "Liderança", "score_medio": 7.0}],  # company_averages
        [{"detratores": 0, "neutros": 0, "promotores": 0}],  # enps
        [
            {
                "area_nome": "Nova Área",
                "nome_coordenacao": "Coord Expansão",
                "nome_gerencia": "Ger Expansão",
                "nome_diretoria": "Dir Expansão",
                "total_funcionarios": 0,
            }
        ],  # area_info
        ]

        # Act
        result = repository.get_area_detailed_metrics(area_id)

        # Assert
        assert result["area_info"]["total_funcionarios"] == 0
        assert len(result["area_scores"]) == 0


    def test_get_area_detailed_metrics_area_not_found(self, repository, mock_db_connection, mock_cursor):
        """Testa métricas quando área não existe"""
        # Arrange
        area_id = "area-nao-existe"
        mock_cursor.fetchall.side_effect = [
        [],  # area_scores
        [{"dimensao": "Liderança", "score_medio": 7.0}],  # company_averages
        [{"detratores": 0, "neutros": 0, "promotores": 0}],  # enps
        [],  # area_info (vazio = não encontrada)
        ]

        # Act
        result = repository.get_area_detailed_metrics(area_id)

        # Assert
        assert result["area_info"] is None
