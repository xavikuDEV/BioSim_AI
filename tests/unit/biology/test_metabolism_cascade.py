# tests/unit/test_metabolism_cascade.py
from core.registry import REGISTRY
from engine.biology.metabolism import update_metabolism

def test_glycogen_to_fat_transition():
    """Verifica que el sistema salta a la Grasa cuando no hay Glucógeno."""
    REGISTRY.clear()
    eid = REGISTRY.create_entity(pos=[0,0,0])
    bio = REGISTRY.biology[eid]
    
    # Forzamos vaciado de Glucógeno
    bio.glycogen = 0.0
    initial_fat = bio.fat
    
    # Ejecutamos metabolismo
    update_metabolism()
    
    assert bio.fat < initial_fat, "La Grasa debería estar consumiéndose tras agotar el Glucógeno"
    assert bio.protein == 100.0, "La Proteína no debería tocarse si aún queda Grasa"

def test_protein_decay_death():
    REGISTRY.clear()
    eid = REGISTRY.create_entity(pos=[0,0,0])
    bio = REGISTRY.biology[eid]
    bio.glycogen, bio.fat, bio.protein = 0.0, 0.0, 0.1 # Al borde
    
    # Forzamos varios ticks hasta que la proteína baje de 0
    for _ in range(5):
        update_metabolism()
        
    assert eid not in REGISTRY.active_entities, "La entidad debería haber muerto tras agotar proteína"