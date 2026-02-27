# tests/unit/test_collision.py
import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root))

from core.registry import REGISTRY
from engine.movement_engine import update_physics

def test_entity_to_entity_collision():
    """Verifica el intercambio simétrico de energía en un choque."""
    REGISTRY.clear()
    
    # Entidad A (Izquierda, va a la derecha)
    id_a = REGISTRY.create_entity(pos=[-2.0, 5, 0])
    REGISTRY.physics[id_a].vel = [10.0, 0, 0]
    
    # Entidad B (Derecha, va a la izquierda)
    id_b = REGISTRY.create_entity(pos=[2.0, 5, 0])
    REGISTRY.physics[id_b].vel = [-10.0, 0, 0]
    
    # Simulamos frames hasta el choque
    for _ in range(15):
        update_physics()
        
    v_a = REGISTRY.physics[id_a].vel[0]
    v_b = REGISTRY.physics[id_b].vel[0]
    
    print(f"\n[FISICA PRO] Vel A Final: {v_a:.2f} | Vel B Final: {v_b:.2f}")
    
    # Tras el choque: A debe ir a la izquierda (<0) y B a la derecha (>0)
    assert v_a < 0, f"A debería haber rebotado hacia la izquierda, tiene {v_a}"
    assert v_b > 0, f"B debería haber rebotado hacia la derecha, tiene {v_b}"