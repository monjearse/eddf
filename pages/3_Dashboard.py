import pandas as pd
import streamlit as st

from database import DatabaseManager


# ============================================================
# Funções utilitárias
# ============================================================
def carregar_validacoes(repo) -> pd.DataFrame:
    registos = list(repo.listar_ultimos(limite=1000))
    if not registos:
        return pd.DataFrame(columns=[
            "id", "nome_arquivo", "eh_valido", "mensagem",
            "erros_brutos", "explicacao_llm", "criado_em"
        ])

    df = pd.DataFrame(registos, columns=[
        "id", "nome_arquivo", "eh_valido", "mensagem",
        "erros_brutos", "explicacao_llm", "criado_em"
    ])
    df["criado_em"] = pd.to_datetime(df["criado_em"])
    df["dia"] = df["criado_em"].dt.date
    return df


def carregar_integracoes(repo) -> pd.DataFrame:
    registos = list(repo.listar_ultimas(limite=1000))
    if not registos:
        return pd.DataFrame(columns=[
            "id", "nome_arquivo", "sucesso",
            "status_http", "resposta", "criado_em"
        ])

    df = pd.DataFrame(registos, columns=[
        "id", "nome_arquivo", "sucesso",
        "status_http", "resposta", "criado_em"
    ])
    df["criado_em"] = pd.to_datetime(df["criado_em"])
    df["dia"] = df["criado_em"].dt.date
    return df


