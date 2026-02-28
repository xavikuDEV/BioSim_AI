from core.registry import REGISTRY
from engine.movement_engine import update_physics
import pytest

def test_physics_precision():
    """Valida la Gravedad y la Precisión del Rebote (Restitución)."""
    REGISTRY.clear()
    # Soltamos desde 10m
    eid = REGISTRY.create_entity(pos=[0, 10, 0])
    body = REGISTRY.physics[eid]
    
    # --- FASE 1: CAÍDA ---
    # Simulamos suficientes ticks para que choque (aprox 1.5s a 60fps = 90 ticks)
    max_impact_vel = 0
    for _ in range(100):
        update_physics()
        if body.vel[1] < max_impact_vel:
            max_impact_vel = body.vel[1]
        
        # Si la velocidad cambia de signo, es que ha rebotado
        if body.vel[1] > 0:
            break
            
    assert max_impact_vel < -10, "La entidad no ganó suficiente velocidad de caída"
    
    # --- FASE 2: REBOTE ---
    # Verificamos la Ley de Restitución: v_final = -v_inicial * 0.5
    # Esperamos que la velocidad post-choque sea aprox la mitad de la de impacto
    expected_rebound = abs(max_impact_vel) * 0.5
    
    # Usamos pytest.approx para tolerar errores de redondeo de coma flotante
    assert body.vel[1] == pytest.approx(expected_rebound, rel=0.1), \
        f"Rebote incorrecto. Esperado: {expected_rebound}, Obtenido: {body.vel[1]}"

    print(f"\n✅ FÍSICA VALIDADA: Impacto {max_impact_vel:.2f} -> Rebote {body.vel[1]:.2f}")