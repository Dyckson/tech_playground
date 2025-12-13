"""
Configuração de fixtures pytest globais
"""
import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID
from contextlib import contextmanager
from faker import Faker

fake = Faker('pt_BR')

# UUIDs fixos para testes
EMPRESA_ID = UUID("8841d338-296b-4cb9-a762-70766f978895")
FUNCIONARIO_ID = UUID("938acd06-2090-4deb-9d74-7b4217c2ac25")
AREA_ID = UUID("01160522-3b26-4073-94a6-8692ab6a6e82")
CARGO_ID = UUID("a10a528d-19c9-498c-9f36-b93a2986332f")
DIRETORIA_ID = UUID("1cddea5a-c23b-4335-a9ce-0dd4f8d2c5b7")


@pytest.fixture
def mock_cursor():
    """Mock de cursor PostgreSQL com RealDictCursor"""
    cursor = MagicMock()
    cursor.fetchall.return_value = []
    cursor.fetchone.return_value = None
    cursor.rowcount = 0
    cursor.close.return_value = None
    return cursor


@pytest.fixture
def mock_connection(mock_cursor):
    """Mock de conexão PostgreSQL"""
    conn = MagicMock()
    conn.cursor.return_value = mock_cursor
    conn.commit.return_value = None
    conn.rollback.return_value = None
    return conn


@pytest.fixture
def mock_db_connection(mock_connection):
    """Mock do DatabaseConnection.get_connection()"""
    @contextmanager
    def get_connection():
        yield mock_connection
    
    with patch('app.database.connection.DatabaseConnection.get_connection', get_connection):
        yield mock_connection


@pytest.fixture
def empresa_data():
    """Dados de empresa para testes"""
    return {
        'id': str(EMPRESA_ID),
        'nome': 'CloudServices XYZ',
        'created_at': '2025-12-12T15:29:22.456058'
    }


@pytest.fixture
def funcionario_data():
    """Dados de funcionário para testes"""
    return {
        'id': str(FUNCIONARIO_ID),
        'nome': 'Patricia Lima',
        'email': 'patricia.lima@email.com',
        'email_corporativo': 'patricia.lima@cloudservices.com',
        'funcao': 'PJ',
        'empresa_id': str(EMPRESA_ID),
        'area_detalhe_id': str(AREA_ID),
        'cargo_id': str(CARGO_ID),
        'genero_id': str(UUID('1cf4206a-27c4-45a2-952e-0e14d0952ede')),
        'geracao_id': str(UUID('a8bf32f5-fd32-49eb-8e47-bf166a52232b')),
        'tempo_empresa_id': str(UUID('7b148996-f772-45fd-be31-3d9466c47085')),
        'localidade_id': str(UUID('23ab9902-15a0-417a-9d60-b0bca3d8dde2')),
        'ativo': True,
        'created_at': '2025-12-12T15:29:22.498878',
        'cargo_nome': 'DevOps Engineer',
        'area_nome': 'Azure',
        'localidade_nome': 'Remoto - Internacional',
        'genero_nome': 'Feminino',
        'geracao_nome': 'Millennials',
        'tempo_empresa_nome': '2 a 5 anos'
    }


@pytest.fixture
def area_hierarquia_data():
    """Dados de hierarquia de área para testes"""
    return {
        'empresa': 'CloudServices XYZ',
        'diretoria': 'Operações',
        'gerencia': 'Cloud Infrastructure',
        'coordenacao': 'Infrastructure',
        'area': 'AWS',
        'empresa_id': str(EMPRESA_ID),
        'diretoria_id': str(DIRETORIA_ID),
        'gerencia_id': str(UUID('e0cafe23-90b6-4000-a7a2-aa22372200f8')),
        'coordenacao_id': str(UUID('c083afc2-54a9-44df-88ff-dc404d3be26c')),
        'area_id': str(AREA_ID)
    }


@pytest.fixture
def fake_funcionarios_list(funcionario_data):
    """Lista de funcionários para paginação"""
    funcionarios = []
    for i in range(5):
        func = funcionario_data.copy()
        func['id'] = str(UUID(int=i))
        func['nome'] = fake.name()
        func['email'] = fake.email()
        funcionarios.append(func)
    return funcionarios


@pytest.fixture
def app_client():
    """Cliente de teste FastAPI"""
    from fastapi.testclient import TestClient
    from app.main import app
    
    return TestClient(app)
