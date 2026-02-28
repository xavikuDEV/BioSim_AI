# engine/movement_engine.py
from core.registry import REGISTRY
from engine.integration.euler import integrate_position
from engine.collision.aabb import check_floor_collision
from engine.collision.quadtree import Quadtree
from engine.physics.forces import apply_universal_forces
from engine.physics.collision_resolver import resolve_collision

def update_physics():
    WORLD_SIZE = 80
    entities = list(REGISTRY.active_entities)
    
    # 1. Optimización Espacial
    qt = Quadtree([-WORLD_SIZE, -WORLD_SIZE, WORLD_SIZE*2, WORLD_SIZE*2], 4)
    for eid in entities:
        if REGISTRY.physics[eid]:
            qt.insert(eid, REGISTRY.physics[eid].pos)

    # --- REGISTRO DE COLISIONES PROCESADAS ---
    processed_pairs = set()

    for eid in entities:
        body = REGISTRY.physics[eid]
        if not body: continue
        
        # 2. Aplicar Fuerzas Universales (Fricción, Gravedad, Muros)
        apply_universal_forces(body, WORLD_SIZE)
        
        # 3. Integración y Suelo
        body.pos = integrate_position(body.pos, body.vel)
        check_floor_collision(eid)
        
        # 4. Resolución de Colisiones (Agente vs Agente)
        nearby = []
        qt.query(body.pos, body.radius * 2, nearby)
        for other_id in nearby:
            if eid == other_id: continue
            
            # EL SECRETO: Evitar procesar el mismo par dos veces
            pair = tuple(sorted((eid, other_id)))
            if pair in processed_pairs: continue
            
            other = REGISTRY.physics[other_id]
            if other:
                resolve_collision(eid, body, other)
                processed_pairs.add(pair)