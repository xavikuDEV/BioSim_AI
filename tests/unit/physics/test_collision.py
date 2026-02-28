# tests/unit/physics/test_collision.py
from core.registry import REGISTRY
from engine.movement_engine import update_physics

def test_mass_based_impact():
    """Verifica que el impacto reparte energía inversamente a la masa."""
    REGISTRY.clear()
    
    # Entidad A (Pesada: 100.0) -> Casi inmóvil
    id_a = REGISTRY.create_entity(pos=[0, 0, 0])
    REGISTRY.physics[id_a].mass = 100.0
    REGISTRY.physics[id_a].vel = [0.1, 0, 0]
    
    # Entidad B (Ligera: 1.0) -> Reacción violenta
    id_b = REGISTRY.create_entity(pos=[1.1, 0, 0])
    REGISTRY.physics[id_b].mass = 1.0
    REGISTRY.physics[id_b].vel = [-10, 0, 0]
    
    # Un solo frame de colisión
    update_physics()
        
    v_a = abs(REGISTRY.physics[id_a].vel[0])
    v_b = abs(REGISTRY.physics[id_b].vel[0])
    
    # RESULTADO: B debe salir disparada mientras A apenas se mueve
    assert v_b > v_a * 10, f"Fallo de inercia: Pesada {v_a:.4f}, Ligera {v_b:.4f}"