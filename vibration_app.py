import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Molecular Vibration Lab")
st.title("Molecular Vibration & Damping Analysis")

# 2. Sidebar Presets & Controls
st.sidebar.header("Classroom Presets")
presets = {
    "Manual Control": {"m": 2.0, "k": 20, "c": 0.2},
    "Light Molecule (High Freq)": {"m": 1.0, "k": 40, "c": 0.1},
    "Heavy Molecule (Low Freq)": {"m": 8.0, "k": 10, "c": 0.3},
    "Oil/Viscous Environment": {"m": 2.0, "k": 20, "c": 1.8},
    "Critical Damping Demo": {"m": 2.0, "k": 20, "c": 12.6}
}

selection = st.sidebar.selectbox("Choose a Scenario", list(presets.keys()))
p = presets[selection]

st.sidebar.divider()
st.sidebar.header("Fine Tuning")
m = st.sidebar.slider("Atomic Mass", 0.5, 10.0, float(p["m"]))
k = st.sidebar.slider("Bond Stiffness", 1, 100, int(p["k"]))
c = st.sidebar.slider("Damping Coefficient", 0.0, 15.0, float(p["c"]))

# 3. Physics & Damping Logic
damping_ratio = c / (2 * np.sqrt(m * k))
gamma = c / (2 * m)
omega_0 = np.sqrt(k / m)
omega = np.sqrt(max(0, omega_0**2 - gamma**2))

if damping_ratio < 1:
    status, color, note = "Underdamped", "green", "The molecule wiggles before stopping."
elif damping_ratio == 1:
    status, color, note = "Critically Damped", "orange", "Fastest return to equilibrium."
else:
    status, color, note = "Overdamped", "red", "Movement is slow due to high friction."

# 4. Top Metrics Display
st.divider()
m1, m2, m3 = st.columns([1, 1, 2])
with m1: st.metric("Damping Ratio", f"{damping_ratio:.2f}")
with m2: st.markdown(f"**Status:** :{color}[{status}]")
with m3: st.info(note)
st.divider()

# 5. Visual Layout
col1, col2 = st.columns(2)

# 6. Execution Loop
if st.button('▶ Run Simulation (Optimized)'):
    # 1. Generate all data at once
    t_vals = np.linspace(0, 20, 200)
    x_vals = np.exp(-gamma * t_vals) * np.cos(omega * t_vals)
    
    # 2. Create the Plotly Figure
    fig = go.Figure(
        data=[
            # The Atoms
            go.Scatter(x=[-1.5, 1.5 + x_vals[0]], y=[0, 0], 
                       mode='markers+lines',
                       marker=dict(size=40, color=['red', 'blue']),
                       line=dict(color='gray', width=4))
        ],
        layout=go.Layout(
            xaxis=dict(range=[-5, 5], autorange=False, visible=False),
            yaxis=dict(range=[-1, 1], autorange=False, visible=False),
            title="Fluid Molecular Vibration",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None, {"frame": {"duration": 20, "redraw": True}, "fromcurrent": True}])])]
        ),
        frames=[go.Frame(data=[go.Scatter(x=[-1.5, 1.5 + x_vals[i]], y=[0, 0])]) 
                for i in range(len(t_vals))]
    )
    
#    st.plotly_chart(fig, use_container_width=True)
    with col1:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# And let's add the static full graph to col2 for a complete view
    with col2:
        fig_graph = go.Figure()
        fig_graph.add_trace(go.Scatter(x=t_vals, y=x_vals, line=dict(color='#FF4B4B')))
        fig_graph.update_layout(title="Full Displacement History", xaxis_title="Time (s)", yaxis_title="x")
        st.plotly_chart(fig_graph, use_container_width=True)

# 7. Theory Section
with st.expander("View Mathematical Theory"):
    st.latex(r"m \frac{d^2x}{dt^2} + c \frac{dx}{dt} + kx = 0")
    st.write("The solution for underdamped vibration:")
    st.latex(r"x(t) = e^{-\frac{c}{2m} t} \cos\left(\sqrt{\frac{k}{m} - (\frac{c}{2m})^2} \cdot t\right)")