# ============================================================
# Dashboard principal
# ============================================================
def main():
    st.title("📊 Dashboard EDDF — Processamento & Integração ERP")

    db_manager = DatabaseManager()
    valid_repo = db_manager.get_results_repository()
    erp_repo = db_manager.get_erp_repository()

    df_valid = carregar_validacoes(valid_repo)
    df_integ = carregar_integracoes(erp_repo)

    if df_valid.empty and df_integ.empty:
        st.info("Ainda não há dados suficientes para o dashboard.")
        return

    # ============================================================
    # KPIs gerais
    # ============================================================
    st.markdown("## 📌 Indicadores principais")

    total_processados = len(df_valid)
    total_validos = int((df_valid["eh_valido"] == 1).sum())
    total_invalidos = int((df_valid["eh_valido"] == 0).sum())

    total_integracoes = len(df_integ)
    total_integ_sucesso = int((df_integ["sucesso"] == 1).sum())
    total_integ_falha = int((df_integ["sucesso"] == 0).sum())

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("XML processados", total_processados)
    col2.metric("Válidos", total_validos)
    col3.metric("Inválidos", total_invalidos)
    col4.metric("Taxa Validação", f"{(total_validos / total_processados) * 100:.1f}%")

    st.markdown("---")

    col5, col6, col7 = st.columns(3)
    col5.metric("Integrações ERP", total_integracoes)
    col6.metric("Sucesso na Integração", total_integ_sucesso)
    col7.metric("Falhas na Integração", total_integ_falha)

    # ============================================================
    # Filtros
    # ============================================================
    st.markdown("## 🔍 Filtros")

    colA, colB, colC = st.columns(3)

    with colA:
        filtro_data_inicio = st.date_input("Data inicial", value=None)

    with colB:
        filtro_data_fim = st.date_input("Data final", value=None)

    with colC:
        filtro_status_integ = st.selectbox(
            "Status integração ERP",
            ["Todos", "Sucesso", "Falha"]
        )

    df_filt = df_integ.copy()

    # Aplicar filtros
    if filtro_data_inicio:
        df_filt = df_filt[df_filt["criado_em"] >= pd.to_datetime(filtro_data_inicio)]

    if filtro_data_fim:
        df_filt = df_filt[df_filt["criado_em"] <= pd.to_datetime(filtro_data_fim)]

    if filtro_status_integ == "Sucesso":
        df_filt = df_filt[df_filt["sucesso"] == 1]
    elif filtro_status_integ == "Falha":
        df_filt = df_filt[df_filt["sucesso"] == 0]

    # ============================================================
    # 📈 Gráfico: Processamento por dia
    # ============================================================
    st.markdown("## 📈 Processamentos por dia")

    por_dia = df_valid.groupby("dia")["id"].count().reset_index()
    por_dia = por_dia.rename(columns={"id": "Quantidade"})

    st.line_chart(por_dia.set_index("dia")["Quantidade"])

    st.markdown("---")

    # ============================================================
    # 📈 Gráfico: Integrações ERP por dia
    # ============================================================
    st.markdown("## 🔗 Integrações ERP por dia")

    por_dia_integ = df_integ.groupby("dia")["id"].count().reset_index()
    por_dia_integ = por_dia_integ.rename(columns={"id": "Integrações"})

    st.area_chart(por_dia_integ.set_index("dia")["Integrações"])

    st.markdown("---")

    # ============================================================
    # 📌 Tabela detalhada com filtros
    # ============================================================
    st.markdown("## 📋 Registos de Integração ERP")

    df_filt["StatusTxt"] = df_filt["sucesso"].replace({1: "🟢 Sucesso", 0: "🔴 Falha"})

    st.dataframe(
        df_filt[[
            "id", "nome_arquivo", "StatusTxt", "status_http",
            "resposta", "criado_em"
        ]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ============================================================
    # Erros mais comuns
    # ============================================================
    st.markdown("## ❗ Erros mais frequentes na integração")

    df_filt["TamanhoResposta"] = df_filt["resposta"].astype(str).str.len()

    erros_top = df_filt.sort_values("TamanhoResposta", ascending=False).head(10)

    if erros_top.empty:
        st.info("Ainda não há falhas suficientes para análise.")
    else:
        st.table(
            erros_top[[
                "id", "nome_arquivo", "StatusTxt",
                "status_http", "TamanhoResposta", "criado_em"
            ]]
        )



    # ============================================================
    # 🧠 Análise LLM – Insights Inteligentes sobre o Processo
    # ============================================================
    st.markdown("## 🧠 Análise Inteligente (Gemini)")

    from llm_client import LLMClient

    llm = LLMClient()

    # Construção do contexto para análise
    total_proc = total_processados
    total_validos = total_validos
    total_invalidos = total_invalidos
    total_integ = total_integracoes
    integ_sucesso = total_integ_sucesso
    integ_falha = total_integ_falha

    erros_validacao = df_valid["erros_brutos"].dropna().tolist()
    respostas_erp = df_integ["resposta"].dropna().tolist()

    contexto_analise = {
        "total_processados": total_proc,
        "validados_com_sucesso": total_validos,
        "validados_com_erro": total_invalidos,
        "total_integracoes": total_integ,
        "integracoes_sucesso": integ_sucesso,
        "integracoes_falha": integ_falha,
        "exemplos_erros_validacao": erros_validacao[:5],
        "exemplos_erros_erp": respostas_erp[:5],
    }

    prompt = f"""
    Você é um analista fiscal e técnico especializado em XML NFe, integrações ERP, 
    e análise de operações. Avalie o seguinte contexto estatístico do sistema EDDF:

    {contexto_analise}

    Gere uma análise COMPLETA respondendo:

    1) Quais são os principais padrões de erro de validação dos XMLs?
    2) Quais erros mais contribuem para reprovações?
    3) Quais são os padrões de falha nas integrações ERP?
    4) Sugira melhorias técnicas no fluxo EDDF (validação → correção → integração).
    5) Dê sugestões práticas para melhorar a qualidade dos XMLs recebidos.
    6) Classifique a "Saúde Geral do Processo" numa escala de 0 a 100.
    7) Liste recomendações objetivas a curto e médio prazo.

    Seja objetivo, estruturado e claro.
    """

    try:
        analise = llm.simple(prompt)
        st.info("A análise abaixo foi gerada automaticamente pelo motor LLM Gemini.")
        st.write(analise)

    except Exception as e:
        st.error(f"Erro ao gerar análise LLM: {e}")

if __name__ == "__main__":
    main()
