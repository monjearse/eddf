import streamlit as st

st.set_page_config(
    page_title="Ajuda & Manual — EDDF",
    layout="wide",
)

# ============================================================
#  Título da Página
# ============================================================
st.title("❓ Ajuda & Manual do Utilizador")
st.write("Bem-vindo à área de suporte do **EDDF — Estação de Dados de Documentos Fiscais**.")

st.markdown("---")

# ============================================================
#  Secção 1 — Como utilizar o sistema
# ============================================================
st.header("📌 1. Como utilizar o sistema")

st.markdown("""
O EDDF permite **validar, corrigir, interpretar** e **integrar documentos fiscais** (NFe/NFCe)
com auxílio de agentes autónomos de IA.

---

### **🔎 Passo a passo**

1. **Aceda à página “1_Processamento”**
   - Carregue um ou mais ficheiros XML.

2. **Clique em “🚀 Iniciar Processamento”**
   - O sistema valida o XML contra o schema oficial **NFe 4.00**.
   - Um agente LLM explica erros fiscais e inconsistências.
   - Um agente de correção tenta gerar um XML corrigido.

3. **Se o XML estiver válido**
   - O botão **“Enviar para ERP”** será ativado.

4. **Integração com ERP**
   - O Integrator Agent envia o XML para a API **ERP.Api (.NET Core)**.
   - A resposta é registada no histórico local.

5. **Análise de Resultados**
   - A página **3_Dashboard** exibe gráficos, tendências e insights do LLM.

6. **Ficha Técnica**
   - A página **5_FichaTecnica** resume o enquadramento académico do projeto.

""")

st.markdown("---")

# ============================================================
#  Secção 2 — Perguntas Frequentes (FAQ)
# ============================================================
st.header("💬 2. FAQ — Perguntas Frequentes")

faq = {
    "O que acontece quando envio um XML?":
        "O ficheiro é validado contra o schema NFe 4.00. Caso passe, é enviado ao ERP e registado no histórico.",

    "O sistema altera o XML original?":
        "Não. O XML corrigido é apenas uma sugestão gerada pelo LLM.",

    "Posso enviar uma NFe inválida ao ERP?":
        "Não. O botão só aparece quando o XML está 100% válido.",

    "Onde ficam armazenados os logs?":
        "Na base SQLite `nfe_validacao.db`, nas tabelas `resultados` e `integracoes_erp`.",

    "Como atualizo o endpoint do ERP?":
        "Altere `ERP_API_BASE` e `ERP_API_IMPORT_NFE` no ficheiro `.env`.",

    "O sistema funciona offline?":
        "Sim, exceto para integração com ERP e chamadas LLM (Gemini).",
}

for pergunta, resposta in faq.items():
    with st.expander(pergunta):
        st.write(resposta)

st.markdown("---")

# ============================================================
#  Secção 3 — Resolução de Problemas Comuns
# ============================================================
st.header("🛠️ 3. Resolução de Problemas Comuns")

st.markdown("""
### ❌ **Erro: ERP endpoint não encontrado**
> *“Failed to establish a new connection”*

**Solução:**
- Verifique se a API ERP está ativa.
- Confira as variáveis no `.env`:
  - `ERP_API_BASE`
  - `ERP_API_IMPORT_NFE`
- Reinicie o Streamlit após alterações.

---

### ❌ **Erro: XML inválido conforme schema NFe 4.00**
**Solução:**
- Consulte os erros detalhados no painel.
- Use as correções sugeridas pelo Fixer Agent.
- Confirme o namespace obrigatório:  
  `http://www.portalfiscal.inf.br/nfe`

---

### ❌ **Erro de assinatura digital**
**Solução:**
- Em homologação, use certificados simplificados ou mockados.
- A estrutura XML da assinatura deve existir mesmo sem valor jurídico.

---

### ❌ **O botão “Enviar para ERP” não aparece**
**Solução:**
- Ele só é mostrado se `is_valid_initial == True`.

""")

st.markdown("---")

# ============================================================
#  Secção 4 — Fluxo dos Agentes Autônomos (Visão Académica)
# ============================================================
st.header("🤖 4. Fluxo dos Agentes Autônomos (Resumo Académico)")

st.markdown("""
A arquitetura multi-agente do EDDF segue a abordagem moderna de **Agentes Autônomos Inteligentes**,
cada um especializado numa etapa do processamento fiscal:

---

### **🟦 Validator Agent**
- Valida o XML contra o schema NFe 4.00  
- Extrai contexto básico da nota (emitente, destinatário, total, datas)

---

### **🟪 Tax Interpreter Agent**
- Usa Gemini para explicar erros e regras fiscais  
- Produz uma leitura humanizada em linguagem de negócio

---

### **🟨 Fixer Agent**
- Gera automaticamente um XML corrigido  
- Remove campos inválidos, corrige estrutura e formatação  
- Solicita revalidação do XML corrigido

---

### **🟧 Integrator Agent**
- Envia o XML validado ao ERP (.NET Core)  
- Grava o status da integração no SQLite  
- Devolve o ID do documento integrado

---

### **🔴 Coordinator Agent**
- Orquestra todos os agentes  
- Mantém consistência e fluxo  
- Produz o objeto final consolidado para apresentação

""")

st.markdown("---")

# ============================================================
#  Secção 5 — Enquadramento Académico (Ficha Técnica)
# ============================================================
st.header("📘 5. Ficha Técnica do Projeto")

st.markdown("""
**Projeto:** EDDF — Estação de Dados de Documentos Fiscais  
**Âmbito:** Agentes Autônomos com Redes Generativas  
**Instituição:** I2A2 — Institut d'Intelligence Artificielle Appliquée  
**Curso:** Agentes Autônomos com Redes Generativas  
**Grupo:** Código B  
**Tema:** Extração e Integração Inteligente de Dados Fiscais (NFe/NFCe)  
**Autor:** Bezix (Desenvolvimento & Arquitetura)  
**Tecnologias:** Python, Streamlit, Gemini 2.0, .NET Core, Dapper, SQLite  
""")
