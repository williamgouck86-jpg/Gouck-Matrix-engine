import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide") # Expands the canvas for a premium dashboard look
st.title("📊 The Gouck Matrix Engine")

# 1. Your Real Stripe Sandbox Payment Link Updated Directly Below
STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_9B600i12x17f4Osce34Vy00" 

# 2. Setup the sidebar settings panel
st.sidebar.header("🎛️ Control Panel")
matrix_size = st.sidebar.slider("Select Matrix Dimension Size (N x N):", min_value=2, max_value=500, value=15)
solver_iterations = st.sidebar.slider("Max GMRES Iterations:", 10, 200, 50)

# 3. Paywall Logic Enforcement
if matrix_size > 50:
    st.error("⚠️ High-Dimensional Solver Locked!")
    st.info("Computing dimensions greater than 50x50 requires a one-time product license.")
    
    # Render a stylized purple Stripe call-to-action button
    st.markdown(
        f'<a href="{STRIPE_PAYMENT_LINK}" target="_blank">'
        '<button style="background-color:#635BFF; color:white; padding:15px 30px; '
        'border:none; border-radius:6px; font-size:18px; cursor:pointer; font-weight:bold; width:100%; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);">'
        '💳 Click Here to Unlock Gouck Pro Access ($5.00)'
        '</button></a>',
        unsafe_url=True
    )
    st.stop() # Stops execution here so free users cannot access premium graphics data

# 4. Standard Math Engine Generation Loop (Simulating a Matrix Solver)
st.success(f"🚀 Running baseline Gouck Matrix Engine solver for a {matrix_size}x{matrix_size} system...")

# Generate realistic, dynamic portfolio optimization data arrays
steps = solver_iterations
x_data = np.arange(steps)
residual_error = np.exp(-x_data / (matrix_size * 0.5)) + np.random.normal(0, 0.02, steps)
residual_error = np.clip(residual_error, 1e-5, 2.0) # bound data cleanly

portfolio_return = np.cumsum(np.random.normal(0.001, 0.02, steps)) + 0.1
portfolio_risk = np.abs(np.sin(x_data / 10) * 0.15 + np.random.normal(0, 0.005, steps))

# 5. Build an Exciting, Fully Interactive Multi-Tab Plotly Graph Window
fig = go.Figure()

# Add Convergence Speed Line Curve
fig.add_trace(go.Scatter(
    x=x_data, y=residual_error,
    mode='lines+markers',
    name='Solver Residual Error',
    line=dict(color='#FF4B4B', width=3),
    marker=dict(size=5, symbol='circle'),
    hovertemplate='<b>Iteration</b>: %{x}<br><b>Error Drop</b>: %{y:.4f}<extra></extra>'
))

# Add Portfolio Return Variance Wave Curve
fig.add_trace(go.Scatter(
    x=x_data, y=portfolio_return,
    mode='lines',
    name='Projected Asset Yield',
    line=dict(color='#00CC96', width=3, dash='dash'),
    hovertemplate='<b>Iteration</b>: %{x}<br><b>Yield</b>: %{y:.2%}<extra></extra>'
))

# Add Risk Frontier Area Shade Chart
fig.add_trace(go.Scatter(
    x=x_data, y=portfolio_risk,
    mode='lines',
    name='Risk Margin Boundary',
    fill='tozeroy',
    line=dict(color='#635BFF', width=1),
    hovertemplate='<b>Iteration</b>: %{x}<br><b>Risk Value</b>: %{y:.4f}<extra></extra>'
))

# Style and polish dashboard canvas parameters layout
fig.update_layout(
    title=f"📈 Live Linear Algebra Solver Analysis Layer ({matrix_size}x{matrix_size} Grid)",
    xaxis_title="Algorithm Progression Cycles (Iterations)",
    yaxis_title="Normalized Value Index Metric",
    hovermode="x unified", 
    template="plotly_dark", 
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=40, r=40, t=80, b=40)
)

# Display the high-performance visualization container natively inside your Streamlit page
st.plotly_chart(fig, use_container_width=True)

# 6. Add metrics indicator counters summary below chart
col1, col2, col3 = st.columns(3)
col1.metric("Final Matrix Dimension Level", f"{matrix_size} x {matrix_size}", "+Baseline")
col2.metric("Convergence Steps Executed", f"{steps} Cycles", "Optimal")
col3.metric("Engine Operating Stability Status", "Active", "100%", delta_color="inverse")
