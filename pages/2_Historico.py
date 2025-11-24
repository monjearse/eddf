import pandas as pd
import streamlit as st

from database import DatabaseManager


def carregar_dados(repo) -> pd.DataFrame:
    registos = list(repo.listar_ultimos(limite=500))
    if not registos:
        return pd.DataFrame(
            columns=[
                "id",
                "nome_arquivo",
                "eh_valido",
                "mensagem",
                "erros_brutos",
                "explicacao_llm",
                "criado_em",
            ]
        )

    df = pd.DataFrame(
        registos,
        columns=[
            "id",
            "nome_arquivo",
            "eh_valido",
            "mensagem",
            "erros_brutos",
            "explicacao_llm",
            "criado_em",
        ],
    )
    df["criado_em"] = pd.to_datetime(df["criado_em"])
    return df


def main():
    st.title("📜 Histórico de Validações")

    db_manager = DatabaseManager()
    repo = db_manager.get_results_repository()

    df = carregar_dados(repo)

    if df.empty:
        st.info("Ainda não há registos gravados.")
        return

    st.markdown("Use os filtros abaixo para refinar a lista.")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        data_inicio = st.date_input(
            "De:",
            value=df["criado_em"].min().date() if not df.empty else None,
        )
    with col2:
        data_fim = st.date_input(
            "Até:",
            value=df["criado_em"].max().date() if not df.empty else None,
        )
    with col3:
        opcao_validez = st.selectbox(
            "Estado",
            options=["Todos", "Válidos", "Inválidos"],
            index=0,
        )

    filtrado = df.copy()

    if data_inicio:
        filtrado = filtrado[filtrado["criado_em"].dt.date >= data_inicio]
    if data_fim:
        filtrado = filtrado[filtrado["criado_em"].dt.date <= data_fim]

    if opcao_validez == "Válidos":
        filtrado = filtrado[filtrado["eh_valido"] == 1]
    elif opcao_validez == "Inválidos":
        filtrado = filtrado[filtrado["eh_valido"] == 0]

    st.markdown(f"**{len(filtrado)}** registos encontrados.")

    # Tabela resumida
    df_vis = filtrado[
        ["id", "nome_arquivo", "eh_valido", "mensagem", "criado_em"]
    ].assign(
        eh_valido=lambda x: x["eh_valido"].map({1: "✅ Válido", 0: "❌ Inválido"})
    )

    st.dataframe(df_vis, use_container_width=True)

    st.markdown("---")
    st.subheader("📄 Detalhes de um registo")

    if filtrado.empty:
        st.info("Nenhum registo no intervalo selecionado.")
        return

    ids = filtrado["id"].tolist()
    id_selecionado = st.selectbox("Selecionar ID", options=ids)
    linha = filtrado[filtrado["id"] == id_selecionado].iloc[0]

    st.markdown(
        f"**[{linha['id']}] {linha['nome_arquivo']}** — "
        f"{'✅ Válido' if linha['eh_valido'] == 1 else '❌ Inválido'}  "
        f" (`{linha['criado_em']}`)"
    )
    st.markdown(f"_Mensagem:_ {linha['mensagem']}")

    if linha["erros_brutos"]:
        with st.expander("Erros de validação", expanded=False):
            st.code(linha["erros_brutos"], language="text")

    if linha["explicacao_llm"]:
        with st.expander("Explicação do LLM", expanded=False):
            st.write(linha["explicacao_llm"])


if __name__ == "__main__":
    main()
