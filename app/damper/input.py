from dataclasses import dataclass


@dataclass
class InitialConditions:
    x0: float
    v0: float
    n_lines: int


@dataclass
class DamperSystem:
    m: float
    k: float
    c: float
    ics: InitialConditions
    start_time: float
    end_time: float
