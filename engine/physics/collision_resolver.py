# engine/physics/collision_resolver.py
import math

def resolve_collision(eid, body, other):
    """Resuelve el impacto respetando la inercia (Newton)."""
    RESTITUTION = 0.8
    
    dx = body.pos[0] - other.pos[0]
    dy = body.pos[1] - other.pos[1]
    dz = body.pos[2] - other.pos[2]
    dist_sq = dx*dx + dy*dy + dz*dz
    min_dist = body.radius + other.radius

    if 0 < dist_sq < min_dist * min_dist:
        dist = math.sqrt(dist_sq)
        nx, ny, nz = dx/dist, dy/dist, dz/dist
        
        # Velocidad relativa
        rvx = body.vel[0] - other.vel[0]
        rvy = body.vel[1] - other.vel[1]
        rvz = body.vel[2] - other.vel[2]
        
        vel_along_normal = rvx*nx + rvy*ny + rvz*nz
        
        # SÓLO resolvemos si se están acercando
        if vel_along_normal < 0:
            # --- MASA SOBERANA ---
            m_a = body.mass
            m_b = other.mass
            
            # Calculamos masas inversas
            inv_m_a = 1.0 / m_a if m_a > 0 else 0
            inv_m_b = 1.0 / m_b if m_b > 0 else 0
            
            # Impulso escalar (j)
            j = -(1 + RESTITUTION) * vel_along_normal
            j /= (inv_m_a + inv_m_b)

            # Aplicar impulso según la inercia (malla de Newton)
            body.vel[0] += (j * inv_m_a) * nx
            body.vel[1] += (j * inv_m_a) * ny
            body.vel[2] += (j * inv_m_a) * nz
            
            other.vel[0] -= (j * inv_m_b) * nx
            other.vel[1] -= (j * inv_m_b) * ny
            other.vel[2] -= (j * inv_m_b) * nz

            # --- ANTIFUSIÓN POSICIONAL ---
            percent, slop = 0.2, 0.01
            penetration = min_dist - dist
            if penetration > slop:
                correction = (penetration / (inv_m_a + inv_m_b)) * percent
                body.pos[0] += nx * correction * inv_m_a
                body.pos[1] += ny * correction * inv_m_a
                body.pos[2] += nz * correction * inv_m_a
                
                other.pos[0] -= nx * correction * inv_m_b
                other.pos[1] -= ny * correction * inv_m_b
                other.pos[2] -= nz * correction * inv_m_b