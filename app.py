import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="EDDF - Extração de Dados de Documentos Fiscais",
    layout="wide",
)


def main():
    st.title("🧾 EDDF - Extração de Dados de Documentos Fiscais")
    st.markdown(
        """
Bem-vindo ao **EDDF** – Ambiente académico de demonstração para:

- 📂 Upload e validação de ficheiros **XML de NFe/NFCe** contra o leiaute oficial **SEFAZ 4.00**  
- 🤖 Análise assistida por IA (Gemini), com explicações em linguagem de negócio  
- 🧠 Agentes autónomos para validação, correção e interpretação fiscal  
- 💾 Armazenamento de histórico em **SQLite**  
- 📊 Dashboards para análise agregada dos resultados

Use o menu de páginas do Streamlit (barra lateral ou topo) para navegar entre:

1. **Processamento** – upload e processamento de novos XML  
2. **Histórico** – consulta de validações gravadas  
3. **Dashboard** – visão agregada dos resultados
"""
    )

    st.info(
        "Sugestão: comece pela página **'Processamento'** para carregar alguns XMLs, "
        "e depois explore as páginas **'Histórico'** e **'Dashboard'**."
    )


if __name__ == "__main__":
    main()
