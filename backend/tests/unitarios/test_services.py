"""
Testes unitários para Services
"""
import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID
from app.services.funcionario_service import FuncionarioService
from app.services.hierarquia_service import HierarquiaService
from tests.conftest import EMPRESA_ID, FUNCIONARIO_ID, AREA_ID, CARGO_ID


class TestFuncionarioService:
    """Testes para FuncionarioService"""
    
    @pytest.fixture
    def service(self):
        """Instância do FuncionarioService"""
        return FuncionarioService()
    
    @pytest.fixture
    def mock_repository(self, service):
        """Mock do FuncionarioRepository"""
        with patch.object(service, 'repository') as mock_repo:
            yield mock_repo
    
    def test_listar_funcionarios_success(self, service, mock_repository, fake_funcionarios_list):
        """Testa listar_funcionarios com sucesso"""
        # Arrange
        mock_repository.get_funcionarios_paginado.return_value = (fake_funcionarios_list, 5)
        
        # Act
        result = service.listar_funcionarios(
            empresa_id=EMPRESA_ID,
            page=1,
            page_size=10
        )
        
        # Assert
        assert result.total == 5
        assert result.page == 1
        assert result.page_size == 10
        assert result.total_pages == 1
        assert len(result.items) == 5
        mock_repository.get_funcionarios_paginado.assert_called_once_with(
            empresa_id=EMPRESA_ID,
            page=1,
            page_size=10,
            areas=None,
            cargos=None,
            localidades=None
        )
    
    def test_listar_funcionarios_with_filters(self, service, mock_repository, funcionario_data):
        """Testa listar_funcionarios com filtros"""
        # Arrange
        mock_repository.get_funcionarios_paginado.return_value = ([funcionario_data], 1)
        areas = [AREA_ID]
        cargos = [CARGO_ID]
        localidades = [UUID(int=5)]
        
        # Act
        result = service.listar_funcionarios(
            empresa_id=EMPRESA_ID,
            page=1,
            page_size=20,
            areas=areas,
            cargos=cargos,
            localidades=localidades
        )
        
        # Assert
        assert result.total == 1
        assert len(result.items) == 1
        mock_repository.get_funcionarios_paginado.assert_called_once_with(
            empresa_id=EMPRESA_ID,
            page=1,
            page_size=20,
            areas=areas,
            cargos=cargos,
            localidades=localidades
        )
    
    def test_listar_funcionarios_empty(self, service, mock_repository):
        """Testa listar_funcionarios sem resultados"""
        # Arrange
        mock_repository.get_funcionarios_paginado.return_value = ([], 0)
        
        # Act
        result = service.listar_funcionarios(
            empresa_id=EMPRESA_ID,
            page=1,
            page_size=10
        )
        
        # Assert
        assert result.total == 0
        assert result.total_pages == 0
        assert len(result.items) == 0
    
    def test_listar_funcionarios_pagination_calculation(self, service, mock_repository, fake_funcionarios_list):
        """Testa cálculo de paginação"""
        # Arrange
        mock_repository.get_funcionarios_paginado.return_value = (fake_funcionarios_list[:3], 23)
        
        # Act
        result = service.listar_funcionarios(
            empresa_id=EMPRESA_ID,
            page=2,
            page_size=10
        )
        
        # Assert
        assert result.total == 23
        assert result.page == 2
        assert result.page_size == 10
        assert result.total_pages == 3  # 23 / 10 = 3 páginas
    
    def test_buscar_funcionarios_success(self, service, mock_repository, funcionario_data):
        """Testa buscar_funcionarios com sucesso"""
        # Arrange
        mock_repository.buscar_funcionarios.return_value = ([funcionario_data], 1)
        
        # Act
        result = service.buscar_funcionarios(
            empresa_id=EMPRESA_ID,
            termo="Patricia",
            page=1,
            page_size=10
        )
        
        # Assert
        assert result.total == 1
        assert len(result.items) == 1
        assert result.items[0].nome == "Patricia Lima"
        mock_repository.buscar_funcionarios.assert_called_once()
    
    def test_buscar_funcionarios_no_results(self, service, mock_repository):
        """Testa buscar_funcionarios sem resultados"""
        # Arrange
        mock_repository.buscar_funcionarios.return_value = ([], 0)
        
        # Act
        result = service.buscar_funcionarios(
            empresa_id=EMPRESA_ID,
            termo="NaoExiste",
            page=1,
            page_size=10
        )
        
        # Assert
        assert result.total == 0
        assert len(result.items) == 0
    
    def test_obter_funcionario_found(self, service, mock_repository, funcionario_data):
        """Testa obter_funcionario encontrando funcionário"""
        # Arrange
        mock_repository.get_funcionario_by_id.return_value = funcionario_data
        
        # Act
        result = service.obter_funcionario(FUNCIONARIO_ID)
        
        # Assert
        assert result is not None
        assert result.id == UUID(funcionario_data['id'])
        assert result.nome == "Patricia Lima"
        mock_repository.get_funcionario_by_id.assert_called_once_with(FUNCIONARIO_ID)
    
    def test_obter_funcionario_not_found(self, service, mock_repository):
        """Testa obter_funcionario não encontrando funcionário"""
        # Arrange
        mock_repository.get_funcionario_by_id.return_value = None
        
        # Act
        result = service.obter_funcionario(UUID('00000000-0000-0000-0000-000000000000'))
        
        # Assert
        assert result is None
    
    def test_obter_filtros_disponiveis(self, service, mock_repository):
        """Testa obter_filtros_disponiveis"""
        # Arrange
        areas = [{'id': str(AREA_ID), 'nome': 'AWS'}]
        cargos = [{'id': str(CARGO_ID), 'nome': 'DevOps Engineer'}]
        localidades = [{'id': str(UUID(int=5)), 'nome': 'Remoto - Brasil'}]
        
        mock_repository.get_areas_unicas.return_value = areas
        mock_repository.get_cargos_unicos.return_value = cargos
        mock_repository.get_localidades_unicas.return_value = localidades
        
        # Act
        result = service.obter_filtros_disponiveis(EMPRESA_ID)
        
        # Assert
        assert 'areas' in result
        assert 'cargos' in result
        assert 'localidades' in result
        assert len(result['areas']) == 1
        assert len(result['cargos']) == 1
        assert len(result['localidades']) == 1
        assert result['areas'][0].nome == 'AWS'
    
    def test_criar_funcionario_success(self, service, mock_repository):
        """Testa criar_funcionario com sucesso"""
        # Arrange
        from app.schemas.schemas import FuncionarioCreate
        
        novo_funcionario = FuncionarioCreate(
            nome="Novo Funcionário",
            email="novo@email.com",
            email_corporativo="novo@empresa.com",
            funcao="CLT",
            empresa_id=EMPRESA_ID,
            area_detalhe_id=AREA_ID,
            cargo_id=CARGO_ID,
            genero_id=UUID(int=1),
            geracao_id=UUID(int=2),
            tempo_empresa_id=UUID(int=3),
            localidade_id=UUID(int=4)
        )
        
        new_id = 'new-uuid-123'
        mock_repository.criar_funcionario.return_value = new_id
        
        # Act
        result = service.criar_funcionario(novo_funcionario)
        
        # Assert
        assert result == new_id
        mock_repository.criar_funcionario.assert_called_once()


