# engine/biology/metabolism.py
from core.registry import REGISTRY
from core.database import log_death

def update_metabolism(dt=0.016):
    to_kill = []
    
    for eid in list(REGISTRY.active_entities):
        bio = REGISTRY.bio[eid]
        phys = REGISTRY.physics[eid]
        
        # 1. Costo de Existencia (Metabolismo Basal)
        cost = bio.metabolic_rate
        
        # 2. Costo por Movimiento (Física real: E = 1/2 * m * v^2)
        # Cuanto más rápido se mueven, más glucógeno queman
        speed_sq = sum(v**2 for v in phys.vel)
        cost += speed_sq * 0.001 
        
        bio.energy -= cost
        bio.age += 1
        
        # 3. Verificación de Muerte
        if bio.energy <= 0:
            bio.is_alive = False
            to_kill.append(eid)
            
    for eid in to_kill:
        log_death(eid, cause="Inanición (Falta de Energía)")
        REGISTRY.remove_entity(eid)