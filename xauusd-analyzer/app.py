import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="XAU/USD Gold Analyzer", layout="wide", page_icon="🪙")
st.title("🪙 XAU/USD Gold Real-Time Analyzer")
st.markdown("**Analisa teknikal real-time: RSI, MACD, Bollinger Bands, Moving Averages**")

# Sidebar
st.sidebar.header("Pengaturan Analisa")
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "30m", "1h"], index=2)
period = st.sidebar.selectbox("Periode Data", ["1d", "5d", "1mo", "3mo"], index=1)
refresh = st.sidebar.slider("Refresh otomatis (detik)", 15, 180, 30)

# Ambil data
@st.cache_data(ttl=refresh)
def load_data():
    try:
        df = yf.download("GC=F", period=period, interval=timeframe, progress=False)
        if df.empty:
            st.error("Data tidak tersedia. Coba ganti timeframe.")
            return None
        return df[['Open', 'High', 'Low', 'Close', 'Volume']]
    except:
        st.error("Gagal mengambil data dari Yahoo Finance. Coba lagi nanti.")
        return None

data = load_data()

if data is not None and len(data) > 50:
    # Hitung indikator
    data['SMA20'] = ta.sma(data['Close'], length=20)
    data['EMA50'] = ta.ema(data['Close'], length=50)
    data['RSI'] = ta.rsi(data['Close'], length=14)
    bb = ta.bbands(data['Close'], length=20, std=2)
    data = pd.concat([data, bb], axis=1)
    macd = ta.macd(data['Close'], fast=12, slow=26, signal=9)
    data = pd.concat([data, macd], axis=1)

    latest = data.iloc[-1]
    prev = data.iloc[-2]

    # Header harga
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        change = latest['Close'] - prev['Close']
        st.metric("Harga XAU/USD", f"${latest['Close']:.2f}", f"{change:+.2f}")
    with col2:
        rsi_val = latest['RSI']
        rsi_status = "🟢 Oversold" if rsi_val < 30 else "🔴 Overbought" if rsi_val > 70 else "🟡 Neutral"
        st.metric("RSI (14)", f"{rsi_val:.1f}", rsi_status)
    with col3:
        st.metric("MACD", f"{latest.get('MACD_12_26_9', 0):.4f}")
    with col4:
        st.metric("Update Terakhir", datetime.now().strftime("%H:%M:%S WIB"))

    # Sinyal Analisa
    signal = "🟡 NEUTRAL"
    reasons = []

    if rsi_val < 30:
        signal = "🟢 STRONG BUY"
        reasons.append("RSI Oversold")
    elif rsi_val > 70:
        signal = "🔴 STRONG SELL"
        reasons.append("RSI Overbought")

    macd_line = latest.get('MACD_12_26_9', 0)
    macd_signal = latest.get('MACDs_12_26_9', 0)
    if macd_line > macd_signal and macd_line > 0:
        if "BUY" not in signal:
            signal = "🟢 BUY" if signal == "🟡 NEUTRAL" else signal
        reasons.append("MACD Bullish Crossover")
    elif macd_line < macd_signal and macd_line < 0:
        if "SELL" not in signal:
            signal = "🔴 SELL" if signal == "🟡 NEUTRAL" else signal
        reasons.append("MACD Bearish Crossover")

    if latest['Close'] > latest['EMA50'] > latest['SMA20']:
        reasons.append("Trend Bullish (di atas MA)")
    elif latest['Close'] < latest['EMA50']:
        reasons.append("Trend Bearish")

    st.subheader("🎯 Sinyal Saat Ini")
    if "STRONG BUY" in signal or "BUY" in signal:
        st.success(f"**{signal}**\n\n{', '.join(reasons)}")
    elif "STRONG SELL" in signal or "SELL" in signal:
        st.error(f"**{signal}**\n\n{', '.join(reasons)}")
    else:
        st.warning(f"**{signal}**\n\n{', '.join(reasons) if reasons else 'Tidak ada sinyal kuat saat ini'}")

    # Chart Interaktif
    fig = go.Figure(data=[
        go.Candlestick(x=data.index,
                       open=data['Open'],
                       high=data['High'],
                       low=data['Low'],
                       close=data['Close'],
                       name="Candlestick")
    ])

    fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'], name="SMA 20", line=dict(color="orange")))
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA50'], name="EMA 50", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=data.index, y=data['BBU_20_2.0'], name="Bollinger Upper", line=dict(color="gray", dash="dash")))
    fig.add_trace(go.Scatter(x=data.index, y=data['BBL_20_2.0'], name="Bollinger Lower", line=dict(color="gray", dash="dash")))

    fig.update_layout(title="Chart XAU/USD + Indikator Teknis", xaxis_title="Waktu", yaxis_title="Harga USD", height=650, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Data Indikator Terbaru (5 baris)")
    st.dataframe(data.tail(5)[['Close', 'RSI', 'MACD_12_26_9', 'MACDs_12_26_9', 'BBU_20_2.0', 'BBL_20_2.0']].round(4))

    st.caption("⚠️ Catatan Penting: Ini hanya alat bantu analisa teknikal. Akurasi tidak pernah 100%. Selalu gunakan manajemen risiko dan kombinasikan dengan analisa fundamental. Trading berisiko tinggi.")

    # Auto refresh
    time.sleep(refresh)
    st.rerun()

else:
    st.info("Menunggu data... Pastikan koneksi internet stabil.")
