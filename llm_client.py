import os
from typing import Optional, List, Tuple, Dict, Any

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


class LLMClient:
    """
    Cliente simples para o Gemini, usando apenas google-generativeai.
    """

    def __init__(self, model: Optional[str] = None):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY não encontrada. Defina no ficheiro .env."
            )

        genai.configure(api_key=api_key)

        self.model_name = model or os.getenv("LLM_MODEL", "gemini-1.5-flash")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", 0.2))

        self.model = genai.GenerativeModel(self.model_name)

    def _generate(self, prompt: str) -> str:
        try:
            cfg = genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=1024,
            )
            resp = self.model.generate_content(prompt, generation_config=cfg)
            return resp.text or "[Sem resposta do modelo]"
        except Exception as e:
            return f"[LLM Error] {e}"

    def simple(self, prompt: str) -> str:
        return self._generate(prompt)

    def explain_validationOld(
        self,
        nome_arquivo: str,
        contexto_xml: Dict[str, Any],
        erros: List[str],
    ) -> str:
        """
        Gera uma explicação amigável dos erros de validação da NFe.
        """
        resumo_erros = "\n".join(f"- {e}" for e in erros)
        prompt = f"""
Você é um especialista em documentos fiscais eletrônicos brasileiros (NFe 4.00).

O seguinte arquivo XML foi analisado: {nome_arquivo}

Erros de validação contra o schema NFe (leiaute 4.00):

{resumo_erros}

Algumas informações de contexto extraídas do XML (podem estar incompletas):
{contexto_xml}

Explique de forma CLARA, didática e objetiva:
1. O que esses erros significam em linguagem de negócio.
2. Quais campos ou blocos provavelmente estão ausentes, na ordem em que aparecem.
3. Sugestões práticas para correção do XML para que fique em conformidade com a NFe 4.00.

Responda em português de Portugal, em formato de texto corrido, podendo usar listas quando útil.
        """.strip()

        return self._generate(prompt)



    def explain_validation(self, nome_arquivo: str, contexto_xml: dict, issues: list) -> str:
        """
        Explica os erros de validação em linguagem fiscal/negócio.
        """
        resumo_erros = "\n".join(f"- {e}" for e in issues)

        prompt = f"""
Você é um especialista fiscal em documentos eletrônicos brasileiros (NFe 4.00).

Arquivo analisado: {nome_arquivo}

Erros de validação detectados:
{resumo_erros}

Contexto extraído do XML:
{contexto_xml}

Explique de forma clara:
1. O que cada erro significa.
2. Como corrigir no XML.
3. Quais campos pertencem ao emitente, destinatário, ide ou produto.
4. Se há erros de ordem estrutural ou campos obrigatórios faltando.

Responda de forma profissional e objetiva.
"""
        try:
            return self.simple(prompt)
        except Exception as e:
            return f"[LLM Error] {e}"
