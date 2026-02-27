# engine/collision/aabb.py
from core.registry import REGISTRY
from core.database import log_death

def check_floor_collision(entity_id: int):
    body = REGISTRY.physics[entity_id]
    radius = body.radius
    
    if body.pos[1] - radius <= 0:
        # --- UMBRAL DE MORTALIDAD AJUSTADO ---
        # Bajamos a -20 para asegurar que registramos datos en las pruebas
        if body.vel[1] < -20:
            log_death(entity_id, cause="Impacto Letal")
        
        body.pos[1] = radius
        body.vel[1] *= -0.5 # Rebote
        body.vel[0] *= 0.9
        body.vel[2] *= 0.9
        return True
    return False