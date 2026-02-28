# engine/biology/metabolism.py
from core.registry import REGISTRY
from core.database import log_death

def update_metabolism():
    """Ejecuta la termodinámica biológica en cascada (Glucógeno -> Grasa -> Proteína)."""
    to_kill = []
    
    for eid in list(REGISTRY.active_entities):
        bio = REGISTRY.biology[eid]
        phys = REGISTRY.physics[eid]
        dna = bio.genome
        
        if not bio or not phys or not dna: continue

        # 1. CÁLCULO DE GASTO (Fórmula SSoT: E = Base + v^2 * m)
        base_cost = 0.05 * dna.mass * dna.metabolic_efficiency
        speed_sq = sum(v**2 for v in phys.vel)
        kinetic_cost = speed_sq * dna.mass * 0.01 # La masa penaliza el movimiento
        
        total_drain = (base_cost + kinetic_cost) / dna.longevity
        
        # 2. CASCADA DE TANQUES
        if bio.glycogen > 0:
            bio.glycogen -= total_drain
        elif bio.fat > 0:
            bio.fat -= total_drain * 0.5 # La grasa rinde el doble pero no da 'explosividad'
        else:
            bio.protein -= total_drain * 2.0 # Consumir músculo es ineficiente y letal
            
        bio.age += 1
        
        # 3. UMBRAL DE MUERTE
        if bio.protein <= 0:
            bio.is_alive = False
            to_kill.append(eid)
            
    for eid in to_kill:
        log_death(eid, cause="Inanición (Falla Estructural)")
        REGISTRY.remove_entity(eid)