from dataclasses import dataclass
from typing import List, Dict, Any

from validation import NFeValidator


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    context: Dict[str, Any]


class ValidatorAgent:
    """
    Agente responsável por validar o XML contra o schema oficial NFe 4.00
    e extrair um contexto mínimo (ide/emit/dest).

    Compatível com:
    - CoordinatorAgent.validate()
    - NFEPipeline
    - Architecture multi-agent EDDF
    """

    def __init__(self, xsd_path: str = "./schemas/nfe_v4.00.xsd"):
        self._validator = NFeValidator(xsd_path=xsd_path)

    # ============================================================
    # 🔹 Método original (usado internamente no fluxo completo)
    # ============================================================
    def run(self, xml_bytes: bytes) -> ValidationResult:
        is_valid, errors = self._validator.validar(xml_bytes)
        context = self._validator.extrair_contexto_basico(xml_bytes)
        return ValidationResult(is_valid=is_valid, errors=errors, context=context)

    # ============================================================
    # 🔹 Método esperado pelo CoordinatorAgent
    # ============================================================
    def validate(self, xml_string: str):
        """
        Compatibilidade retroativa:
        - CoordinatorAgent espera (bool, List[str]).
        - Aqui apenas convertemos string → bytes e
          chamamos o validador já existente.
        """
        xml_bytes = xml_string.encode("utf-8")

        is_valid, errors = self._validator.validar(xml_bytes)
        return is_valid, errors
