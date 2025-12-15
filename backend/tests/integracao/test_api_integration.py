"""
Testes de integração da API
Testa endpoints end-to-end com requisições HTTP reais e banco de dados real
"""

import pytest


class TestHealthEndpoint:
    """Testes do endpoint de health check"""

    def test_health_check_returns_200(self, api_client):
        """Testa se health check retorna 200"""
        response = api_client.get("/health")
        assert response.status_code == 200

    def test_health_check_response_format(self, api_client):
        """Testa formato da resposta do health check"""
        response = api_client.get("/health")
        data = response.json()

        assert "status" in data
        assert data["status"] == "healthy"


class TestFuncionariosEndpoint:
    """Testes do endpoint de funcionários"""

    def test_listar_funcionarios_returns_200(self, api_client):
        """Testa listagem de funcionários"""
        response = api_client.get("/api/v1/funcionarios")
        assert response.status_code == 200

    def test_listar_funcionarios_returns_data(self, api_client):
        """Testa se retorna dados de funcionários"""
        response = api_client.get("/api/v1/funcionarios")
        data = response.json()

        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)
        assert len(data["items"]) > 0

    def test_listar_funcionarios_pagination(self, api_client):
        """Testa paginação de funcionários"""
        response = api_client.get("/api/v1/funcionarios?page=1&page_size=10")
        data = response.json()

        assert data["page"] == 1
        assert data["page_size"] == 10
        assert "total" in data
        assert "total_pages" in data

    def test_listar_funcionarios_with_filters(self, api_client):
        """Testa filtros de funcionários"""
        response = api_client.get("/api/v1/funcionarios?cargo=Desenvolvedor Sênior")
        data = response.json()

        assert response.status_code == 200
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_obter_funcionario_by_id(self, api_client, funcionario_id_teste):
        """Testa obter funcionário por ID"""
        if not funcionario_id_teste:
            pytest.skip("Nenhum funcionário encontrado no banco")

        response = api_client.get(f"/api/v1/funcionarios/{funcionario_id_teste}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == funcionario_id_teste
        assert "nome" in data
        assert "email" in data

    def test_obter_funcionario_not_found(self, api_client):
        """Testa funcionário não encontrado"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = api_client.get(f"/api/v1/funcionarios/{fake_id}")
        assert response.status_code == 404

    def test_buscar_funcionarios(self, api_client):
        """Testa busca de funcionários por termo"""
        response = api_client.get("/api/v1/funcionarios/buscar?termo=silva")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert "total" in data

    def test_buscar_funcionarios_termo_muito_curto(self, api_client):
        """Testa busca com termo curto (2 caracteres) - aceito pelo sistema"""
        response = api_client.get("/api/v1/funcionarios/buscar?termo=ab")
        assert response.status_code == 200  # Sistema aceita termos com 2+ caracteres
        data = response.json()
        assert "items" in data
        assert "total" in data

    def test_obter_filtros_disponiveis(self, api_client):
        """Testa obtenção de filtros disponíveis"""
        response = api_client.get("/api/v1/funcionarios/filtros")
        assert response.status_code == 200

        data = response.json()
        assert "areas" in data
        assert "cargos" in data
        assert "localidades" in data


class TestHierarquiaEndpoint:
    """Testes do endpoint de hierarquia organizacional"""

    def test_listar_empresas(self, api_client):
        """Testa listagem de empresas"""
        response = api_client.get("/api/v1/hierarquia/empresas")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_obter_empresa_by_id(self, api_client, empresa_id_teste):
        """Testa obter empresa por ID"""
        if not empresa_id_teste:
            pytest.skip("Nenhuma empresa encontrada no banco")

        response = api_client.get(f"/api/v1/hierarquia/empresas/{empresa_id_teste}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == empresa_id_teste
        assert "nome" in data

    def test_obter_arvore_hierarquica(self, api_client, empresa_id_teste):
        """Testa obtenção da árvore hierárquica"""
        if not empresa_id_teste:
            pytest.skip("Nenhuma empresa encontrada no banco")

        response = api_client.get(f"/api/v1/hierarquia/empresas/{empresa_id_teste}/arvore")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)  # API retorna lista de diretorias
        if len(data) > 0:
            assert "gerencias" in data[0]

    def test_listar_areas(self, api_client, empresa_id_teste):
        """Testa listagem de áreas de uma empresa"""
        if not empresa_id_teste:
            pytest.skip("Nenhuma empresa encontrada no banco")

        response = api_client.get(f"/api/v1/hierarquia/empresas/{empresa_id_teste}/areas")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

    def test_contagem_funcionarios_por_area(self, api_client, empresa_id_teste):
        """Testa contagem de funcionários por área"""
        if not empresa_id_teste:
            pytest.skip("Nenhuma empresa encontrada no banco")

        response = api_client.get(f"/api/v1/hierarquia/empresas/{empresa_id_teste}/funcionarios/contagem")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)


class TestEndToEndFlow:
    """Testes de fluxo end-to-end completo"""

    def test_complete_flow_empresa_to_funcionarios(self, api_client):
        """Testa fluxo completo: listar empresa → árvore → funcionários"""
        # 1. Lista empresas
        response = api_client.get("/api/v1/hierarquia/empresas")
        assert response.status_code == 200
        empresas = response.json()
        assert len(empresas) > 0

        empresa_id = empresas[0]["id"]

        # 2. Obtém árvore hierárquica
        response = api_client.get(f"/api/v1/hierarquia/empresas/{empresa_id}/arvore")
        assert response.status_code == 200
        arvore = response.json()
        assert isinstance(arvore, list)  # API retorna lista de diretorias

        # 3. Lista funcionários
        response = api_client.get("/api/v1/funcionarios")
        assert response.status_code == 200
        funcionarios = response.json()
        assert "items" in funcionarios
        assert len(funcionarios["items"]) > 0

    def test_complete_flow_search_and_filter(self, api_client):
        """Testa fluxo: buscar funcionário → filtrar por cargo"""
        # 1. Busca funcionários
        response = api_client.get("/api/v1/funcionarios/buscar?termo=silva")
        assert response.status_code == 200

        # 2. Obtém filtros disponíveis
        response = api_client.get("/api/v1/funcionarios/filtros")
        assert response.status_code == 200
        filtros = response.json()

        # 3. Filtra por cargo (se houver cargos disponíveis)
        if filtros["cargos"]:
            cargo = filtros["cargos"][0]
            response = api_client.get(f"/api/v1/funcionarios?cargo={cargo}")
            assert response.status_code == 200


class TestAPIErrorHandling:
    """Testes de tratamento de erros da API"""

    def test_invalid_uuid_format(self, api_client):
        """Testa UUID inválido"""
        response = api_client.get("/api/v1/funcionarios/invalid-uuid")
        assert response.status_code == 422

    def test_invalid_pagination_params(self, api_client):
        """Testa parâmetros de paginação inválidos"""
        response = api_client.get("/api/v1/funcionarios?page=-1")
        assert response.status_code == 422

        response = api_client.get("/api/v1/funcionarios?page_size=0")
        assert response.status_code == 422

    def test_page_size_too_large(self, api_client):
        """Testa page_size muito grande"""
        response = api_client.get("/api/v1/funcionarios?page_size=1000")
        assert response.status_code == 422


class TestAnalyticsEndpoints:
    """Testes dos endpoints de analytics (Task 7)"""

    def test_get_enps_success(self, api_client):
        """Testa obtenção de eNPS geral"""
        response = api_client.get("/api/v1/analytics/enps")
        assert response.status_code == 200

        data = response.json()
        assert "enps_score" in data
        assert "promotores" in data
        assert "neutros" in data
        assert "detratores" in data
        assert "total_respostas" in data

    def test_get_enps_with_empresa_filter(self, api_client, empresa_id_teste):
        """Testa obtenção de eNPS filtrado por empresa"""
        if not empresa_id_teste:
            pytest.skip("Nenhuma empresa encontrada no banco")

        response = api_client.get(f"/api/v1/analytics/enps?id_empresa={empresa_id_teste}")
        assert response.status_code == 200

        data = response.json()
        assert "enps_score" in data
        assert isinstance(data["enps_score"], (int, float)) or data["enps_score"] is None

    def test_get_areas_scores_comparison_success(self, api_client):
        """Testa comparação de scores entre áreas"""
        response = api_client.get("/api/v1/analytics/areas/scores-comparison")
        assert response.status_code == 200

        data = response.json()
        assert "areas" in data
        assert isinstance(data["areas"], list)
        if len(data["areas"]) > 0:
            area = data["areas"][0]
            assert "area_id" in area
            assert "area_nome" in area
            assert "coordenacao" in area
            assert "dimensoes" in area

    def test_get_areas_scores_comparison_with_empresa(self, api_client, empresa_id_teste):
        """Testa comparação de scores filtrada por empresa"""
        if not empresa_id_teste:
            pytest.skip("Nenhuma empresa encontrada no banco")

        response = api_client.get(
            f"/api/v1/analytics/areas/scores-comparison?id_empresa={empresa_id_teste}"
        )
        assert response.status_code == 200

        data = response.json()
        assert "areas" in data
        assert isinstance(data["areas"], list)

    def test_get_areas_enps_comparison_success(self, api_client):
        """Testa comparação de eNPS entre áreas"""
        response = api_client.get("/api/v1/analytics/areas/enps-comparison")
        assert response.status_code == 200

        data = response.json()
        assert "areas" in data
        assert isinstance(data["areas"], list)
        if len(data["areas"]) > 0:
            area = data["areas"][0]
            assert "area_id" in area
            assert "area_nome" in area
            assert "coordenacao" in area
            assert "enps_score" in area
            assert "promotores" in area
            assert "neutros" in area
            assert "detratores" in area

    def test_get_areas_enps_comparison_with_empresa(self, api_client, empresa_id_teste):
        """Testa comparação de eNPS filtrada por empresa"""
        if not empresa_id_teste:
            pytest.skip("Nenhuma empresa encontrada no banco")

        response = api_client.get(
            f"/api/v1/analytics/areas/enps-comparison?id_empresa={empresa_id_teste}"
        )
        assert response.status_code == 200

        data = response.json()
        assert "areas" in data
        assert isinstance(data["areas"], list)

    def test_get_area_detailed_metrics_success(self, api_client, area_id_teste):
        """Testa obtenção de métricas detalhadas de uma área"""
        if not area_id_teste:
            pytest.skip("Nenhuma área encontrada no banco")

        response = api_client.get(
            f"/api/v1/analytics/areas/{area_id_teste}/detailed-metrics"
        )
        assert response.status_code == 200

        data = response.json()
        assert "area_info" in data
        assert "enps" in data
        assert "scores_comparison" in data
        
        # Verificar estrutura area_info
        area_info = data["area_info"]
        assert "area_nome" in area_info
        assert "nome_coordenacao" in area_info

    def test_get_area_detailed_metrics_not_found(self, api_client):
        """Testa métricas detalhadas para área inexistente - retorna 200 com dados vazios"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = api_client.get(
            f"/api/v1/analytics/areas/{fake_id}/detailed-metrics"
        )
        assert response.status_code == 200
        data = response.json()
        assert "enps" in data
        assert data["enps"]["total_respostas"] == 0

    def test_get_area_detailed_metrics_invalid_uuid(self, api_client):
        """Testa métricas detalhadas com UUID inválido"""
        response = api_client.get(
            "/api/v1/analytics/areas/invalid-uuid/detailed-metrics"
        )
        assert response.status_code == 422


