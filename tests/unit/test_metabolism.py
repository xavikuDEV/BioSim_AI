# tests/unit/test_metabolism.py
import sys
from pathlib import Path

# Añadimos la raíz para las importaciones
root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root))

from core.registry import REGISTRY
from engine.biology.metabolism import update_metabolism

def test_basal_metabolism():
    """Ley 1: Una entidad quieta debe perder energía lentamente."""
    REGISTRY.clear()
    id_still = REGISTRY.create_entity(pos=[0, 0, 0])
    
    # Simulamos 1 frame metabólico
    update_metabolism()
    
    energy = REGISTRY.biology[id_still].energy
    assert energy < 100.0, "El metabolismo basal no está consumiendo energía"

def test_kinetic_metabolism():
    """Ley 2: Una entidad en movimiento debe consumir MÁS energía que una quieta."""
    REGISTRY.clear()
    id_still = REGISTRY.create_entity(pos=[0, 0, 0])
    id_fast = REGISTRY.create_entity(pos=[5, 0, 0])
    
    # Le damos una velocidad extrema a la segunda entidad
    REGISTRY.physics[id_fast].vel = [50.0, 0, 0] 
    
    update_metabolism()
    
    energy_still = REGISTRY.biology[id_still].energy
    energy_fast = REGISTRY.biology[id_fast].energy
    
    assert energy_fast < energy_still, f"Fallo cinético: Quieta ({energy_still}) vs Rápida ({energy_fast})"

def test_starvation_death():
    """Ley 3: Si la energía llega a 0, la entidad debe morir y ser purgada."""
    REGISTRY.clear()
    id_dying = REGISTRY.create_entity(pos=[0, 0, 0])
    
    # La ponemos al borde de la muerte (menos del coste basal de 1 frame)
    REGISTRY.biology[id_dying].energy = 0.01 
    
    # Este frame consumirá sus últimos recursos
    update_metabolism() 
    
    assert id_dying not in REGISTRY.active_entities, "La entidad fantasma sigue en el registro tras morir"