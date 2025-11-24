# database.py
import os
import sqlite3
from contextlib import contextmanager
from typing import Optional, Iterable, Tuple


# =========================================================
# 🔹 Classe base para repositórios SQLite
# =========================================================
class BaseRepository:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.getenv("DB_PATH", "./nfe_validacao.db")

    @contextmanager
    def _conn(self):
        """Abre e encerra uma conexão SQLite de forma segura."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # melhor para acesso por nome
        try:
            yield conn
        finally:
            conn.close()


# =========================================================
# 🔹 Tabela: resultados (validações XML)
# =========================================================
class ResultsRepository(BaseRepository):

    def ensure_schema(self):
        with self._conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS resultados (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_arquivo   TEXT NOT NULL,
                    eh_valido      INTEGER NOT NULL,
                    mensagem       TEXT,
                    erros_brutos   TEXT,
                    explicacao_llm TEXT,
                    criado_em      DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def registrar_resultado(
        self,
        nome_arquivo: str,
        eh_valido: bool,
        mensagem: str,
        erros_brutos: Optional[str] = None,
        explicacao_llm: Optional[str] = None,
    ):
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO resultados
                    (nome_arquivo, eh_valido, mensagem, erros_brutos, explicacao_llm)
                VALUES (?, ?, ?, ?, ?)
            """, (
                nome_arquivo,
                1 if eh_valido else 0,
                mensagem,
                erros_brutos,
                explicacao_llm,
            ))
            conn.commit()

    def listar_ultimos(self, limite: int = 50):
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nome_arquivo, eh_valido, mensagem, erros_brutos,
                       explicacao_llm, criado_em
                FROM resultados
                ORDER BY id DESC
                LIMIT ?
            """, (limite,))
            return cur.fetchall()


# =========================================================
# 🔹 Tabela: integracoes_erp (logs de envio para ERP)
# =========================================================
class ErpIntegrationRepository(BaseRepository):

    def ensure_schema(self):
        with self._conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS integracoes_erp (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_arquivo  TEXT NOT NULL,
                    sucesso       INTEGER NOT NULL,
                    status_http   INTEGER,
                    resposta      TEXT,
                    criado_em     DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def registrar_integracao(
        self,
        nome_arquivo: str,
        sucesso: bool,
        status_http: Optional[int],
        resposta: Optional[str],
    ):
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO integracoes_erp
                    (nome_arquivo, sucesso, status_http, resposta)
                VALUES (?, ?, ?, ?)
            """, (
                nome_arquivo,
                1 if sucesso else 0,
                status_http,
                resposta,
            ))
            conn.commit()

    def listar_ultimas(self, limite: int = 50):
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nome_arquivo, sucesso, status_http, resposta, criado_em
                FROM integracoes_erp
                ORDER BY id DESC
                LIMIT ?
            """, (limite,))
            return cur.fetchall()


# =========================================================
# 🔹 DatabaseManager – centraliza e expõe repositórios
# =========================================================
class DatabaseManager:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.getenv("DB_PATH", "./nfe_validacao.db")

        # Repositório de resultados
        self._results_repo = ResultsRepository(self.db_path)
        self._results_repo.ensure_schema()

        # Repositório de integrações com ERP
        self._erp_repo = ErpIntegrationRepository(self.db_path)
        self._erp_repo.ensure_schema()

    # 🔸 getter oficial usado pelo pipeline
    def get_results_repository(self) -> ResultsRepository:
        return self._results_repo

    # 🔸 getter oficial usado para logging de ERP
    def get_erp_repository(self) -> ErpIntegrationRepository:
        return self._erp_repo
