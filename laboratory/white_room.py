# laboratory/white_room.py
import sys
from pathlib import Path
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Inyección de rutas SSoT
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path: sys.path.insert(0, str(root_path))

from core.registry import REGISTRY
from engine.movement_engine import update_physics
from engine.biology.metabolism import update_metabolism
from core.database import init_db
from laboratory.interface import LabUI
from laboratory.controls import handle_god_keys

class LabState:
    def __init__(self):
        self.paused = False
        self.speed = 1.0
        self.current_count = 50

# --- SETUP ---
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

# CÁMARA PRO: FirstPersonController modificado para modo "Vuelo de Dios"
player = FirstPersonController(y=30, z=-100, gravity=0)
player.cursor.visible = False # Oculta el puntero para inmersión

visual_entities = []

def spawn_matter(count):
    state.current_count = count
    for _, v in visual_entities: destroy(v)
    visual_entities.clear()
    REGISTRY.clear()
    
    print(f"🧬 Inyectando {count} entidades...")
    for _ in range(count):
        pos = [random.uniform(-20, 20), random.uniform(20, 60), random.uniform(-20, 20)]
        eid = REGISTRY.create_entity(pos=pos)
        if eid is not None:
            # Obtenemos el tamaño real definido por su ADN
            dna = REGISTRY.biology[eid].genome
            v_ent = Entity(
                model='sphere', 
                color=color.yellow, 
                scale=dna.size, # <--- ¡Morfología Dinámica!
                position=pos
            )
            visual_entities.append((eid, v_ent))

spawn_matter(state.current_count)

def input(key):
    # Delegamos el control al módulo especializado
    handle_god_keys(key, state, ui, spawn_matter)

def update():
    if not state.paused:
        update_physics()
        update_metabolism()
        
        to_destroy = []
        for i, (eid, v_ent) in enumerate(visual_entities):
            body = REGISTRY.physics[eid]
            bio = REGISTRY.biology[eid]
            
            if body and bio:
                v_ent.position = body.pos
                energy_pct = clamp(bio.energy / bio.max_energy, 0, 1)
                v_ent.color = lerp(color.red, color.yellow, energy_pct)
            else:
                destroy(v_ent)
                to_destroy.append(i)
        
        for i in reversed(to_destroy): visual_entities.pop(i)

    # Movimiento vertical manual para el FirstPersonController (E arriba, Q abajo)
    if held_keys['e']: player.y += 0.5
    if held_keys['q']: player.y -= 0.5

if __name__ == "__main__":
    app.run()