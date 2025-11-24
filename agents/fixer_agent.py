from typing import List, Dict, Any

from llm_client import LLMClient


class FixerAgent:
    """
    Agente responsável por sugerir uma versão corrigida do XML,
    garantindo que o prompt nunca quebra devido ao uso de markdown.
    """

    def __init__(self):
        self._llm = LLMClient()

    def run(self, file_name: str, original_xml: str, context, errors):
        # Construção segura do prompt usando format()
        resumo_erros = "\n".join(f"- {e}" for e in errors)

        prompt = (
            "Você é um especialista em NFe 4.00 e XML.\n\n"
            "Recebeu o ficheiro: {file}\n\n"
            "Erros de validação:\n"
            "{erros}\n\n"
            "Contexto extraído:\n"
            "{contexto}\n\n"
            "A seguir está o XML ORIGINAL:\n\n"
            "<XML_INICIO>\n"
            "{xml}\n"
            "<XML_FIM>\n\n"
            "Tarefa:\n"
            "1. Corrigir o XML para ficar conforme o schema NFe 4.00.\n"
            "2. Preencher campos obrigatórios ausentes.\n"
            "3. Corrigir a ordem das tags.\n"
            "4. Retornar apenas o XML corrigido entre as marcações abaixo:\n\n"
            "<XML_CORRIGIDO_INICIO>\n"
            "... coloque XML corrigido aqui ...\n"
            "<XML_CORRIGIDO_FIM>"
        ).format(
            file=file_name,
            erros=resumo_erros,
            contexto=context,
            xml=original_xml
        )

        resposta = self._llm.simple(prompt)

        # Extrair XML entre marcadores personalizados
        ini = resposta.find("<XML_CORRIGIDO_INICIO>")
        fim = resposta.find("<XML_CORRIGIDO_FIM>")

        if ini != -1 and fim != -1:
            return resposta[ini + len("<XML_CORRIGIDO_INICIO>"):fim].strip()

        # Caso o LLM não siga o formato
        return resposta.strip()
