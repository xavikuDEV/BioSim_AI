# laboratory/controls.py
from ursina import camera, Vec3, application, time, color, mouse

def handle_god_keys(key, lab_state, ui, player, spawn_func): # <--- AÑADIMOS 'player'
    # ESC para liberar el ratón
    if key == 'escape':
        mouse.locked = not mouse.locked

    if key == 'p':
        lab_state.paused = not lab_state.paused
        time.time_scale = 0 if lab_state.paused else lab_state.speed
        ui.update_status(lab_state.paused, lab_state.speed)
        
    if key in ('+', 'kp_plus'):
        lab_state.speed = min(lab_state.speed + 0.5, 5.0)
        if not lab_state.paused: time.time_scale = lab_state.speed
        ui.update_status(lab_state.paused, lab_state.speed)

    if key in ('-', 'kp_minus'):
        lab_state.speed = max(lab_state.speed - 0.5, 0.1)
        if not lab_state.paused: time.time_scale = lab_state.speed
        ui.update_status(lab_state.paused, lab_state.speed)

    # Cámara y Navegación
    if key == 'c':
        # Ahora 'player' sí existe en este ámbito
        player.position = (0, 30, -100)
        player.rotation = (0, 0, 0)
        camera.rotation = (0, 0, 0)
        print("📍 Cámara de Dios centrada.")
        
    if key == '1': spawn_func(1)
    if key == '2': spawn_func(100)
    if key == '3': spawn_func(2000)
    if key == 'r': spawn_func(lab_state.current_count)