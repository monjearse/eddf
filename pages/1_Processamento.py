import streamlit as st
from dotenv import load_dotenv
import pandas as pd

from database import DatabaseManager
from nfe_pipeline import NFEPipeline

load_dotenv()


def main():

    st.title("📂 Processamento de Arquivos XML (NFe/NFCe)")
    st.write(
        "Carregue um ou mais ficheiros XML de NFe/NFCe para validação automática "
        "contra o leiaute oficial **SEFAZ 4.00** e análise assistida por IA (Gemini)."
    )

    # Instâncias de BD e Pipeline
    db_manager = DatabaseManager()
    results_repo = db_manager.get_results_repository()
    erp_repo = db_manager.get_erp_repository()

    pipeline = NFEPipeline(db=results_repo, erp_repo=erp_repo, salvar_banco=True)

    uploaded_files = st.file_uploader(
        "Selecione os ficheiros XML",
        type=["xml"],
        accept_multiple_files=True,
        key="upload_processamento",
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        processar = st.button("🚀 Iniciar Processamento", type="primary")

    with col2:
        mostrar_historico = st.checkbox("Mostrar histórico recente abaixo", value=False)

    # ============================================================
    # PROCESSAMENTO
    # ============================================================
    if processar:
        if not uploaded_files:
            st.warning("Nenhum ficheiro selecionado.")
        else:
            with st.status("A processar ficheiros...", expanded=True) as status:
                for f in uploaded_files:
                    st.markdown(f"## 📄 Resultado para: `{f.name}`")
                    xml_bytes = f.read()

                    resultado = pipeline.processar_arquivo(
                        f.name, xml_bytes, tentar_corrigir=True
                    )

                    # ------------------- Validação inicial -------------------
                    if resultado.is_valid_initial:
                        st.success("✅ XML original válido conforme o schema NFe 4.00.")
                    else:
                        st.error("❌ XML original inválido conforme o schema NFe 4.00.")

                    if resultado.errors_initial:
                        with st.expander("Erros do XML original"):
                            for e in resultado.errors_initial:
                                st.code(e, language="text")

                    # ------------------- Explicação fiscal -------------------
                    if resultado.explanation:
                        with st.expander("📘 Explicação Fiscal (Gemini)"):
                            st.write(resultado.explanation)

                    # ------------------- XML Corrigido ------------------------
                    if resultado.fixed_xml:
                        with st.expander("🛠 XML Corrigido Sugerido"):
                            st.code(resultado.fixed_xml, language="xml")

                    if resultado.errors_fixed:
                        with st.expander("⚠ Erros na Validação do XML Corrigido"):
                            for e in resultado.errors_fixed:
                                st.code(e, language="text")

                    if resultado.is_valid_fixed:
                        st.success("✅ O XML corrigido passou na validação do schema.")

                    st.markdown("---")

                status.update(label="Processamento concluído", state="complete")

    # ============================================================
    # HISTÓRICO DE VALIDAÇÕES
    # ============================================================
    if mostrar_historico:
        st.subheader("📜 Histórico recente de validações")

        registos = list(results_repo.listar_ultimos(50))
        if not registos:
            st.info("Ainda não há registos gravados.")
        else:
            dfv = pd.DataFrame(registos, columns=[
                "ID",
                "Arquivo",
                "Valido",
                "Mensagem",
                "Erros",
                "Explicacao",
                "Data"
            ])

            dfv["Valido"] = dfv["Valido"].replace({1: "🟢 Sim", 0: "🔴 Não"})

            st.dataframe(dfv, use_container_width=True)

            st.markdown("---")

    # ============================================================
    # FILTROS DO HISTÓRICO DE INTEGRAÇÃO
    # ============================================================
    st.subheader("🔗 Histórico de Integrações com o ERP")

    integracoes = list(erp_repo.listar_ultimas(200))

    if not integracoes:
        st.info("Ainda não há integrações registadas.")
        return

    df = pd.DataFrame(integracoes, columns=[
        "ID",
        "Arquivo",
        "Sucesso",
        "HTTP",
        "Resposta",
        "Data"
    ])

    df["SucessoTxt"] = df["Sucesso"].apply(lambda x: "🟢 Sucesso" if x == 1 else "🔴 Falha")

    # ------------------- FILTROS -------------------
    st.markdown("### 🔍 Filtros")

    colA, colB, colC, colD = st.columns(4)

    with colA:
        filtro_status = st.selectbox(
            "Status",
            ["Todos", "Sucesso", "Falha"]
        )

    with colB:
        filtro_arquivo = st.text_input("Nome do arquivo contém:")

    with colC:
        filtro_data_inicio = st.date_input("Data inicial", value=None)

    with colD:
        filtro_data_fim = st.date_input("Data final", value=None)

    # ------------------- APLICAR FILTROS -------------------
    df_filtrado = df.copy()

    # Status
    if filtro_status == "Sucesso":
        df_filtrado = df_filtrado[df_filtrado["Sucesso"] == 1]
    elif filtro_status == "Falha":
        df_filtrado = df_filtrado[df_filtrado["Sucesso"] == 0]

    # Arquivo
    if filtro_arquivo:
        df_filtrado = df_filtrado[df_filtrado["Arquivo"].str.contains(filtro_arquivo, case=False)]

    # Datas
    if filtro_data_inicio:
        df_filtrado = df_filtrado[df_filtrado["Data"] >= str(filtro_data_inicio)]

    if filtro_data_fim:
        df_filtrado = df_filtrado[df_filtrado["Data"] <= str(filtro_data_fim)]

    # ------------------- MOSTRAR TABELA FILTRADA -------------------
    st.dataframe(
        df_filtrado[["ID", "Arquivo", "SucessoTxt", "HTTP", "Data"]],
        use_container_width=True,
        hide_index=True
    )

    # ------------------- DETALHES DA INTEGRAÇÃO -------------------
    st.markdown("### 📄 Detalhes da integração selecionada")

    if not df_filtrado.empty:
        selected_id = st.selectbox(
            "Selecione um registo:",
            df_filtrado["ID"].tolist()
        )

        row = df[df["ID"] == selected_id].iloc[0]

        st.write(f"**📁 Arquivo:** {row['Arquivo']}")
        st.write(f"**📅 Data:** {row['Data']}")
        st.write(f"**🔗 Status:** { '🟢 Sucesso' if row['Sucesso'] == 1 else '🔴 Falha' }")
        st.write(f"**🌐 HTTP:** {row['HTTP']}")

        st.markdown("#### 📨 Resposta completa do ERP:")
        st.code(row["Resposta"], language="json")


if __name__ == "__main__":
    main()
