# tests/test_memory_stress.py
import sys
from core.registry import REGISTRY

def test_10k_entities():
    print(f"--- Iniciando Stress Test: 10,000 Entidades ---")
    for i in range(10000):
        REGISTRY.create_entity(pos=[i, 0, 0])
    
    count = REGISTRY.get_count()
    print(f"✅ Entidades creadas: {count}")
    
    # Cálculo aproximado de memoria
    size = sys.getsizeof(REGISTRY.physics) + sys.getsizeof(REGISTRY.biology)
    print(f"📊 Memoria ocupada por punteros del Registry: {size / 1024:.2f} KB")

if __name__ == "__main__":
    test_10k_entities()