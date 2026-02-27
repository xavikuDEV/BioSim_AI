# tests/unit/test_gravity_drop.py
from core.registry import REGISTRY
from engine.movement_engine import update_physics

def test_drop():
    # Limpieza obligatoria antes de testear
    REGISTRY.clear()
    
    eid = REGISTRY.create_entity(pos=[0, 10, 0])
    
    # Verificación de seguridad
    assert eid is not None, "Error: El registro está lleno"
    
    body = REGISTRY.physics[eid]
    initial_y = body.pos[1]
    
    # Simular caída
    for _ in range(5):
        update_physics()
        
    assert body.pos[1] < initial_y, f"La gravedad falló: {body.pos[1]} >= {initial_y}"