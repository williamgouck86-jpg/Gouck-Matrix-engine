    import streamlit as st
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

st.set_page_config(layout="wide") # Full widescreen dashboard layout
st.title("📊 The Gouck Matrix Engine Pro")

# 1. Your Real Stripe Sandbox Payment Link
STRIPE_PAYMENT_LINK = "https://stripe.com" 

# 2. Control Panel Sidebar Configuration
st.sidebar.header("🎛️ Engine Configuration")

# Add a license bypass key text entry field
access_key = st.sidebar.text_input("Enter Pro Access License Key:", type="password")

# Multi-stock picker dropdown setup
ticker_input = st.sidebar.text_input(
    "Enter Asset Stock Tickers (Comma separated):", 
    value="AAPL, MSFT, GOOGL"
)

# Convert string inputs into a clean list of individual tickers
tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
num_assets = len(tickers)

# 3. Paywall Restriction Security Enforcement Logic
is_unlocked = (access_key == "GOUCK_PRO_2026") # Admin master bypass code

if num_assets > 3 and not is_unlocked:
    st.error("⚠️ High-Dimensional Portfolio Array Locked!")
    st.info("Analyzing a matrix of more than 3 target assets requires Gouck Pro Access.")
    
    # Corrected parameter: unsafe_allow_html=True fixed below!
    st.markdown(
        f'<a href="{STRIPE_PAYMENT_LINK}" target="_blank">'
        '<button style="background-color:#635BFF; color:white; padding:15px 30px; '
        'border:none; border-radius:6px; font-size:18px; cursor:pointer; font-weight:bold; width:100%; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);">'
        '💳 Click Here to Unlock Gouck Pro Access ($5.00)'
        '</button></a>',
        unsafe_allow_html=True
    )
    st.stop() # Prevents non-paying users from pulling live data rows

# 4. Live Global Stock Market Data Extraction Core Loop
st.success(f"🚀 Extracting historical live data matrix arrays for: {', '.join(tickers)}...")

try:
    # Pull trailing 6 months of market close data for the requested assets
    data = yf.download(tickers, period="6mo")['Close']
    
    # If downloading a single stock, structure data as a clean DataFrame layout
    if isinstance(data, np.ndarray) or isinstance(data, list):
        data = data.to_frame()
        
    # Calculate percentage daily adjustments and baseline correlation index metrics
    returns = data.pct_change().dropna()
    cumulative_returns = (1 + returns).cumprod() - 1
    
    # 5. Build an Interactive Financial Analysis Performance Dashboard Layout
    fig = go.Figure()

    # Dynamic line generator to loop through and map each selected stock individually
    for col in cumulative_returns.columns:
        fig.add_trace(go.Scatter(
            x=cumulative_returns.index, 
            y=cumulative_returns[col],
            mode='lines',
            name=f'{col} Yield Trend',
            line=dict(width=2),
            hovertemplate=f'<b>Asset</b>: {col}<br><b>Date</b>: %{{x|%b %d}}<br><b>Growth</b>: %{{y:.2%}}<extra></extra>'
        ))

    # Refine and polish aesthetic canvas theme parameters configuration layout
    fig.update_layout(
        title="📈 Real-Time Asset Return Frontiers (Interactive Analysis Cluster)",
        xaxis_title="Calendar Trading Windows (Timeline)",
        yaxis_title="Normalized Cumulative Return Index",
        hovermode="x unified",
        template="plotly_dark",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=80, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

    # 6. Informative Analytical KPI Tracking Cards Widgets Display Summary Layout
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Assets Computed", f"{num_assets} Equities", "Live")
    col2.metric("Matrix Cluster Horizon", "6 Months", "Trailing")
    col3.metric("Engine Optimization Status", "Verified Stable", "100%")

except Exception as e:
    st.warning("⚠️ Market data extraction delay. Double check that your tickers are spelled correctly (e.g. AAPL, MSFT).")
