# engine/biology/mitosis.py
import random
import copy
from core.registry import REGISTRY
from core.logger import get_logger

logger = get_logger("BIOLOGY")

def process_mitosis():
    """Detecta excedente de energía y gestiona la replicación con herencia."""
    new_borns = []
    
    for eid in list(REGISTRY.active_entities):
        bio = REGISTRY.biology[eid]
        # LEYES DE REPLICACIÓN (SSoT Era I):
        # 1. Glucógeno casi al máximo (>98)
        # 2. Proteína intacta (100% salud)
        # 3. Edad de madurez (>800 ticks) - Evita explosión demográfica
        if bio and bio.glycogen > 98.0 and bio.protein >= 100.0 and bio.age > 800:
            new_borns.append(eid)

    # Limitador de nacimientos por frame (estabilidad de CPU)
    for parent_id in new_borns[:5]: 
        parent_bio = REGISTRY.biology[parent_id]
        parent_phys = REGISTRY.physics[parent_id]
        
        # EL COSTE DE LA VIDA: El padre pierde el 60% de sus reservas
        parent_bio.glycogen *= 0.4
        parent_bio.fat *= 0.4
        
        # Posición del hijo (leve desplazamiento para evitar solapamiento perfecto)
        child_pos = [parent_phys.pos[i] + random.uniform(-0.5, 0.5) for i in range(3)]
        child_id = REGISTRY.create_entity(pos=child_pos)
        
        if child_id is not None:
            # --- HERENCIA GENÉTICA ---
            parent_dna = parent_bio.genome
            child_dna = copy.copy(parent_dna)
            
            # Mutación epigenética sutil (±1%)
            mutation_factor = random.uniform(0.99, 1.01)
            child_dna.mass *= mutation_factor
            child_dna.size = 0.3 + (child_dna.mass * 0.4)
            
            # Inyección de materia y alma
            child_bio = REGISTRY.biology[child_id]
            child_bio.genome = child_dna
            child_bio.generation = parent_bio.generation + 1
            
            # Sincronización física
            REGISTRY.physics[child_id].mass = child_dna.mass
            REGISTRY.physics[child_id].radius = child_dna.size / 2
            
            logger.info(f"🐣 GEN {child_bio.generation} NACIDA: ID {child_id} (Hijo de {parent_id})")