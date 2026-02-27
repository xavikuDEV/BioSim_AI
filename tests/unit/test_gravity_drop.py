# tests/test_gravity_drop.py
from core.registry import REGISTRY
from engine.movement_engine import update_physics
from core.constants import WORLD

def test_drop():
    # Crear entidad a 10m de altura
    eid = REGISTRY.create_entity(pos=[0, 10, 0])
    body = REGISTRY.physics[eid]
    
    print(f"Inicio: Pos {body.pos}")
    
    # Simular 10 ticks (0.16s aprox)
    for _ in range(10):
        update_physics()
    
    print(f"Final (10 ticks): Pos {body.pos}")
    
    if body.pos[1] < 10:
        print("✅ ÉXITO: La gravedad es soberana. La entidad está cayendo.")
    else:
        print("❌ ERROR: La entidad levita.")

if __name__ == "__main__":
    test_drop()