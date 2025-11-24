import os
import requests
from dataclasses import dataclass
from typing import Optional

from llm_client import LLMClient


# ============================================================
# 🔹 ROLE: comportamento do IntegratorAgent
# ============================================================
integrator_agent_role = """
Você é o IntegratorAgent do sistema EDDF.

FUNÇÃO PRINCIPAL:
- Receber o XML já validado pelo pipeline.
- Enviar esse XML para o serviço ERP.Api através do endpoint configurado.
- Interpretar a resposta recebida (sucesso, warning ou erro).
- Gerar explicações claras ao usuário final sobre o resultado da integração.

VOCÊ DEVE:
- Explicar causas prováveis de falha (HTTP, formato, ERP offline, etc.).
- Sugerir verificações práticas: porta, endpoint, rede, firewall, estrutura XML, etc.
- Dizer se o erro é provável no ERP ou no EDDF, de forma objetiva.
- Atuar como assistente técnico, não como validador fiscal.

VOCÊ NÃO DEVE:
- Modificar o XML.
- Corrigir o XML (isso é feito pelo FixerAgent).
- Gerar ou inventar dados fiscais.
- Revalidar XML (isso é feito pelo ValidatorAgent).
- Produzir XML novo (isso é proibido).

Seu objetivo é apenas interpretar tecnicamente o que aconteceu ao ENVIAR ao ERP.
"""


# ============================================================
# 🔹 Resultado estruturado retornado ao pipeline
# ============================================================
@dataclass
class IntegrationResult:
    sucesso: bool
    status_http: Optional[int]
    resposta: str
    explicacao_llm: Optional[str]


# ============================================================
# 🔹 IntegratorAgent — envia XML ao ERP e interpreta a resposta
# ============================================================
class IntegratorAgent:
    def __init__(self, erp_repo=None):
        #self.endpoint = os.getenv("ERP_ENDPOINT")

        base = os.getenv("ERP_API_BASE")
        path = os.getenv("ERP_API_IMPORT_NFE")

        if base and path:
            self.endpoint = base.rstrip("/") + path
        else:
            self.endpoint = os.getenv("ERP_ENDPOINT")

        if not self.endpoint:
            raise ValueError("❌ ERP_ENDPOINT não definido no .env")
        
        if not self.endpoint:
            raise ValueError("❌ ERP_ENDPOINT não definido no .env")

        self.repo = erp_repo
        self.llm = LLMClient()

    # ------------------------------------------------------------
    # Explicação do erro via LLM
    # ------------------------------------------------------------
    def _explicar_falha(self, resposta: str, status_http: Optional[int]):
        return self.llm.structured([
            ("system", integrator_agent_role),
            ("user", f"""
A integração do XML com o ERP falhou.

Status HTTP: {status_http}
Resposta recebida:
{resposta}

Explique o que isso significa, possíveis causas e ações recomendadas.
""")
        ])

    # ------------------------------------------------------------
    # Execução principal do agente
    # ------------------------------------------------------------
    def run(self, xml_string: str, file_name: str) -> IntegrationResult:
        try:
            response = requests.post(
                self.endpoint,
                data=xml_string.encode("utf-8"),
                headers={"Content-Type": "application/xml"},
                timeout=20
            )

            status = response.status_code
            body = response.text
            sucesso = 200 <= status < 300

            explicacao = None
            if not sucesso:
                explicacao = self._explicar_falha(body, status)

            # Registrar na BD caso exista repositório
            if self.repo:
                self.repo.registrar_integracao(
                    nome_arquivo=file_name,
                    sucesso=sucesso,
                    status_http=status,
                    resposta=body,
                )

            return IntegrationResult(
                sucesso=sucesso,
                status_http=status,
                resposta=body,
                explicacao_llm=explicacao,
            )

        except Exception as e:
            msg = str(e)

            explicacao = self._explicar_falha(msg, None)

            if self.repo:
                self.repo.registrar_integracao(
                    nome_arquivo=file_name,
                    sucesso=False,
                    status_http=None,
                    resposta=msg,
                )

            return IntegrationResult(
                sucesso=False,
                status_http=None,
                resposta=msg,
                explicacao_llm=explicacao,
            )
