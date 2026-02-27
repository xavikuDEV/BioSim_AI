# engine/movement_engine.py
from core.registry import REGISTRY
from engine.physics_vault.gravity import apply_gravity
from engine.integration.euler import integrate_position

def update_physics():
    """Procesa el movimiento de todas las entidades activas."""
    for entity_id in REGISTRY.active_entities:
        body = REGISTRY.physics[entity_id]
        
        # 1. Aplicar Leyes (Gravedad)
        body.vel = apply_gravity(body.vel)
        
        # 2. Integrar Movimiento
        body.pos = integrate_position(body.pos, body.vel)