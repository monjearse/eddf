from .connection import DBConnection


class DBMigrations:
    """
    Responsável por garantir que o schema da base de dados exista.
    """

    def __init__(self, conn: DBConnection):
        self.conn = conn

    def ensure_schema(self):
        """
        Cria a tabela 'resultados' se ainda não existir.

        Mantém o mesmo layout do db.py original:
        - id, nome_arquivo, eh_valido, mensagem, erros_brutos,
          explicacao_llm, criado_em
        """
        with self.conn.connect() as db:
            cur = db.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS resultados (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_arquivo  TEXT NOT NULL,
                    eh_valido     INTEGER NOT NULL,
                    mensagem      TEXT,
                    erros_brutos  TEXT,
                    explicacao_llm TEXT,
                    criado_em     DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            db.commit()
