"""
Base Repository
Classe base com métodos comuns para acesso a dados
"""

import logging
from typing import Any

from app.database.connection import DatabaseConnection


logger = logging.getLogger(__name__)


class BaseRepository:
    """Repositório base com operações CRUD genéricas"""

    def __init__(self):
        self.db = DatabaseConnection

    def execute_query(self, query: str, params: tuple | None = None) -> list[dict[str, Any]]:
        """
        Executa query SELECT e retorna lista de dicionários
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            return [dict(row) for row in results]

    def execute_one(self, query: str, params: tuple | None = None) -> dict[str, Any] | None:
        """
        Executa query SELECT e retorna um único registro
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            cursor.close()
            return dict(result) if result else None

    def execute_insert(self, query: str, params: tuple | None = None) -> str | None:
        """
        Executa INSERT e retorna o ID inserido
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params or ())
                result = cursor.fetchone()
                conn.commit()
                cursor.close()
                return result["id"] if result else None
            except Exception as e:
                conn.rollback()
                logger.error(f"Erro no INSERT: {e}")
                raise

    def execute_update(self, query: str, params: tuple | None = None) -> int:
        """
        Executa UPDATE e retorna número de linhas afetadas
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params or ())
                affected = cursor.rowcount
                conn.commit()
                cursor.close()
                return affected
            except Exception as e:
                conn.rollback()
                logger.error(f"Erro no UPDATE: {e}")
                raise

    def execute_delete(self, query: str, params: tuple | None = None) -> int:
        """
        Executa DELETE e retorna número de linhas deletadas
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params or ())
                affected = cursor.rowcount
                conn.commit()
                cursor.close()
                return affected
            except Exception as e:
                conn.rollback()
                logger.error(f"Erro no DELETE: {e}")
                raise

    def execute_scalar(self, query: str, params: tuple | None = None) -> Any:
        """
        Executa query e retorna um único valor escalar
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            cursor.close()
            # Se result é um dicionário (RealDictCursor), pega o primeiro valor
            if result:
                return next(iter(result.values())) if isinstance(result, dict) else result[0]
            return None

    def execute_count(self, table: str, where: str = "", params: tuple | None = None) -> int:
        """
        Conta registros em uma tabela
        """
        query = f"SELECT COUNT(*) FROM {table}"
        if where:
            query += f" WHERE {where}"
        return self.execute_scalar(query, params) or 0

    def build_pagination(self, page: int, page_size: int) -> tuple[int, int]:
        """
        Calcula LIMIT e OFFSET para paginação
        """
        offset = (page - 1) * page_size
        return page_size, offset

    def build_where_clause(self, filters: dict[str, Any]) -> tuple[str, tuple]:
        """
        Constrói cláusula WHERE dinamicamente

        Args:
            filters: Dicionário com {campo: valor}

        Returns:
            Tupla (where_clause, params)
        """
        if not filters:
            return "", ()

        conditions = []
        params = []

        for field, value in filters.items():
            if value is not None:
                if isinstance(value, list):
                    placeholders = ",".join(["%s"] * len(value))
                    conditions.append(f"{field} IN ({placeholders})")
                    params.extend(value)
                else:
                    conditions.append(f"{field} = %s")
                    params.append(value)

        where_clause = " AND ".join(conditions) if conditions else ""
        return where_clause, tuple(params)
