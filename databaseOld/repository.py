from typing import Optional, Iterable, Tuple

from .connection import DBConnection


class ResultsRepository:
    """
    Repositório para acesso aos resultados de validação.

    Expõe os mesmos métodos que o antigo `Database`:
    - registrar_resultado(...)
    - listar_ultimos(...)
    Assim, o NFEPipeline continua compatível.
    """

    def __init__(self, conn: DBConnection):
        self.conn = conn

    def registrar_resultado(
        self,
        nome_arquivo: str,
        eh_valido: bool,
        mensagem: str,
        erros_brutos: Optional[str] = None,
        explicacao_llm: Optional[str] = None,
    ):
        """
        Insere um registo na tabela 'resultados'.
        """
        with self.conn.connect() as db:
            cur = db.cursor()
            cur.execute(
                """
                INSERT INTO resultados
                    (nome_arquivo, eh_valido, mensagem, erros_brutos, explicacao_llm)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    nome_arquivo,
                    1 if eh_valido else 0,
                    mensagem,
                    erros_brutos,
                    explicacao_llm,
                ),
            )
            db.commit()

    def listar_ultimos(
        self, limite: int = 50
    ) -> Iterable[Tuple[int, str, int, str, Optional[str], Optional[str], str]]:
        """
        Lista os últimos registos inseridos, em ordem decrescente de id.
        """
        with self.conn.connect() as db:
            cur = db.cursor()
            cur.execute(
                """
                SELECT id, nome_arquivo, eh_valido, mensagem, erros_brutos,
                       explicacao_llm, criado_em
                FROM resultados
                ORDER BY id DESC
                LIMIT ?
                """,
                (limite,),
            )
            return cur.fetchall()
