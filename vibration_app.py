import streamlit as st
import numpy as np
import time
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

# Use a small tolerance range to capture "Critically Damped" due to floating point rounding
if np.isclose(damping_ratio, 1.0, atol=1e-2):
    status, color, note = "Critically Damped", "orange", "Fastest return to equilibrium."
    omega = 0.0
elif damping_ratio < 1:
    status, color, note = "Underdamped", "green", "The molecule wiggles before stopping."
    omega = np.sqrt(omega_0**2 - gamma**2)
else:
    status, color, note = "Overdamped", "red", "Movement is slow due to high friction."
    omega = 0.0

# 4. Top Metrics Display
st.divider()
m1, m2, m3 = st.columns([1, 1, 2])
with m1: 
    st.metric("Damping Ratio", f"{damping_ratio:.2f}")
with m2: 
    # Use st.markdown with standard color tags
    st.markdown(f"**Status:** :{color}[{status}]")
with m3: 
    st.info(note)
st.divider()

# 5. Visual Layout
col1, col2 = st.columns(2)

# 6. Execution Loop
if st.button('▶ Run Simulation (Live)'):
    t_history = []
    x_history = []
    
    with col1:
        atom_spot = st.empty()
    with col2:
        graph_spot = st.empty()

    for idx, t in enumerate(np.linspace(0, 20, 300)): 
        # --- CORRECTED PHYSICS LOGIC FOR ACCURATE CURVES ---
        if damping_ratio < 1:
            # Underdamped: Oscillates with decaying amplitude
            x = np.exp(-gamma * t) * np.cos(omega * t)
        elif damping_ratio == 1:
            # Critically Damped: Fast return to equilibrium without wiggling
            x = (1 + gamma * t) * np.exp(-gamma * t)
        else:
            # Overdamped: Heavy friction, slow drag back to equilibrium
            r1 = -gamma + np.sqrt(gamma**2 - omega_0**2)
            r2 = -gamma - np.sqrt(gamma**2 - omega_0**2)
            x = 0.5 * (np.exp(r1 * t) + np.exp(r2 * t))
            
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
        atom_spot.plotly_chart(fig_atom, use_container_width=True, config={'displayModeBar': False}, key=f"atom_{idx}")
        
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
        graph_spot.plotly_chart(fig_graph, use_container_width=True, config={'displayModeBar': False}, key=f"graph_{idx}")
        
        time.sleep(0.05)

# 7. Theory Section (Always Visible)
st.divider()
with st.expander("📖 View Mathematical Theory & Equations"):
    st.write("The motion of the molecule is modeled as a **Damped Harmonic Oscillator**:")
    st.latex(r"m \frac{d^2x}{dt^2} + c \frac{dx}{dt} + kx = 0")
    
    st.write(f"Based on your current settings (**{status}**), the motion is solved using:")
    
    # Dynamic Equation Display based on Damping Regime
    if damping_ratio < 1:
        st.latex(r"x(t) = e^{-\frac{c}{2m} t} \cos(\omega t)")
        st.caption(r"where $\omega = \sqrt{\omega_0^2 - \gamma^2}$ is the damped angular frequency.")
    elif np.isclose(damping_ratio, 1.0, atol=1e-2):
        st.latex(r"x(t) = \left(1 + \frac{c}{2m} t\right) e^{-\frac{c}{2m} t}")
        st.caption("Critical damping: Returns to equilibrium in minimum time without oscillating.")
    else:
        st.latex(r"x(t) = \frac{1}{2} \left( e^{r_1 t} + e^{r_2 t} \right)")
        st.caption(r"where roots $r_{1,2} = -\gamma \pm \sqrt{\gamma^2 - \omega_0^2}$ are real and negative.")
    
    st.info("""
    - **m**: Atomic Mass (kg)
    - **c**: Damping Coefficient (Friction/Viscosity)
    - **k**: Bond Stiffness (N/m)
    - **ω (Omega)**: Damped angular frequency
    """)
