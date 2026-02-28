# laboratory/white_room.py
import sys
from pathlib import Path

# --- INYECCIÓN DE RUTA SSoT (DEBE SER LO PRIMERO) ---
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Imports del Motor BioSim_AI
from core.registry import REGISTRY
from core.database import init_db, log_snapshot
from core.logger import get_logger
from engine.movement_engine import update_physics
from engine.biology.metabolism import update_metabolism
from engine.biology.mitosis import process_mitosis
from laboratory.interface import LabUI
from laboratory.controls import handle_god_keys

logger = get_logger("LABORATORY")

class LabState:
    def __init__(self):
        self.paused = False
        self.speed = 1.0
        self.current_count = 50
        self.tick_counter = 0

# --- INICIALIZACIÓN ---
init_db()
app = Ursina()
state = LabState()
ui = LabUI()

# Visuales de entorno
window.color = color.black
scene.fog_density = 0.01
sun = DirectionalLight(y=50, rotation=(45, 30, 0))
ground = Entity(model='plane', scale=2000, texture='white_cube', 
                texture_scale=(1000, 1000), color=color.rgba(255, 255, 255, 20))

# Cámara de Dios (FPS Mode)
player = FirstPersonController(y=30, z=-100, gravity=0)
player.cursor.visible = False

visual_entities = []

def spawn_matter(count):
    state.current_count = count
    for _, v in visual_entities: destroy(v)
    visual_entities.clear()
    REGISTRY.clear()
    
    logger.info(f"🧬 Inyectando {count} entidades en la Sala Blanca...")
    for _ in range(count):
        pos = [random.uniform(-20, 20), random.uniform(20, 60), random.uniform(-20, 20)]
        eid = REGISTRY.create_entity(pos=pos)
        if eid is not None:
            dna = REGISTRY.biology[eid].genome
            v_ent = Entity(model='sphere', color=color.yellow, scale=dna.size, position=pos)
            visual_entities.append((eid, v_ent))

spawn_matter(state.current_count)

def input(key):
    handle_god_keys(key, state, ui, player, spawn_matter)

def update():
    if not state.paused:
        try:
            # 1. Motores del Universo
            update_physics()
            update_metabolism()
            process_mitosis()
            
            # 2. Telemetría (Cada 60 frames / 1 segundo aprox)
            state.tick_counter += 1
            if state.tick_counter % 60 == 0:
                log_snapshot(state.tick_counter, REGISTRY)

            # 3. Sincronización Visual
            to_destroy = []
            for i, (eid, v_ent) in enumerate(visual_entities):
                body = REGISTRY.physics[eid]
                bio = REGISTRY.biology[eid]
                
                if body and bio:
                    v_ent.position = body.pos
                    # Color basado en Glucógeno (Tanque 1)
                    energy_pct = clamp(bio.glycogen / 100.0, 0, 1)
                    v_ent.color = lerp(color.red, color.yellow, energy_pct)
                    
                    # Si drena Proteína (Salud), se vuelve negro
                    if bio.protein < 100:
                        health_pct = clamp(bio.protein / 100.0, 0, 1)
                        v_ent.color = lerp(color.black, color.red, health_pct)
                else:
                    destroy(v_ent)
                    to_destroy.append(i)
            
            for i in reversed(to_destroy): visual_entities.pop(i)
        except Exception as e:
            logger.error(f"Fallo crítico en el loop de simulación: {e}")

    # Movimiento vertical FPS (E/Q)
    if held_keys['e']: player.y += 0.5
    if held_keys['q']: player.y -= 0.5

if __name__ == "__main__":
    app.run()