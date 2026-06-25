# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Install dependencies:**
```
pip install -r requirements.txt
```

**Run the app:**
```
streamlit run app.py
```

## Architecture

Two-file structure with a clear separation of concerns:

- **`dados.py`** — data layer. Fetches closing prices from Yahoo Finance (`yfinance`) for three Brazilian stocks (PETR4, VALE3, ITUB4) and exposes three pure functions: `buscar_acoes`, `calcular_performance`, and `metricas_por_acao`. No UI code here.
- **`app.py`** — presentation layer. Streamlit app that calls `dados.py` and renders metric cards, a historical price chart, and a cumulative-performance chart using Plotly.

The app tracks 2025 year-to-date data by default (`inicio="2025-01-02"` in `buscar_acoes`). To change the tracked tickers or date range, edit the `TICKERS` dict and `inicio` default in `dados.py`.
