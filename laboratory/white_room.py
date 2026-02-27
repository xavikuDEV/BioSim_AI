# laboratory/white_room.py
from ursina import *
from core.registry import REGISTRY
from engine.movement_engine import update_physics
import random

def start_laboratory():
    app = Ursina()
    window.title = "BioSim_AI | THE GENESIS"
    window.color = color.black
    
    # --- ILUMINACIÓN POTENTE ---
    # Luz cenital (como un estadio)
    main_light = DirectionalLight(y=10, rotation=(45, 30, 0))
    # Luz de relleno para que no haya zonas negras puras
    AmbientLight(color=color.rgba(150, 150, 150, 255))

    # Suelo con textura de rejilla blanca para contraste
    ground = Entity(model='plane', scale=200, texture='white_cube', 
                    texture_scale=(100,100), color=color.dark_gray)
    
    # Posición inicial de cámara
    camera.position = (0, 50, -100)
    camera.look_at(ground)
    EditorCamera()

    # --- SPAWNING ---
    REGISTRY.clear() # Limpiar restos de tests anteriores
    visual_entities = []
    
    print("⏳ Invocando 10,000 entidades...")
    for _ in range(10000):
        pos = [random.uniform(-40, 40), random.uniform(30, 80), random.uniform(-40, 40)]
        eid = REGISTRY.create_entity(pos=pos)
        
        if eid is not None:
            # Color cian vibrante para destacar sobre el gris
            v_ent = Entity(model='sphere', color=color.cyan, scale=0.4, position=pos)
            visual_entities.append((eid, v_ent))

    def update():
        update_physics()
        for eid, v_ent in visual_entities:
            body = REGISTRY.physics[eid]
            v_ent.position = body.pos
            # Suelo sólido
            if body.pos[1] <= 0:
                body.pos[1] = 0
                body.vel = [0, 0, 0]

    app.run()

if __name__ == "__main__":
    start_laboratory()