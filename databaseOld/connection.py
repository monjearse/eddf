import os
import sqlite3
from contextlib import contextmanager
from typing import Optional


class DBConnection:
    """
    Gerencia a conexão com o SQLite usando context manager.
    """

    def __init__(self, db_path: Optional[str] = None):
        # Usa variável de ambiente DB_PATH ou default local
        self.db_path = db_path or os.getenv("DB_PATH", "./nfe_validacao.db")

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