class TestAnalyticsEndToEnd:
    """Testes de fluxo end-to-end de analytics"""

    def test_complete_analytics_flow(self, api_client, empresa_id_teste):
        """Testa fluxo completo: eNPS → comparação de áreas → métricas detalhadas"""
        # 1. Obtém eNPS geral
        response = api_client.get("/api/v1/analytics/enps")
        assert response.status_code == 200
        enps_data = response.json()
        assert "enps_score" in enps_data

        # 2. Compara scores entre áreas
        response = api_client.get("/api/v1/analytics/areas/scores-comparison")
        assert response.status_code == 200
        scores_data = response.json()
        assert "areas" in scores_data
        assert isinstance(scores_data["areas"], list)

        # 3. Compara eNPS entre áreas
        response = api_client.get("/api/v1/analytics/areas/enps-comparison")
        assert response.status_code == 200
        enps_comparison_data = response.json()
        assert "areas" in enps_comparison_data
        assert isinstance(enps_comparison_data["areas"], list)

        # 4. Se houver áreas, obtém métricas detalhadas da primeira
        if len(scores_data["areas"]) > 0:
            area_id = scores_data["areas"][0]["area_id"]
            response = api_client.get(
                f"/api/v1/analytics/areas/{area_id}/detailed-metrics"
            )
            assert response.status_code == 200
            detailed_data = response.json()
            assert "enps" in detailed_data
            assert "scores_comparison" in detailed_data
            assert "area_info" in detailed_data

    def test_analytics_with_empresa_filter_flow(self, api_client, empresa_id_teste):
        """Testa fluxo de analytics filtrado por empresa"""
        if not empresa_id_teste:
            pytest.skip("Nenhuma empresa encontrada no banco")

        # 1. eNPS da empresa
        response = api_client.get(
            f"/api/v1/analytics/enps?id_empresa={empresa_id_teste}"
        )
        assert response.status_code == 200

        # 2. Comparação de scores da empresa
        response = api_client.get(
            f"/api/v1/analytics/areas/scores-comparison?id_empresa={empresa_id_teste}"
        )
        assert response.status_code == 200

        # 3. Comparação de eNPS da empresa
        response = api_client.get(
            f"/api/v1/analytics/areas/enps-comparison?id_empresa={empresa_id_teste}"
        )
        assert response.status_code == 200
