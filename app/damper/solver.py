import numpy as np
from damper.input import DamperSystem
from sympy import Derivative, Eq, Function, Symbol, dsolve, lambdify
from sympy.abc import x


def solve_for_y(damper_system_cfg: DamperSystem):
    y = Function("y")
    dy = Derivative(y(x), x)
    dy2 = Derivative(y(x), x, x)

    m = Symbol("m")
    c = Symbol("c")
    k = Symbol("k")

    eq = Eq(m * dy2 + c * dy + k * y(x), 0)
    ics = {
        y(0): damper_system_cfg.ics.x0,
        Derivative(y(x), x).subs(x, 0): damper_system_cfg.ics.v0,
    }
    particular_solution = dsolve(eq, y(x), ics=ics)
    current_solution = particular_solution.subs(
        {m: damper_system_cfg.m, c: damper_system_cfg.c, k: damper_system_cfg.k}
    )
    time_solution = np.linspace(
        damper_system_cfg.start_time, damper_system_cfg.end_time, 1000
    )
    y_func = lambdify(x, current_solution.rhs, modules=["numpy"])
    y_vals = y_func(time_solution)

    return time_solution, y_vals
