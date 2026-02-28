# laboratory/white_room.py
import sys
from pathlib import Path
from ursina import *
from engine.biology.metabolism import update_metabolism
import random

# --- SOBERANÍA DE RUTAS (RESTAURADA) ---
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

try:
    from core.registry import REGISTRY
    from engine.movement_engine import update_physics
    from core.database import init_db
except ImportError as e:
    print(f"❌ Error crítico de importación: {e}")
    sys.exit(1)

# --- INICIALIZACIÓN ---
init_db()
app = Ursina()

# --- CONFIGURACIÓN DE VENTANA Y ESTÉTICA ---
window.title = "BioSim_AI | God Mode Laboratory v2.8"
window.color = color.black
window.fps_counter.enabled = True
window.exit_button.visible = True

# Niebla para profundidad visual
scene.fog_density = 0.01
scene.fog_color = color.black

# Iluminación
sun = DirectionalLight(y=50, rotation=(45, 30, 0))
sun.look_at(Vec3(0,0,0))
AmbientLight(color=color.rgba(100, 100, 100, 255))

# Escenario: Suelo de rejilla sutil
ground = Entity(
    model='plane', scale=2000, 
    texture='white_cube', texture_scale=(1000, 1000), 
    color=color.rgba(255, 255, 255, 20) 
)

# Cámara de Dios (Blindada)
cam_control = EditorCamera()
camera.clip_plane_far = 10000 
camera.position = (0, 30, -100)

# --- ESTADO GLOBAL DEL LABORATORIO ---
visual_entities = []
current_count = 50
simulation_speed = 1.0
paused = False

# UI: Texto de Estado en pantalla
status_text = Text(
    text="Velocidad: 1.0x", 
    position=(-0.85, 0.45), 
    color=color.yellow,
    scale=1.5
)

# --- LÓGICA DE GENERACIÓN ---
def spawn_matter(count):
    global current_count
    current_count = count
    
    # Limpieza visual y de registro
    for _, v in visual_entities:
        destroy(v)
    visual_entities.clear()
    REGISTRY.clear()
    
    print(f"🧬 Inyectando {count} entidades...")
    for _ in range(count):
        pos = [random.uniform(-20, 20), random.uniform(20, 60), random.uniform(-20, 20)]
        eid = REGISTRY.create_entity(pos=pos)
        if eid is not None:
            # Amarillo Neón para visibilidad, escala 0.8 para ver colisiones
            v_ent = Entity(model='sphere', color=color.yellow, scale=0.8, position=pos)
            visual_entities.append((eid, v_ent))

# Lanzamiento inicial
spawn_matter(50)

# --- CONTROLES DE DIOS (INPUT) ---
def input(key):
    global simulation_speed, paused
    
    # PAUSA / REANUDAR
    if key == 'p':
        paused = not paused
        time.time_scale = 0 if paused else simulation_speed
        status_text.text = "PAUSADO" if paused else f"Velocidad: {simulation_speed}x"
        status_text.color = color.red if paused else color.yellow
        
    # REPETIR
    if key == 'r':
        spawn_matter(current_count)
        
    # CANTIDADES DE SPAWN
    if key == '1': spawn_matter(1)
    if key == '2': spawn_matter(100)
    if key == '3': spawn_matter(2000) # Límite para evitar lag visual
        
    # AJUSTE DE VELOCIDAD
    if key == '+' or key == 'kp_plus':
        simulation_speed = min(simulation_speed + 0.5, 5.0)
        if not paused: time.time_scale = simulation_speed
        status_text.text = f"Velocidad: {simulation_speed}x"
        
    if key == '-' or key == 'kp_minus':
        simulation_speed = max(simulation_speed - 0.5, 0.1)
        if not paused: time.time_scale = simulation_speed
        status_text.text = f"Velocidad: {simulation_speed}x"
        
    # CENTRAR CÁMARA
    if key == 'c':
        camera.position = (0, 30, -100)
        camera.look_at(Vec3(0,0,0))
        cam_control.target_z = -100
        
    # VELOCIDAD DE CÁMARA (CORREGIDA)
    if key == 'scroll up': 
        cam_control.move_speed *= 1.1
        cam_control.pan_speed *= 1.1
    if key == 'scroll down': 
        cam_control.move_speed *= 0.9
        cam_control.pan_speed *= 0.9

    if key == 'f':
        window.fullscreen = not window.fullscreen
    if key == 'escape':
        application.quit()

# --- BUCLE DE ACTUALIZACIÓN ---
def update():
    if not paused:
        # 1. Motores
        update_physics()
        update_metabolism()
        
        # 2. Sincronización y Limpieza
        to_destroy = []
        for i, (eid, v_ent) in enumerate(visual_entities):
            body = REGISTRY.physics[eid]
            bio = REGISTRY.biology[eid]
            
            if body and bio:
                v_ent.position = body.pos
                
                # Interpolación corregida: De rojo (muerte) a amarillo (vida)
                # Aseguramos que el valor esté entre 0 y 1
                energy_percent = clamp(bio.energy / bio.max_energy, 0, 1)
                v_ent.color = lerp(color.red, color.yellow, energy_percent)
            else:
                destroy(v_ent)
                to_destroy.append(i)
        
        for i in reversed(to_destroy):
            visual_entities.pop(i)
            
if __name__ == "__main__":
    app.run()