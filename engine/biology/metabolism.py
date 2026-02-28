# engine/biology/metabolism.py
from core.registry import REGISTRY
from core.database import log_death

def update_metabolism(dt=0.016):
    """Calcula el consumo de energía de todas las entidades vivas."""
    to_kill = []
    
    # Usamos list() para evitar errores si la lista cambia durante el bucle
    for eid in list(REGISTRY.active_entities):
        bio = REGISTRY.biology[eid]
        phys = REGISTRY.physics[eid]
        
        if not bio or not phys: continue

        # Costo cinético: v^2 (quemar energía por movimiento)
        speed_sq = sum(v**2 for v in phys.vel)
        total_cost = bio.metabolic_rate + (speed_sq * 0.001)
        
        bio.energy -= total_cost
        bio.age += 1
        
        # Umbral de Muerte por Inanición
        if bio.energy <= 0:
            bio.is_alive = False
            to_kill.append(eid)
            
    # Procesar muertes
    for eid in to_kill:
        log_death(eid, cause="Inanición (Agotamiento de Energía)")
        REGISTRY.remove_entity(eid) 