# tests/unit/test_metabolism.py
import sys
from pathlib import Path

# --- CONFIGURACIÓN DE RUTA ---
root = Path(__file__).resolve().parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from core.registry import REGISTRY
from core.logger import get_logger
from engine.biology.metabolism import update_metabolism

logger = get_logger("TEST_METABOLISM")

def test_basal_metabolism():
    """Ley 1: El Glucógeno debe bajar por el simple hecho de existir (Gasto Basal)."""
    try:
        REGISTRY.clear()
        eid = REGISTRY.create_entity(pos=[0, 0, 0])
        bio = REGISTRY.biology[eid]
        
        initial_glycogen = bio.glycogen
        update_metabolism()
        
        assert bio.glycogen < initial_glycogen, "El gasto basal no está drenando Glucógeno"
        logger.info(f"✅ Basal OK: {initial_glycogen:.2f} -> {bio.glycogen:.2f}")
    except AssertionError as e:
        logger.error(f"❌ Fallo Basal: {e}")
        raise e

def test_kinetic_metabolism():
    """Ley 2: Correr debe drenar energía cuadráticamente (v^2 * m)."""
    try:
        REGISTRY.clear()
        id_still = REGISTRY.create_entity(pos=[0, 0, 0])
        id_fast = REGISTRY.create_entity(pos=[5, 0, 0])
        
        # Forzamos misma masa para comparar solo velocidad
        REGISTRY.physics[id_still].mass = 1.0
        REGISTRY.physics[id_fast].mass = 1.0
        REGISTRY.physics[id_fast].vel = [20.0, 0, 0] # Alta velocidad
        
        update_metabolism()
        
        drain_still = 100.0 - REGISTRY.biology[id_still].glycogen
        drain_fast = 100.0 - REGISTRY.biology[id_fast].glycogen
        
        assert drain_fast > drain_still, f"Fallo Cinético: Fast ({drain_fast:.4f}) no gasta más que Still ({drain_still:.4f})"
        logger.info(f"✅ Cinético OK: Drain Still {drain_still:.4f} < Drain Fast {drain_fast:.4f}")
    except AssertionError as e:
        logger.error(f"❌ Fallo Cinético: {e}")
        raise e

def test_metabolic_cascade():
    """Ley 3: Si el Glucógeno se agota, debe empezar a quemar Grasa."""
    try:
        REGISTRY.clear()
        eid = REGISTRY.create_entity(pos=[0, 0, 0])
        bio = REGISTRY.biology[eid]
        
        bio.glycogen = 0.0 # Agotamos tanque 1
        initial_fat = bio.fat
        
        update_metabolism()
        
        assert bio.fat < initial_fat, "La cascada falló: No se está consumiendo Grasa tras agotar Glucógeno"
        assert bio.protein == 100.0, "Error de jerarquía: Se consumió Proteína antes de agotar la Grasa"
        logger.info(f"✅ Cascada (Grasa) OK: Grasa consumida {initial_fat:.2f} -> {bio.fat:.2f}")
    except AssertionError as e:
        logger.error(f"❌ Fallo Cascada: {e}")
        raise e

def test_starvation_death_protein():
    """Ley 4: Si la Proteína (tanque 3) llega a 0, la entidad debe morir (Falla Estructural)."""
    try:
        REGISTRY.clear()
        eid = REGISTRY.create_entity(pos=[0, 0, 0])
        bio = REGISTRY.biology[eid]
        
        # Vaciamos tanques de reserva
        bio.glycogen = 0.0
        bio.fat = 0.0
        bio.protein = 0.01 # Al borde del colapso
        
        update_metabolism()
        
        assert eid not in REGISTRY.active_entities, "La entidad debería haber sido purgada del Registro tras morir"
        logger.info(f"✅ Muerte por Inanición OK: ID {eid} eliminado tras colapso proteico")
    except AssertionError as e:
        logger.error(f"❌ Fallo Muerte: {e}")
        raise e

def test_genetic_mass_penalty():
    """Ley 5: Una masa mayor debe penalizar el gasto energético total (Basal + Cinético)."""
    try:
        REGISTRY.clear()
        id_light = REGISTRY.create_entity(pos=[0, 0, 0])
        id_heavy = REGISTRY.create_entity(pos=[2, 0, 0])
        
        # Inyectamos genes de masa distintos
        REGISTRY.biology[id_light].genome.mass = 0.5
        REGISTRY.biology[id_heavy].genome.mass = 2.5
        
        update_metabolism()
        
        drain_light = 100.0 - REGISTRY.biology[id_light].glycogen
        drain_heavy = 100.0 - REGISTRY.biology[id_heavy].glycogen
        
        assert drain_heavy > drain_light, "La masa no está penalizando el gasto basal"
        logger.info(f"✅ Penalización de Masa OK: Light ({drain_light:.4f}) < Heavy ({drain_heavy:.4f})")
    except AssertionError as e:
        logger.error(f"❌ Fallo Masa: {e}")
        raise e