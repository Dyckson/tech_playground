"""
Fixtures para testes de integração
Usa conexões reais com o banco de dados e cliente HTTP real
"""
import pytest
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.testclient import TestClient
from typing import Generator
import os


@pytest.fixture(scope="session")
def db_connection_string() -> str:
    """String de conexão com o banco de dados de testes"""
    return (
        f"postgresql://{os.getenv('DB_USER', 'tech_user')}:"
        f"{os.getenv('DB_PASSWORD', 'tech_password')}@"
        f"{os.getenv('DB_HOST', 'postgres')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'tech_playground')}"
    )


@pytest.fixture(scope="session")
def db_connection(db_connection_string) -> Generator:
    """
    Conexão real com o banco de dados PostgreSQL
    Escopo: session - uma conexão para toda a sessão de testes
    """
    conn = psycopg2.connect(db_connection_string)
    conn.autocommit = False
    yield conn
    conn.close()


@pytest.fixture(scope="function")
def db_cursor(db_connection) -> Generator:
    """
    Cursor para executar queries no banco de dados
    Escopo: function - cada teste tem seu próprio cursor com transação isolada
    """
    cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    yield cursor
    db_connection.rollback()  # Rollback após cada teste
    cursor.close()


@pytest.fixture(scope="session")
def api_client() -> TestClient:
    """
    Cliente HTTP real para testes de API
    Usa o app FastAPI real com conexões reais ao banco
    """
    from app.main import app
    return TestClient(app)


@pytest.fixture(scope="function")
def db_transaction(db_connection) -> Generator:
    """
    Fixture para testes que precisam de transação explícita
    Faz rollback automático após o teste
    """
    db_connection.rollback()  # Garante estado limpo
    yield db_connection
    db_connection.rollback()  # Desfaz mudanças do teste


@pytest.fixture(scope="session")
def empresa_id_teste(db_connection) -> str:
    """
    Retorna o ID de uma empresa real do banco para usar nos testes
    """
    cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id_empresa FROM empresa LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    if result:
        return str(result['id_empresa'])
    return None


@pytest.fixture(scope="session")
def funcionario_id_teste(db_connection) -> str:
    """
    Retorna o ID de um funcionário real do banco para usar nos testes
    """
    cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id_funcionario FROM funcionario LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    if result:
        return str(result['id_funcionario'])
    return None
