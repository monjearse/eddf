from typing import Optional

from .connection import DBConnection
from .migrations import DBMigrations
from .repository import ResultsRepository


class DatabaseManager:
    """
    Ponto central de acesso à base de dados.

    - Cria a conexão
    - Executa migrações (ensure_schema)
    - Fornece o ResultsRepository
    """

    def __init__(self, db_path: Optional[str] = None):
        self.conn = DBConnection(db_path)
        self.migrations = DBMigrations(self.conn)
        self.migrations.ensure_schema()

        self._results_repo = ResultsRepository(self.conn)

    def get_results_repository(self) -> ResultsRepository:
        return self._results_repo
