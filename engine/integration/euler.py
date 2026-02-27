# engine/integration/euler.py
from core.constants import WORLD

def integrate_position(pos: list[float], vel: list[float]) -> list[float]:
    """
    Actualiza la posición basada en la velocidad (Integración de Euler).
    p = p0 + v * dt
    """
    dt = WORLD.TIME_STEP
    for i in range(3):
        pos[i] += vel[i] * dt
    return pos