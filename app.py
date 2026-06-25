import streamlit as st
import plotly.graph_objects as go
from dados import buscar_acoes, calcular_performance, metricas_por_acao

st.set_page_config(page_title="Ações 2025", page_icon="📈", layout="wide")

st.title("📈 Análise de Ações — 2025")
st.caption("Petrobras (PETR4) · Itaú (ITUB4) · Vale (VALE3)")

with st.spinner("Buscando dados..."):
    df = buscar_acoes()

if df.empty:
    st.error("Não foi possível carregar os dados. Verifique sua conexão.")
    st.stop()

metricas = metricas_por_acao(df)

# --- Cards de métricas ---
st.subheader("Resumo")
cols = st.columns(3)
for col, (nome, m) in zip(cols, metricas.items()):
    cor_ano = "normal" if m["variacao_ano"] >= 0 else "inverse"
    cor_dia = "normal" if m["variacao_dia"] >= 0 else "inverse"
    with col:
        st.metric(
            label=nome,
            value=f"R$ {m['preco_atual']:.2f}",
            delta=f"{m['variacao_dia']:+.2f}% hoje",
        )
        st.caption(f"Performance no ano: **{m['variacao_ano']:+.2f}%**")

st.divider()

# --- Gráfico de preço histórico ---
st.subheader("Preço de Fechamento (R$)")
fig_preco = go.Figure()
for nome in df.columns:
    fig_preco.add_trace(go.Scatter(
        x=df.index, y=df[nome],
        name=nome, mode="lines",
        hovertemplate="%{x|%d/%m/%Y}<br>R$ %{y:.2f}<extra>" + nome + "</extra>",
    ))
fig_preco.update_layout(
    xaxis_title="Data",
    yaxis_title="Preço (R$)",
    hovermode="x unified",
    legend=dict(orientation="h", y=1.1),
    height=400,
)
st.plotly_chart(fig_preco, use_container_width=True)

# --- Gráfico de performance comparada ---
st.subheader("Performance Comparada (% acumulado desde jan/2025)")
perf = calcular_performance(df)
fig_perf = go.Figure()
for nome in perf.columns:
    fig_perf.add_trace(go.Scatter(
        x=perf.index, y=perf[nome],
        name=nome, mode="lines",
        hovertemplate="%{x|%d/%m/%Y}<br>%{y:+.2f}%<extra>" + nome + "</extra>",
    ))
fig_perf.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
fig_perf.update_layout(
    xaxis_title="Data",
    yaxis_title="Retorno acumulado (%)",
    hovermode="x unified",
    legend=dict(orientation="h", y=1.1),
    height=400,
)
st.plotly_chart(fig_perf, use_container_width=True)

# --- Tabela de dados brutos ---
with st.expander("Ver dados brutos"):
    st.dataframe(
        df.sort_index(ascending=False).style.format("R$ {:.2f}"),
        use_container_width=True,
    )
