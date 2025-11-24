import streamlit as st

st.set_page_config(
    page_title="Ficha Técnica — Agentes Autônomos",
    layout="wide",
)

# ============================================================
#  Cabeçalho
# ============================================================
st.title("📘 Ficha Técnica do Projeto")
st.markdown("""
## **Agentes Autônomos para Extração de Dados Fiscais**  
_Revolucionando o processamento fiscal com IA._
""")

st.markdown("---")

# ============================================================
#  Identificação do Projeto
# ============================================================
st.header("📄 Identificação do Projeto")

st.markdown("""
**Título:** *Agentes Autônomos para Extração Inteligente de Dados Fiscais (NFe/NFCe)*  
**Objetivo Geral:** Construir um sistema multi-agente inteligente para validação, diagnóstico,
correção e integração ERP de documentos fiscais eletrónicos.

**Curso:** Agentes Autônomos com Redes Generativas  
**Instituição:** 🏛️ *I²A² – Institut d’Intelligence Artificielle Appliquée* (i2a2.academy)  
**Turma:** Código B  
""")

st.markdown("---")

# ============================================================
#  Autor
# ============================================================
st.header("👤 Autor")
st.markdown("""
**Arsénio António Monjane**  
Especialista em Engenharia de Software, Sistemas de Informação e Automação Inteligente.  
Responsável pelo design dos agentes, desenvolvimento do pipeline, integração ERP e dashboards.
""")

st.markdown("---")

# ============================================================
#  Arquitetura
# ============================================================
st.header("🧠 Arquitetura Técnica")

st.markdown("""
O sistema é composto por **4 agentes autónomos**, orquestrados por um *Coordinator Agent*:

1. **Validator Agent**  
   - Valida XML NFe 4.00 com XSD oficial  
   - Extrai contexto básico (ide/emit/dest)

2. **Tax Interpreter Agent**  
   - Explica impostos e regras fiscais  
   - Gera relatórios em linguagem de negócio

3. **Fixer Agent**  
   - Sugere correções estruturais no XML

4. **Integrator Agent**  
   - Envia o XML validado ao ERP  
   - Regista logs de integração em SQLite

**Tecnologias-chave:**

- Python 3.12 + Streamlit  
- Gemini API (LLM)  
- Validação XSD com `lxml`  
- SQLite (persistência local)  
- ASP.NET Core API (ERP)  
- Dapper + SQL Server  
""")

st.markdown("---")

# ============================================================
#  Fluxo Geral
# ============================================================
st.header("🔄 Fluxo de Funcionamento")

st.markdown("""
1. Upload de XML (NFe/NFCe)  
2. Validação contra schema SEFAZ 4.00  
3. Diagnóstico + explicação fiscal por IA  
4. Sugestão de correções automáticas  
5. Envio para o ERP (API .NET Core)  
6. Registo de logs + dashboards  

Todos os passos são assistidos por agentes autónomos.
""")



st.markdown("---")

st.success("📘 Ficha técnica carregada com sucesso.")
