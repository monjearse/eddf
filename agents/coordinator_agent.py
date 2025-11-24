from dataclasses import dataclass
from typing import List, Optional

from agents.validator_agent import ValidatorAgent
from agents.tax_interpreter_agent import TaxInterpreterAgent
from agents.fixer_agent import FixerAgent
from agents.integrator_agent import IntegratorAgent


@dataclass
class CoordinatorResult:
    file_name: str

    # 1) Validação inicial
    is_valid_initial: bool
    errors_initial: List[str]

    # 2) Explicação fiscal
    explanation: Optional[str]

    # 3) XML corrigido
    fixed_xml: Optional[str]

    # 4) Validação final
    is_valid_fixed: Optional[bool]
    errors_fixed: Optional[List[str]]

    # 5) Integração com ERP
    integration_success: Optional[bool]
    integration_status: Optional[int]
    integration_response: Optional[str]
    integration_explanation: Optional[str]


class CoordinatorAgent:
    """
    Orquestra todo o fluxo:
    - Valida o XML
    - Pede explicação fiscal
    - Corrige o XML (opcional)
    - Revalida o XML corrigido
    - Envia para o ERP (novo!)
    """

    def __init__(self, erp_repo=None):
        self.validator = ValidatorAgent()
        self.tax_agent = TaxInterpreterAgent()
        self.fixer = FixerAgent()
        self.integrator = IntegratorAgent(erp_repo=erp_repo)

    def run(
        self,
        file_name: str,
        xml_bytes: bytes,
        tentar_corrigir: bool = True,
    ) -> CoordinatorResult:

        xml_str = xml_bytes.decode("utf-8")

        # ============================================================
        # 1) VALIDAR XML ORIGINAL
        # ============================================================
        valid, errors = self.validator.validate(xml_str)

        explanation = None
        fixed_xml = None
        valid_fixed = None
        errors_fixed = None

        # Se inválido → aciona agente explicador
        if not valid:
            explanation = self.tax_agent.run(xml_str, errors)

            # Tentativa de correção
            if tentar_corrigir:
                fixed_xml = self.fixer.run(xml_str, errors)

                if fixed_xml and not fixed_xml.startswith("[LLM Error]"):
                    valid_fixed, errors_fixed = self.validator.validate(fixed_xml)

        # ============================================================
        # 2) Se XML válido → Integrar no ERP
        # ============================================================
        integration_success = None
        integration_status = None
        integration_response = None
        integration_explanation = None

        if valid or (valid_fixed is True):
            xml_to_send = fixed_xml if valid_fixed else xml_str

            integ = self.integrator.run(xml_to_send, file_name)

            integration_success = integ.sucesso
            integration_status = integ.status_http
            integration_response = integ.resposta
            integration_explanation = integ.explicacao_llm

        # ============================================================
        # 3) Retornar resultado unificado
        # ============================================================
        return CoordinatorResult(
            file_name=file_name,
            is_valid_initial=valid,
            errors_initial=errors,
            explanation=explanation,
            fixed_xml=fixed_xml,
            is_valid_fixed=valid_fixed,
            errors_fixed=errors_fixed,
            integration_success=integration_success,
            integration_status=integration_status,
            integration_response=integration_response,
            integration_explanation=integration_explanation,
        )
