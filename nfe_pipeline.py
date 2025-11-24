from dataclasses import dataclass
from typing import List, Optional

from database import ResultsRepository, ErpIntegrationRepository
from agents.coordinator_agent import CoordinatorAgent, CoordinatorResult


# ===============================================================
# 🔹 Resultado consolidado enviado ao front-end Streamlit
# ===============================================================
@dataclass
class ResultadoProcessamento:
    # Arquivo
    file_name: str

    # Validação inicial
    is_valid_initial: bool
    errors_initial: List[str]

    # Explicação fiscal do LLM
    explanation: Optional[str]

    # XML corrigido (opcional)
    fixed_xml: Optional[str]

    # Validação pós-correção
    is_valid_fixed: Optional[bool]
    errors_fixed: Optional[List[str]]

    # Integração ERP
    integration_success: Optional[bool]
    integration_status: Optional[int]
    integration_response: Optional[str]
    integration_explanation: Optional[str]


# ===============================================================
# 🔹 Pipeline de Alto Nível
# ===============================================================
class NFEPipeline:
    """
    Orquestra:
    - Validação
    - Explicação
    - Correção
    - Revalidação
    - Integração ERP
    - Registro em base de dados
    """

    def __init__(
        self,
        db: ResultsRepository | None = None,
        erp_repo: ErpIntegrationRepository | None = None,
        salvar_banco: bool = True,
    ):
        self.db = db
        self.erp_repo = erp_repo
        self.salvar_banco = salvar_banco and db is not None

        # Passa o repositório do ERP ao coordinator
        self.coordinator = CoordinatorAgent(erp_repo=self.erp_repo)

    def processar_arquivo(
        self,
        nome_arquivo: str,
        xml_bytes: bytes,
        tentar_corrigir: bool = True,
    ) -> ResultadoProcessamento:

        xml_str = xml_bytes.decode("utf-8")

        # Executar pipeline completo
        coord: CoordinatorResult = self.coordinator.run(
            file_name=nome_arquivo,
            xml_bytes=xml_bytes,
            tentar_corrigir=tentar_corrigir,
        )

        resultado = ResultadoProcessamento(
            file_name=coord.file_name,
            is_valid_initial=coord.is_valid_initial,
            errors_initial=coord.errors_initial,
            explanation=coord.explanation,
            fixed_xml=coord.fixed_xml,
            is_valid_fixed=coord.is_valid_fixed,
            errors_fixed=coord.errors_fixed,
            integration_success=coord.integration_success,
            integration_status=coord.integration_status,
            integration_response=coord.integration_response,
            integration_explanation=coord.integration_explanation,
        )

        # =========================================================
        # 🔹 Registro em base de dados — Resultados
        # =========================================================
        if self.salvar_banco and self.db is not None:

            erros_brutos = ""
            if resultado.errors_initial:
                erros_brutos += "- Erros do XML Original:\n" + "\n".join(resultado.errors_initial)
            if resultado.errors_fixed:
                erros_brutos += "\n\n- Erros do XML Corrigido:\n" + "\n".join(resultado.errors_fixed)

            self.db.registrar_resultado(
                nome_arquivo=resultado.file_name,
                eh_valido=resultado.is_valid_fixed
                if resultado.is_valid_fixed is not None
                else resultado.is_valid_initial,
                mensagem=resultado.explanation or "",
                erros_brutos=erros_brutos or None,
                explicacao_llm=resultado.explanation,
            )

        # =========================================================
        # 🔹 Registro em base de dados — Integração ERP
        # =========================================================
        if self.erp_repo and resultado.integration_success is not None:
            self.erp_repo.registrar_integracao(
                nome_arquivo=resultado.file_name,
                sucesso=resultado.integration_success,
                status_http=resultado.integration_status,
                resposta=resultado.integration_response,
            )

        return resultado