class TestHierarquiaService:
    """Testes para HierarquiaService"""
    
    @pytest.fixture
    def service(self):
        """Instância do HierarquiaService"""
        return HierarquiaService()
    
    @pytest.fixture
    def mock_repository(self, service):
        """Mock do HierarquiaRepository"""
        with patch.object(service, 'repository') as mock_repo:
            yield mock_repo
    
    def test_get_all_empresas(self, service, mock_repository, empresa_data):
        """Testa get_all_empresas"""
        # Arrange
        empresas = [empresa_data, {**empresa_data, 'id': str(UUID(int=2)), 'nome': 'Outra'}]
        mock_repository.get_all_empresas.return_value = empresas
        
        # Act
        result = service.get_all_empresas()
        
        # Assert
        assert len(result) == 2
        assert result[0].nome == 'CloudServices XYZ'
        mock_repository.get_all_empresas.assert_called_once()
    
    def test_get_all_empresas_empty(self, service, mock_repository):
        """Testa get_all_empresas vazio"""
        # Arrange
        mock_repository.get_all_empresas.return_value = []
        
        # Act
        result = service.get_all_empresas()
        
        # Assert
        assert len(result) == 0
    
    def test_get_empresa_found(self, service, mock_repository, empresa_data):
        """Testa get_empresa encontrando empresa"""
        # Arrange
        mock_repository.get_empresa_by_id.return_value = empresa_data
        
        # Act
        result = service.get_empresa(EMPRESA_ID)
        
        # Assert
        assert result is not None
        assert result.id == UUID(empresa_data['id'])
        assert result.nome == 'CloudServices XYZ'
    
    def test_get_empresa_not_found(self, service, mock_repository):
        """Testa get_empresa não encontrando empresa"""
        # Arrange
        mock_repository.get_empresa_by_id.return_value = None
        
        # Act
        result = service.get_empresa(UUID('00000000-0000-0000-0000-000000000000'))
        
        # Assert
        assert result is None
    
    def test_get_arvore_hierarquica_success(self, service, mock_repository):
        """Testa get_arvore_hierarquica com sucesso"""
        # Arrange
        nodes = [
            {
                'empresa_id': str(EMPRESA_ID),
                'empresa_nome': 'CloudServices',
                'diretoria_id': str(UUID(int=1)),
                'diretoria_nome': 'Operações',
                'gerencia_id': str(UUID(int=2)),
                'gerencia_nome': 'Cloud',
                'coordenacao_id': str(UUID(int=3)),
                'coordenacao_nome': 'Infra',
                'area_id': str(AREA_ID),
                'area_nome': 'AWS'
            },
            {
                'empresa_id': str(EMPRESA_ID),
                'empresa_nome': 'CloudServices',
                'diretoria_id': str(UUID(int=1)),
                'diretoria_nome': 'Operações',
                'gerencia_id': str(UUID(int=2)),
                'gerencia_nome': 'Cloud',
                'coordenacao_id': str(UUID(int=3)),
                'coordenacao_nome': 'Infra',
                'area_id': str(UUID(int=10)),
                'area_nome': 'Azure'
            }
        ]
        mock_repository.get_arvore_hierarquica.return_value = nodes
        
        # Act
        result = service.get_arvore_hierarquica(EMPRESA_ID)
        
        # Assert
        assert len(result) == 1  # 1 diretoria
        assert result[0]['nome'] == 'Operações'
        assert len(result[0]['gerencias']) == 1
        assert len(result[0]['gerencias'][0]['coordenacoes']) == 1
        assert len(result[0]['gerencias'][0]['coordenacoes'][0]['areas']) == 2
    
    def test_get_arvore_hierarquica_empty(self, service, mock_repository):
        """Testa get_arvore_hierarquica vazio"""
        # Arrange
        mock_repository.get_arvore_hierarquica.return_value = []
        
        # Act
        result = service.get_arvore_hierarquica(EMPRESA_ID)
        
        # Assert
        assert result == []


class TestFuncionarioServiceFailures:
    """Testes de casos de falha para FuncionarioService"""
    
