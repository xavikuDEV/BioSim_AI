# engine/movement_engine.py
import math
from core.registry import REGISTRY
from engine.physics_vault.gravity import apply_gravity
from engine.integration.euler import integrate_position
from engine.collision.aabb import check_floor_collision
from engine.collision.quadtree import Quadtree

def update_physics():
    # --- CONSTANTES UNIVERSALES ---
    AIR_RESISTANCE = 0.98  # El aire frena un 2% por frame (Damping horizontal)
    WORLD_SIZE = 80        # El mundo es un cubo de 160x160 (-80 a 80)
    WALL_BOUNCE = 0.6      # Factor de restitución contra los muros
    RESTITUTION = 0.8      # Factor de restitución entre entidades (Choque elástico)
    
    entities = list(REGISTRY.active_entities) # Copia segura
    
    # 1. Reconstruir Quadtree con posiciones actuales (Optimización Espacial)
    qt = Quadtree([-WORLD_SIZE, -WORLD_SIZE, WORLD_SIZE*2, WORLD_SIZE*2], 4)
    for eid in entities:
        # Solo insertamos si la entidad tiene física válida
        if REGISTRY.physics[eid]:
            qt.insert(eid, REGISTRY.physics[eid].pos)

    for eid in entities:
        body = REGISTRY.physics[eid]
        if not body: continue
        
        # 2. FRICCIÓN (Damping)
        # Aplicamos resistencia solo en X y Z para no anular la aceleración de gravedad
        body.vel[0] *= AIR_RESISTANCE
        body.vel[2] *= AIR_RESISTANCE
        
        # 3. LÍMITES DEL MUNDO (Contención)
        for i in [0, 2]: # Ejes X y Z
            if abs(body.pos[i]) > WORLD_SIZE:
                # Reposicionamiento exacto en el borde
                body.pos[i] = WORLD_SIZE if body.pos[i] > 0 else -WORLD_SIZE
                # Inversión de velocidad con pérdida (Choque contra la pared)
                body.vel[i] *= -WALL_BOUNCE

        # 4. FÍSICA BÁSICA (Gravedad, Integración y Suelo)
        body.vel = apply_gravity(body.vel)
        body.pos = integrate_position(body.pos, body.vel)
        check_floor_collision(eid)
        
        # 5. DETECCIÓN Y RESOLUCIÓN DE COLISIONES (Agente vs Agente)
        nearby = []
        qt.query(body.pos, body.radius * 2, nearby)
        
        for other_id in nearby:
            if eid == other_id: continue
            
            other = REGISTRY.physics[other_id]
            if not other: continue
            
            # Vector entre centros
            dx = body.pos[0] - other.pos[0]
            dy = body.pos[1] - other.pos[1]
            dz = body.pos[2] - other.pos[2]
            dist_sq = dx*dx + dy*dy + dz*dz
            min_dist = body.radius + other.radius
            
            # Comprobación de solapamiento
            if dist_sq < min_dist * min_dist and dist_sq > 0:
                dist = math.sqrt(dist_sq)
                
                # Normal de la colisión (dirección del impacto)
                nx, ny, nz = dx/dist, dy/dist, dz/dist
                
                # Velocidad Relativa
                rvx = body.vel[0] - other.vel[0]
                rvy = body.vel[1] - other.vel[1]
                rvz = body.vel[2] - other.vel[2]
                
                # Velocidad a lo largo de la normal
                vel_along_normal = rvx*nx + rvy*ny + rvz*nz
                
                # Solo resolver si las entidades se están acercando
                if vel_along_normal < 0:
                    
                    # --- IMPULSO BASADO EN MASA (NEWTON) ---
                    m_a = body.mass
                    m_b = other.mass
                    
                    # Prevenir división por cero si la masa es 0 (aunque no debería pasar)
                    inv_mass_a = 1.0 / m_a if m_a > 0 else 0
                    inv_mass_b = 1.0 / m_b if m_b > 0 else 0
                    
                    # Escalar del Impulso (j)
                    j = -(1 + RESTITUTION) * vel_along_normal
                    j /= (inv_mass_a + inv_mass_b)
                    
                    # Repartimos el impulso proporcional a la masa inversa
                    impulse_x = j * nx
                    impulse_y = j * ny
                    impulse_z = j * nz
                    
                    body.vel[0] += impulse_x * inv_mass_a
                    body.vel[1] += impulse_y * inv_mass_a
                    body.vel[2] += impulse_z * inv_mass_a
                    
                    other.vel[0] -= impulse_x * inv_mass_b
                    other.vel[1] -= impulse_y * inv_mass_b
                    other.vel[2] -= impulse_z * inv_mass_b
                    
                    # --- LOG DE EVENTOS EXTREMOS ---
                    # Consideramos traumático un choque con un impulso muy alto
                    if j > 20: 
                        from core.database import log_death
                        log_death(eid, cause="Colisión Traumática")

                    # --- ANTIFUSIÓN (Positional Correction) ---
                    # Evita que las esferas se queden pegadas si chocan a alta velocidad
                    percent = 0.2 # Normalmente 20% al 80%
                    slop = 0.01   # Permite una pequeña penetración
                    penetration = min_dist - dist
                    
                    if penetration > slop:
                        correction = (penetration / (inv_mass_a + inv_mass_b)) * percent
                        cx, cy, cz = nx * correction, ny * correction, nz * correction
                        
                        body.pos[0] += cx * inv_mass_a
                        body.pos[1] += cy * inv_mass_a
                        body.pos[2] += cz * inv_mass_a
                        
                        other.pos[0] -= cx * inv_mass_b
                        other.pos[1] -= cy * inv_mass_b
                        other.pos[2] -= cz * inv_mass_b