from typing import List, Dict, Any

from llm_client import LLMClient


class TaxInterpreterAgent:
    """
    Agente responsável por transformar erros técnicos de validação
    em explicações em linguagem de negócio / fiscal.
    """

    def __init__(self):
        self._llm = LLMClient()

    def run(
        self,
        file_name: str,
        context: Dict[str, Any],
        errors: List[str],
    ) -> str:
        if not errors:
            return "Nenhum erro técnico foi reportado."

        return self._llm.explain_validation(
            nome_arquivo=file_name,
            contexto_xml=context,
            issues=errors,
        )
