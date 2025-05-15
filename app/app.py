import numpy as np
import streamlit as st
from damper.input import DamperSystem, InitialConditions
from damper.plots import generate_phase_plot, generate_time_evolution_plot

initial_params = DamperSystem(
    m=1.0,
    k=1.0,
    c=1.0,
    start_time=0.0,
    end_time=100.0,
    ics=InitialConditions(x0=0.0, v0=1.0, n_lines=1),
)


def log_system_properties(c_val, m_val, k_val):
    p = -c_val / m_val
    q = k_val / m_val
    delta = (c_val / m_val) ** 2 - 4 * k_val / m_val

    charact_expander = st.sidebar.expander("System Characteristics")

    if np.isclose(c_val, 0):
        system_type = "No damping, center"
    elif delta < 0:
        system_type = "Underdamping, stable and attractive spiral"
    elif delta == 0:
        system_type = "Critical damping, stable and attractive point"
    elif delta > 0:
        system_type = "Overdamping, stable and attractive"
    elif p >= 0:
        system_type = "Unstable"
    else:
        system_type = "Other"

    markdown_string = f"""
        * **p value:** {p:.2f}
        * **q value:** {q:.2f}
        * **Δ value:** {delta:.2f}
        * **λ¹ value:** {(p+delta**0.5)/2:.2f}
        * **λ² value:** {(p-delta**0.5)/2:.2f}
        * **System type:** {system_type}
    """
    charact_expander.markdown(markdown_string)


def setup_sidebar():
    st.sidebar.header("System Parameters")
    system_expander = st.sidebar.expander("Edit Parameters")
    mass_slider = system_expander.slider(
        "Mass M",
        0.0,
        20.0,
        st.session_state.system_params.m,
        key="mass_slider",
    )
    spring_slider = system_expander.slider(
        "Spring K",
        0.0,
        20.0,
        st.session_state.system_params.k,
        key="spring_slider",
    )
    damper_slider = system_expander.slider(
        "Damper C",
        0.0,
        20.0,
        st.session_state.system_params.c,
        key="damper_slider",
    )
    log_system_properties(damper_slider, mass_slider, spring_slider)
    st.sidebar.header("Initial Conditions")
    ics_expander = st.sidebar.expander("Edit ICs")
    x0_slider = ics_expander.slider(
        "Initial Displacement (x₀)",
        -5.0,
        5.0,
        st.session_state.system_params.ics.x0,
        key="x0_slider",
    )
    v0_slider = ics_expander.slider(
        "Initial Velocity (v₀)",
        -5.0,
        5.0,
        st.session_state.system_params.ics.v0,
        key="v0_slider",
    )
    n_lines_slider = ics_expander.slider(
        "Number of lines",
        1,
        24,
        st.session_state.system_params.ics.n_lines,
        key="n_lines_slider",
    )
    st.sidebar.header("Solution Time")
    time_expander = st.sidebar.expander("Edit time")
    start_time_slider = time_expander.slider(
        "Start time",
        0.0,
        100.0,
        st.session_state.system_params.start_time,
        key="start_time_slider",
    )
    end_time_slider = time_expander.slider(
        "End time",
        0.0,
        100.0,
        st.session_state.system_params.end_time,
        key="end_time_slider",
    )
    st.session_state.system_params = DamperSystem(
        m=mass_slider,
        k=spring_slider,
        c=damper_slider,
        start_time=start_time_slider,
        end_time=end_time_slider,
        ics=InitialConditions(x0=x0_slider, v0=v0_slider, n_lines=n_lines_slider),
    )


def init_state():
    if "system_params" not in st.session_state:
        st.session_state.system_params = initial_params
    if "plot_placeholder" not in st.session_state:
        st.session_state.plot_placeholder = st.empty()
    if "message_placeholder" not in st.session_state:
        st.session_state.message_placeholder = st.empty()


def main():
    st.title("Stability Criteria Analysis")
    init_state()
    setup_sidebar()
    wave_tab, phase_tab = st.tabs(["Response Plot", "Phase Plot"])
    phase_fig = generate_phase_plot(st.session_state.system_params)
    with wave_tab:
        wave_fig = generate_time_evolution_plot(st.session_state.system_params)
        st.header("Response/Time Evolution")
        st.pyplot(wave_fig)
    with phase_tab:
        st.header("Phase Plane")
        st.pyplot(phase_fig)


if __name__ == "__main__":
    main()
