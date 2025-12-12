"""
Gerenciamento de conexões com o banco de dados PostgreSQL
"""
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Gerencia pool de conexões com PostgreSQL"""
    
    _pool = None
    
    @classmethod
    def init_pool(cls, minconn=2, maxconn=10):
        """Inicializa o pool de conexões"""
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(
                    minconn,
                    maxconn,
                    host=settings.DB_HOST,
                    port=settings.DB_PORT,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    database=settings.DB_NAME,
                    cursor_factory=RealDictCursor
                )
                logger.info(f"✅ Pool de conexões inicializado ({minconn}-{maxconn} conexões)")
            except Exception as e:
                logger.error(f"❌ Erro ao inicializar pool: {e}")
                raise
    
    @classmethod
    @contextmanager
    def get_connection(cls):
        """Context manager para obter conexão do pool"""
        if cls._pool is None:
            cls.init_pool()
        
        conn = None
        try:
            conn = cls._pool.getconn()
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"❌ Erro na conexão: {e}")
            raise
        finally:
            if conn:
                cls._pool.putconn(conn)
    
    @classmethod
    def close_all(cls):
        """Fecha todas as conexões do pool"""
        if cls._pool:
            cls._pool.closeall()
            logger.info("✅ Pool de conexões fechado")


def get_db_connection():
    """Helper para obter conexão (dependency injection)"""
    return DatabaseConnection.get_connection()
