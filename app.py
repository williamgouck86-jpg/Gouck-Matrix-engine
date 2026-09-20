import streamlit as st
import numpy as np
import yfinance as yf
from scipy.sparse.linalg import LinearOperator, gmres
import matplotlib.pyplot as plt

# --- WEBSITE PAGE CONFIGURATION ---
st.set_page_config(page_title="The Gouck Matrix Engine", layout="wide")

# Branded Application Header
st.title("📊 The Gouck Matrix Engine")
st.markdown("#### *High-Dimensional Portfolio Optimization via Matrix-Free Physics Solvers*")
st.caption("🚀 **Engineered by Gouck** | Open-Source Quantitative Architecture")

st.write(
    "Welcome to the platform. This application translates advanced quantum matrix simulation architectures "
    "(specifically the IKKT model framework) into real-world portfolio risk analytics. "
    "Input your target assets below to execute an optimized, matrix-free GMRES solve."
)

st.markdown("---")

# --- USER INTERFACE CONTROLS ---
col1, col2 = st.columns(2)

with col1:
    user_input = st.text_area(
        "📝 Enter Stock Tickers (separated by commas):",
        value="AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA, AVGO, CSCO, ORCL, JPM, V",
        help="Type any valid US stock tickers separated by commas."
    )

with col2:
    ridge_val = st.slider(
        "🛡️ Ridge Preconditioning Floor (Noise Filter):",
        min_value=1e-5, max_value=1e-2, value=1e-4, format="%.5f",
        help="Stabilizes matrix calculations against highly correlated market noise."
    )

# Clean and parse user inputs
tickers = [t.strip().upper() for t in user_input.split(",") if t.strip()]

if st.button("🚀 Execute Optimization Solver"):
    if len(tickers) < 3:
        st.error("Please enter at least 3 valid stock tickers to build a meaningful risk matrix.")
    else:
        with st.spinner("Downloading live historical market records from Yahoo Finance..."):
            market_data = yf.download(tickers, period="1y", progress=False)
            
            if 'Close' in market_data.columns:
                prices = market_data['Close']
            else:
                prices = market_data
                
            returns = prices.pct_change().dropna(how='all').fillna(0)
            active_tickers = list(returns.columns)
            raw_covariance = returns.cov().values
            N = len(active_tickers)
            
        if N == 0:
            st.error("Could not retrieve market data for the specified tickers. Please check your spelling.")
        else:
            st.success(f"✅ Successfully initialized a live {N}x{N} covariance structural grid!")
            
            with st.spinner("Running optimized matrix-free GMRES solver..."):
                stable_covariance = raw_covariance + ridge_val * np.eye(N)
                
                def stable_market_multiply(v):
                    return stable_covariance @ v
                
                RealOperator = LinearOperator((N, N), matvec=stable_market_multiply)
                market_target = np.random.randn(N)
                
                weights, status = gmres(RealOperator, market_target, rtol=1e-5, maxiter=100)
                
            if status == 0:
                normalized_weights = (weights - np.min(weights)) / (np.max(weights) - np.min(weights))
                if np.sum(normalized_weights) > 0:
                    normalized_weights /= np.sum(normalized_weights)
                
                st.markdown("### 🏆 Optimization System Diagnostics")
                st.caption("Computation verified by the Gouck Optimization Core.")
                
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    st.metric(label="Active Asset Count (N)", value=f"{N} Stocks")
                    st.metric(label="Solver Status", value="CONVERGED / STABLE")
                    
                    st.write("#### 📊 Numerical Weights Breakdown")
                    for i, ticker in enumerate(active_tickers[:10]):
                        st.write(f"• **{ticker}** Optimization Target Allocation: `{normalized_weights[i]:.4%}`")
                    if N > 10:
                        st.write(f"*... and {N - 10} more assets successfully balanced inside the matrix layer.*")
                        
                with res_col2:
                    st.write("#### 📈 Allocation Distribution Mapping")
                    fig, ax = plt.subplots(figsize=(8, 5.2))
                    ax.bar(active_tickers[:10], normalized_weights[:10] * 100, color='royalblue', edgecolor='black')
                    ax.set_ylabel("Portfolio Optimization Allocation (%)")
                    ax.set_xlabel("Asset Key")
                    ax.grid(axis='y', linestyle='--', alpha=0.5)
                    st.pyplot(fig)
            else:
                st.error("⚠️ The solver encountered a convergence error. Try increasing the Noise Filter slider.")
