import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import time
import numpy as np

st.set_page_config(page_title="XAU/USD Gold Analyzer", layout="wide", page_icon="🪙")

st.title("🪙 XAU/USD Gold Real-Time Analyzer")
st.markdown("**Analisa teknikal real-time (RSI, MACD, SMA, EMA, Bollinger Bands)**")

# Sidebar
st.sidebar.header("Pengaturan")
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "30m", "1h"], index=2)
period = st.sidebar.selectbox("Periode Data", ["1d", "5d", "1mo", "3mo"], index=1)
refresh_rate = st.sidebar.slider("Refresh otomatis (detik)", 15, 180, 30)

@st.cache_data(ttl=refresh_rate)
def load_data():
    try:
        df = yf.download("GC=F", period=period, interval=timeframe, progress=False)
        if df.empty:
            return None
        return df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    except:
        return None

data = load_data()

if data is not None and len(data) > 50:
    # Hitung indikator manual (tanpa pandas_ta)
    close = data['Close']
    
    # SMA & EMA
    data['SMA20'] = close.rolling(window=20).mean()
    data['EMA50'] = close.ewm(span=50, adjust=False).mean()
    
    # RSI (14)
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    data['BB_middle'] = close.rolling(window=20).mean()
    data['BB_std'] = close.rolling(window=20).std()
    data['BB_upper'] = data['BB_middle'] + 2 * data['BB_std']
    data['BB_lower'] = data['BB_middle'] - 2 * data['BB_std']
    
    # MACD sederhana
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    data['MACD'] = ema12 - ema26
    data['MACD_signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

    latest = data.iloc[-1]
    prev = data.iloc[-2]

    # Header
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        change = latest['Close'] - prev['Close']
        st.metric("Harga XAU/USD", f"${latest['Close']:.2f}", f"{change:+.2f}")
    with col2:
        rsi_val = latest['RSI']
        rsi_status = "Oversold" if rsi_val < 30 else "Overbought" if rsi_val > 70 else "Neutral"
        st.metric("RSI (14)", f"{rsi_val:.1f}", rsi_status)
    with col3:
        st.metric("MACD", f"{latest['MACD']:.4f}")
    with col4:
        st.metric("Update", datetime.now().strftime("%H:%M:%S WIB"))

    # Sinyal Sederhana
    signal = "NEUTRAL"
    reasons = []
    if rsi_val < 30:
        signal = "STRONG BUY"
        reasons.append("RSI Oversold")
    elif rsi_val > 70:
        signal = "STRONG SELL"
        reasons.append("RSI Overbought")
    
    if latest['MACD'] > latest['MACD_signal'] and latest['MACD'] > 0:
        signal = "BUY" if signal == "NEUTRAL" else signal
        reasons.append("MACD Bullish")
    elif latest['MACD'] < latest['MACD_signal'] and latest['MACD'] < 0:
        signal = "SELL" if signal == "NEUTRAL" else signal
        reasons.append("MACD Bearish")
    
    if latest['Close'] > latest['EMA50']:
        reasons.append("Di atas EMA50 (Bullish)")

    st.subheader("🎯 Sinyal Analisa Saat Ini")
    if "STRONG BUY" in signal or "BUY" in signal:
        st.success(f"**{signal}** — {', '.join(reasons)}")
    elif "STRONG SELL" in signal or "SELL" in signal:
        st.error(f"**{signal}** — {', '.join(reasons)}")
    else:
        st.warning(f"**{signal}** — {', '.join(reasons) if reasons else 'Tidak ada sinyal kuat'}")

    # Chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'],
                                 low=data['Low'], close=data['Close'], name="Candlestick"))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'], name="SMA 20", line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA50'], name="EMA 50", line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_upper'], name="BB Upper", line=dict(color='gray', dash='dash')))
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_lower'], name="BB Lower", line=dict(color='gray', dash='dash')))

    fig.update_layout(title="Chart XAU/USD + Indikator", height=650, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Data Indikator Terbaru")
    st.dataframe(data.tail(5)[['Close', 'RSI', 'MACD', 'MACD_signal', 'BB_upper', 'BB_lower']].round(4))

    st.caption("⚠️ Tools analisa teknikal saja. Tidak ada jaminan akurasi 90%. Gunakan dengan manajemen risiko.")

    time.sleep(refresh_rate)
    st.rerun()

else:
    st.error("Gagal mengambil data. Coba refresh atau ganti timeframe.")
