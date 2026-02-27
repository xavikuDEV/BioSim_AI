# engine/physics_vault/gravity.py
from core.constants import WORLD

def apply_gravity(velocity: list[float]) -> list[float]:
    """
    Aplica la aceleración constante de la gravedad al vector de velocidad.
    v = v0 + g * dt
    """
    dt = WORLD.TIME_STEP
    g = WORLD.GRAVITY
    
    # Solo afectamos el eje Y (caída libre)
    velocity[1] -= g * dt
    return velocity