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
if st.button('▶ Run Simulation (Live)'):
    t_history = []
    x_history = []
    
    # Create placeholders so the charts stay in the same spot
    with col1:
        atom_spot = st.empty()
    with col2:
        graph_spot = st.empty()

    for t in np.linspace(0, 20, 300): # Reduced to 300 steps for speed
        x = np.exp(-gamma * t) * np.cos(omega * t)
        t_history.append(t)
        x_history.append(x)
        
        # 1. Update Atom Animation (Left)
        fig_atom = go.Figure(go.Scatter(
            x=[-1.5, 1.5 + x], y=[0, 0],
            mode='markers+lines',
            marker=dict(size=40, color=['#FF4B4B', '#1C83E1']),
            line=dict(color='gray', width=4)
        ))
        fig_atom.update_layout(
            xaxis=dict(range=[-5, 5], visible=False),
            yaxis=dict(range=[-1, 1], visible=False),
            height=300, margin=dict(l=0, r=0, t=0, b=0)
        )
        atom_spot.plotly_chart(fig_atom, use_container_width=True, config={'displayModeBar': False})
        
        # 2. Update Displacement Graph (Right)
        fig_graph = go.Figure(go.Scatter(
            x=t_history, y=x_history,
            mode='lines',
            line=dict(color='#FF4B4B', width=2)
        ))
        fig_graph.update_layout(
            xaxis=dict(range=[0, 20], title="Time (s)"),
            yaxis=dict(range=[-1.2, 1.2], title="Displacement"),
            height=300, margin=dict(l=0, r=0, t=0, b=0)
        )
        graph_spot.plotly_chart(fig_graph, use_container_width=True, config={'displayModeBar': False})
        
        # Small sleep to keep it looking like a real-time process
        time.sleep(0.05)

# 7. Theory Section (Always Visible)
st.divider()
with st.expander("📖 View Mathematical Theory & Equations"):
    st.write("The motion of the molecule is modeled as a **Damped Harmonic Oscillator**:")
    st.latex(r"m \frac{d^2x}{dt^2} + c \frac{dx}{dt} + kx = 0")
    
    st.write("Depending on your sliders, the system is solved using the following formula:")
    st.latex(r"x(t) = e^{-\frac{c}{2m} t} \cos\left(\omega t\right)")
    
    st.info("""
    - **m**: Atomic Mass (kg)
    - **c**: Damping Coefficient (Friction/Viscosity)
    - **k**: Bond Stiffness (N/m)
    - **ω (Omega)**: Damped angular frequency
    """)