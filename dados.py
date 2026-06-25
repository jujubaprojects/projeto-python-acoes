import yfinance as yf
import pandas as pd

TICKERS = {
    "Petrobras": "PETR4.SA",
    "Itaú": "ITUB4.SA",
    "Vale": "VALE3.SA",
}

def buscar_acoes(inicio="2025-01-02", fim=None):
    tickers = list(TICKERS.values())
    df = yf.download(tickers, start=inicio, end=fim, auto_adjust=True)["Close"]
    df.columns = list(TICKERS.keys())
    df.dropna(how="all", inplace=True)
    return df

def calcular_performance(df):
    primeiro = df.iloc[0]
    return ((df / primeiro) - 1) * 100

def metricas_por_acao(df):
    metricas = {}
    for nome in df.columns:
        serie = df[nome].dropna()
        if len(serie) < 2:
            continue
        preco_atual = serie.iloc[-1]
        preco_inicial = serie.iloc[0]
        preco_ontem = serie.iloc[-2]
        variacao_ano = ((preco_atual / preco_inicial) - 1) * 100
        variacao_dia = ((preco_atual / preco_ontem) - 1) * 100
        metricas[nome] = {
            "preco_atual": preco_atual,
            "variacao_ano": variacao_ano,
            "variacao_dia": variacao_dia,
        }
    return metricas
