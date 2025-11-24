# EDDF — Estação de Dados de Documentos Fiscais  
### 🔍 Validação, correção e integração de NFe/NFCe com agentes autônomos de IA

Este projeto implementa uma pipeline completa para **validação, análise e integração de XMLs fiscais (NFe/NFCe)** utilizando **agentes autônomos de IA**, integração com um **ERP ASP.NET Core**, dashboard em **Streamlit**, persistência em **SQLite** e análise por **LLMs (Gemini)**.

---

## 👨‍🎓 **Autor**
**Arsénio António Monjane**  
📧 Email: monjearse@hotmail.com  
🔗 LinkedIn: https://www.linkedin.com/in/arsenioamonjane/  
🧑‍💻 Grupo: **Código B**

## 🚀 Funcionalidades Principais

### ✔️ 1. Validação Técnica (Agente Validator)
- Valida XML NFe 4.00 usando XSD oficial SEFAZ.  
- Extrai contexto fiscal: `ide`, `emit`, `dest`, `total`.

### ✔️ 2. Interpretação Fiscal (Agente Tax Interpreter)
- Usa LLM Gemini para explicar erros e regras fiscais.  
- Traduz o erro técnico do XSD para uma explicação compreensível.

### ✔️ 3. Correção do XML (Agente Fixer)
- Sugere correções possíveis para o XML inválido.  
- Propõe ajustes mínimos mantendo integridade fiscal.

### ✔️ 4. Integração com ERP (.NET Core) (Agente Integrator)
- Envia XML validado para endpoint REST:  POST /api/Xml/importar
- Registra logs locais da resposta do ERP.
- Garante segurança e idempotência (chaves duplicadas não são reenviadas).

### ✔️ 5. Dashboard Analítico
- Gráficos por dia.  
- Tendências de erros.  
- Distribuição de sucesso/falha.  
- Análise linguística dos logs do LLM.

### ✔️ 6. Histórico Completo
- Histórico de validações (SQLite).  
- Histórico de integrações com ERP.  
- Comparação entre XML original e XML corrigido.

---

## 🧠 Arquitetura de Agentes
            ┌────────────────────────────┐
            │     Validator Agent        │
            │  Valida e extrai contexto  │
            └──────────────┬─────────────┘
                           ↓
            ┌────────────────────────────┐
            │   Tax Interpreter Agent    │
            │  Explica erros com LLM     │
            └──────────────┬─────────────┘
                           ↓
            ┌────────────────────────────┐
            │        Fixer Agent         │
            │  Sugere XML corrigido      │
            └──────────────┬─────────────┘
                           ↓
            ┌────────────────────────────┐
            │     Integrator Agent       │
            │  Envia ao ERP + registra   │
            └──────────────┬─────────────┘
                           ↓
            ┌────────────────────────────┐
            │     Coordinator Agent      │
            │ Orquestra todo o processo  │
            └────────────────────────────┘

## 📁 Estrutura do Projeto
/eddf
│── agents/
│ ├── validator_agent.py
│ ├── fixer_agent.py
│ ├── tax_interpreter_agent.py
│ ├── integrator_agent.py
│ └── coordinator_agent.py
│
│── pages/
│ ├── 1_Processamento.py
│ ├── 2_Historico.py
│ ├── 3_Dashboard.py
│ ├── 4_FichaTecnica.py
│ └── 5_Ajuda.py
│
│── database.py
│── nfe_pipeline.py
│── validation/
│── schemas/
│── .env
│── README.md

---

## ⚙️ Variáveis de Ambiente (.env)

```ini
# Gemini API Key
GEMINI_API_KEY=...

# ERP endpoint
ERP_API_BASE=http://localhost:5256
ERP_API_IMPORT_NFE=/api/Xml/importar

# Path para schemas NFe
XSD_PATH=./schemas/nfe_v4.00.xsd

▶️ Como executar
1) Instalar dependências

pip install -r requirements.txt

2) Rodar Streamlit
streamlit run app.py

3) Rodar ERP (separado)
dotnet run --project ERP.Api

📌 Requisitos

Python 3.10+

Streamlit 1.36+

SQLite 3+

.NET 7+ (para ERP)

Gemini API Key


## 🧭 Licença

Projeto desenvolvido por **Arsénio António Monjane (I2A2 - Institut d'Intelligence Artificielle Appliquée)**  
Distribuído sob licença **MIT**.