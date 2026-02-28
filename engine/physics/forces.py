# engine/physics/forces.py
from engine.physics_vault.gravity import apply_gravity

def apply_universal_forces(body, world_size):
    """Aplica fricción, gravedad y rebote en muros."""
    AIR_RESISTANCE = 0.98
    WALL_BOUNCE = 0.6

    # 1. FRICCIÓN (Damping horizontal)
    body.vel[0] *= AIR_RESISTANCE
    body.vel[2] *= AIR_RESISTANCE

    # 2. GRAVEDAD (Inyección desde el vault)
    body.vel = apply_gravity(body.vel)

    # 3. LÍMITES DEL MUNDO (Muros Invisibles)
    for i in [0, 2]: # Ejes X y Z
        if abs(body.pos[i]) > world_size:
            # Reposicionamiento exacto en el borde
            body.pos[i] = world_size if body.pos[i] > 0 else -world_size
            # Inversión de velocidad con pérdida
            body.vel[i] *= -WALL_BOUNCE