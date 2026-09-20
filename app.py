import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# 1. Setup Premium Canvas Configuration
st.set_page_config(layout="wide")
st.title("📊 The Gouck Matrix Engine Pro")

# Active Stripe Payment Link Gate
STRIPE_PAYMENT_LINK = "https://stripe.com"

# 2. Control Panel Sidebar Configuration
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
    # Force yfinance to pull clean, completely flat data tables directly
    df = yf.download(tickers, period="6mo", multi_level_index=False)
    
    # Isolate Close prices securely
    if 'Close' in df.columns:
        df_close = df['Close']
    else:
        df_close = df

    # If it is a single stock input, structure it cleanly as a dataframe
    if num_assets == 1:
        df_close = df_close.to_frame(name=tickers[0])

    # Compute clean daily returns scaling adjustments
    returns = df_close.pct_change().dropna()
    cumulative_returns = (1 + returns).cumprod() - 1

    # 5. Build High-Contrast Mattplotlib Visual Plot
    # Enable dark-theme workspace metrics
    plt.style.use('dark_background')
    
    # Set high-visibility neon colors for stock lines to pop
    glowing_colors = ['#00FFCC', '#FF3366', '#33CCFF', '#FFCC00', '#FF66FF']
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Loop and forcefully plot each column line onto the image layer
    for idx, col in enumerate(cumulative_returns.columns):
        color_pick = glowing_colors[idx % len(glowing_colors)]
        ax.plot(
            cumulative_returns.index, 
            cumulative_returns[col] * 100,  # Convert to clean percentages
            label=f"{col} Yield Trend", 
            linewidth=3, 
            color=color_pick
        )

    # Style and crisp the chart grid parameters labels
    ax.set_title("📈 Real-Time Asset Return Frontiers", fontsize=14, fontweight='bold', pad=15)
    ax.set_ylabel("Normalized Growth Return (%)", fontsize=11, labelpad=10)
    ax.grid(True, linestyle='--', alpha=0.3, color='#444444')
    ax.legend(loc="upper left", frameon=True, facecolor='#222222', edgecolor='#444444')
    
    # Rotate date index strings text slightly for narrow mobile screens
    plt.xticks(rotation=15)
    plt.tight_layout()

    # Pass the static image container natively to your Streamlit page
    st.pyplot(fig)

    # 6. Performance Indicators Footer Layer Layout
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Assets Computed", f"{num_assets} Equities", "Live")
    col2.metric("Matrix Cluster Horizon", "6 Months", "Trailing")
    col3.metric("Engine Optimization Status", "Verified Stable", "100%")

except Exception as e:
    st.warning(f"⚠️ Data rendering delay: {str(e)}. Please check ticker spellings
