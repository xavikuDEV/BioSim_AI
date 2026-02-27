# engine/movement_engine.py
import math
from core.registry import REGISTRY
from engine.physics_vault.gravity import apply_gravity
from engine.integration.euler import integrate_position
from engine.collision.aabb import check_floor_collision
from engine.collision.quadtree import Quadtree

def update_physics():
    entities = REGISTRY.active_entities
    
    # 1. Reconstruir Quadtree con posiciones actuales
    qt = Quadtree([0, 0, 100, 100], 4)
    for eid in entities:
        qt.insert(eid, REGISTRY.physics[eid].pos)

    for eid in entities:
        body = REGISTRY.physics[eid]
        
        # Física básica y suelo
        body.vel = apply_gravity(body.vel)
        body.pos = integrate_position(body.pos, body.vel)
        check_floor_collision(eid)
        
        # 2. Detección y Resolución de Colisiones
        nearby = []
        qt.query(body.pos, body.radius * 2, nearby)
        
        for other_id in nearby:
            if eid == other_id: continue
            other = REGISTRY.physics[other_id]
            
            # Vector entre centros
            dx = body.pos[0] - other.pos[0]
            dy = body.pos[1] - other.pos[1]
            dz = body.pos[2] - other.pos[2]
            dist_sq = dx*dx + dy*dy + dz*dz
            min_dist = body.radius + other.radius
            
            if dist_sq < min_dist * min_dist and dist_sq > 0:
                dist = math.sqrt(dist_sq)
                # Normal del impacto (dirección del choque)
                nx, ny, nz = dx/dist, dy/dist, dz/dist
                
                # Velocidad Relativa
                rvx = body.vel[0] - other.vel[0]
                rvy = body.vel[1] - other.vel[1]
                rvz = body.vel[2] - other.vel[2]
                
                # Producto Punto: ¿Se están acercando?
                vel_along_normal = rvx*nx + rvy*ny + rvz*nz
                
                if vel_along_normal < 0:
                    # Coeficiente de restitución (0.8 = rebote elástico)
                    j = -(1 + 0.8) * vel_along_normal
                    j /= 2
                    
                    # --- IMPACTO SIMÉTRICO ---
                    body.vel[0] += j * nx
                    body.vel[1] += j * ny
                    body.vel[2] += j * nz
                    
                    other.vel[0] -= j * nx
                    other.vel[1] -= j * ny
                    other.vel[2] -= j * nz
                    
                    # --- REGISTRO DE EVENTOS EXTREMOS ---
                    if j > 15: 
                        from core.database import log_death
                        # Registramos la colisión en la "caja negra" del universo
                        log_death(eid, cause="Colisión Traumática")

                    # --- ANTIFUSIÓN ---
                    overlap = (min_dist - dist) * 0.5
                    body.pos[0] += nx * overlap
                    body.pos[1] += ny * overlap
                    body.pos[2] += nz * overlap
                    other.pos[0] -= nx * overlap
                    other.pos[1] -= ny * overlap
                    other.pos[2] -= nz * overlap