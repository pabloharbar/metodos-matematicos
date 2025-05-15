import matplotlib.pyplot as plt
import numpy as np
from damper.input import DamperSystem
from damper.solver import solve_for_y
from scipy.integrate import odeint


def generate_time_evolution_plot(damper_system_cfg: DamperSystem):
    time_solution, y_vals = solve_for_y(damper_system_cfg)
    fig_time, ax_time = plt.subplots()
    ax_time.plot(time_solution, y_vals, label="Displacement (x)", linewidth=2)
    ax_time.set_title("Mass-Spring-Damper System Response")
    ax_time.set_xlabel("Time (s)")
    ax_time.set_ylabel("Displacement (m)")
    ax_time.set_xlim(time_solution.min(), time_solution.max())
    ax_time.set_ylim(y_vals.min(), y_vals.max())
    ax_time.grid(True)
    ax_time.legend()

    return fig_time


def generate_phase_plot(damper_system_cfg: DamperSystem):
    y1_vals = np.linspace(-5, 5, 25)
    y2_vals = np.linspace(-5, 5, 25)
    Y1, Y2 = np.meshgrid(y1_vals, y2_vals)

    def derivatives(y, t, m_val, c_val, k_val):
        y1, y2 = y
        dy1dt = y2
        dy2dt = -c_val / m_val * y2 - k_val / m_val * y1
        return [dy1dt, dy2dt]

    # Evaluate vector field
    DY1, DY2 = np.zeros(Y1.shape), np.zeros(Y2.shape)
    for i in range(Y1.shape[0]):
        for j in range(Y1.shape[1]):
            dy = derivatives(
                [Y1[i, j], Y2[i, j]],
                0,
                damper_system_cfg.m,
                damper_system_cfg.c,
                damper_system_cfg.k,
            )
            DY1[i, j], DY2[i, j] = dy

    # Normalize for quiver
    M = np.hypot(DY1, DY2)
    M[M == 0] = 1.0
    DY1 /= M
    DY2 /= M

    fig_phase, ax_phase = plt.subplots()
    ax_phase.quiver(Y1, Y2, DY1, DY2, color="teal", alpha=0.6)
    ax_phase.set_xlabel("$y$ (position)")
    ax_phase.set_ylabel("$\dot{y}$ (velocity)")
    ax_phase.set_xlim(-3, 3)
    ax_phase.set_ylim(-3, 3)
    ax_phase.set_title("Phase Plane")

    # Time values for integration
    t_phase = np.linspace(0, 50, 200)

    # Initial conditions to plot parametric solutions
    initial_conditions = [
        [damper_system_cfg.ics.x0 * (1.0), damper_system_cfg.ics.v0 * (1.0)],
        [damper_system_cfg.ics.x0 * (-1.0), damper_system_cfg.ics.v0 * (-1.0)],
        [damper_system_cfg.ics.x0 * (1.0), damper_system_cfg.ics.v0 * (-1.0)],
        [damper_system_cfg.ics.x0 * (-1.0), damper_system_cfg.ics.v0 * (1.0)],
        [damper_system_cfg.ics.x0 * (0.5), damper_system_cfg.ics.v0 * (0.5)],
        [damper_system_cfg.ics.x0 * (-0.5), damper_system_cfg.ics.v0 * (-0.5)],
        [damper_system_cfg.ics.x0 * (0.5), damper_system_cfg.ics.v0 * (-0.5)],
        [damper_system_cfg.ics.x0 * (-0.5), damper_system_cfg.ics.v0 * (0.5)],
        [damper_system_cfg.ics.x0 * (2.0), damper_system_cfg.ics.v0 * (2.0)],
        [damper_system_cfg.ics.x0 * (-2.0), damper_system_cfg.ics.v0 * (-2.0)],
        [damper_system_cfg.ics.x0 * (2.0), damper_system_cfg.ics.v0 * (-2.0)],
        [damper_system_cfg.ics.x0 * (-2.0), damper_system_cfg.ics.v0 * (2.0)],
        [damper_system_cfg.ics.x0 * (0), damper_system_cfg.ics.v0 * (1.0)],
        [damper_system_cfg.ics.x0 * (0), damper_system_cfg.ics.v0 * (-1.0)],
        [damper_system_cfg.ics.x0 * (1.0), damper_system_cfg.ics.v0 * (0.0)],
        [damper_system_cfg.ics.x0 * (-1.0), damper_system_cfg.ics.v0 * (0.0)],
        [damper_system_cfg.ics.x0 * (0), damper_system_cfg.ics.v0 * (2.0)],
        [damper_system_cfg.ics.x0 * (0), damper_system_cfg.ics.v0 * (-2.0)],
        [damper_system_cfg.ics.x0 * (2.0), damper_system_cfg.ics.v0 * (0.0)],
        [damper_system_cfg.ics.x0 * (-2.0), damper_system_cfg.ics.v0 * (0.0)],
        [damper_system_cfg.ics.x0 * (0), damper_system_cfg.ics.v0 * (0.5)],
        [damper_system_cfg.ics.x0 * (0), damper_system_cfg.ics.v0 * (-0.5)],
        [damper_system_cfg.ics.x0 * (0.5), damper_system_cfg.ics.v0 * (0.0)],
        [damper_system_cfg.ics.x0 * (-0.5), damper_system_cfg.ics.v0 * (0.0)],
    ]

    # Solve and plot trajectories
    for y0 in initial_conditions[: damper_system_cfg.ics.n_lines]:
        sol = odeint(
            derivatives,
            y0,
            t_phase,
            args=(damper_system_cfg.m, damper_system_cfg.c, damper_system_cfg.k),
        )
        arrow_index = 1
        x_arrow = sol[:, 0][arrow_index]
        y_arrow = sol[:, 1][arrow_index]

        dx = sol[:, 0][arrow_index + 1] - sol[:, 0][arrow_index]
        dy = sol[:, 1][arrow_index + 1] - sol[:, 1][arrow_index]

        ax_phase.annotate(
            "",
            xy=(x_arrow + dx, y_arrow + dy),
            xytext=(x_arrow, y_arrow),
            arrowprops=dict(arrowstyle="->", color="red", lw=1.5),
        )
        ax_phase.plot(sol[:, 0], sol[:, 1], lw=1.5)

    ax_phase.grid(True)
    ax_phase.axis("equal")
    return fig_phase
