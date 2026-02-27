# laboratory/white_room.py
from ursina import *
from core.registry import REGISTRY
from engine.movement_engine import update_physics
import random

def start_laboratory():
    app = Ursina()
    window.title = "BioSim_AI | THE GENESIS"
    window.color = color.black
    
    # Suelo
    Entity(model='plane', scale=100, texture='white_cube', texture_scale=(100,100), color=color.dark_gray)
    EditorCamera()

    # --- SPAWNING DE 10,000 ENTIDADES ---
    print("⏳ Generando 10,000 entidades...")
    visual_entities = []
    
    for _ in range(10000):
        # 1. Crear en el Registry (Materia)
        pos = [random.uniform(-40, 40), random.uniform(20, 100), random.uniform(-40, 40)]
        eid = REGISTRY.create_entity(pos=pos)
        
        # 2. Crear en Ursina (Espectador)
        v_ent = Entity(model='sphere', color=color.cyan, scale=0.5, position=pos)
        visual_entities.append((eid, v_ent))

    # --- BUCLE DE SIMULACIÓN ---
    def update():
        # 1. Actualizar Física Soberana (Pura matemática)
        update_physics()
        
        # 2. Sincronizar Espectador (Visualización)
        for eid, v_ent in visual_entities:
            body = REGISTRY.physics[eid]
            v_ent.position = body.pos
            
            # Si tocan el suelo (y=0), los detenemos (Colisión básica)
            if body.pos[1] <= 0:
                body.pos[1] = 0
                body.vel = [0, 0, 0]

    app.run()

if __name__ == "__main__":
    start_laboratory()