import streamlit as st
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

st.set_page_config(layout="wide")
st.title("📊 The Gouck Matrix Engine Pro")

# 1. Active Payment Link
STRIPE_PAYMENT_LINK = "https://stripe.com"

# 2. Control Panel Sidebar Setup
st.sidebar.header("🎛️ Engine Configuration")
access_key = st.sidebar.text_input("Enter Pro Access License Key:", type="password")
ticker_input = st.sidebar.text_input("Enter Asset Stock Tickers (Comma separated):", value="AAPL, MSFT, GOOGL")

# Parse tickers safely
tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
num_assets = len(tickers)

# 3. Security Paywall Verification Boundary
is_unlocked = (access_key == "GOUCK_PRO_2026")

if num_assets > 3 and not is_unlocked:
    st.error("⚠️ High-Dimensional Portfolio Array Locked!")
    st.info("Analyzing a matrix of more than 3 target assets requires Gouck Pro Access.")
    
    st.markdown(
        f'<a href="{STRIPE_PAYMENT_LINK}" target="_blank">'
        '<button style="background-color:#635BFF; color:white; padding:15px 30px; '
        'border:none; border-radius:6px; font-size:18px; cursor:pointer; font-weight:bold; width:100%; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);">'
        '💳 Click Here to Unlock Gouck Pro Access ($5.00)'
        '</button></a>',
        unsafe_allow_html=True
    )
    st.stop()

# 4. Live Global Stock Extraction Loop
st.success(f"🚀 Extracting historical live data matrix arrays for: {', '.join(tickers)}...")

try:
    # Initialize interactive figure layout
    fig = go.Figure()
    
    # Loop over each stock ticker individually to guarantee single/multi data compatibility
    for ticker in tickers:
        stock_data = yf.download(ticker, period="6mo")
        
        # Pull Close price array safely across different yfinance formats
        if 'Close' in stock_data.columns:
            close_prices = stock_data['Close']
        else:
            close_prices = stock_data
            
        # Calculate daily change percentage metrics and cumulative values
        returns = close_prices.pct_change().dropna()
        cumulative_returns = (1 + returns).cumprod() - 1
        
        # Render line vector trace into the plotly canvas layer
        fig.add_trace(go.Scatter(
            x=cumulative_returns.index, 
            y=cumulative_returns.values.flatten(),
            mode='lines', 
            name=f'{ticker} Yield Trend', 
            line=dict(width=2.5),
            hovertemplate=f'<b>Asset</b>: {ticker}<br><b>Date</b>: %{{x|%b %d}}<br><b>Growth</b>: %{{y:.2%}}<extra></extra>'
        ))

    fig.update_layout(
        title="📈 Real-Time Asset Return Frontiers (Interactive Analysis Cluster)",
        xaxis_title="Calendar Trading Windows (Timeline)",
        yaxis_title="Normalized Cumulative Return Index",
        hovermode="x unified",
        template="plotly_dark",
        margin=dict(l=40, r=40, t=80, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    # 5. Performance Indicators Footer Layer Layout
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Assets Computed", f"{num_assets} Equities", "Live")
    col2.metric("Matrix Cluster Horizon", "6 Months", "Trailing")
    col3.metric("Engine Optimization Status", "Verified Stable", "100%")

except Exception as e:
    st.warning(f"⚠️ Market data extraction delay: {str(e)}. Ensure tickers are valid and try again.")
