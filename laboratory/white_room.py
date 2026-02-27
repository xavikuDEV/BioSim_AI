# laboratory/white_room.py
from ursina import *

def start_laboratory():
    app = Ursina()
    
    # Ajustes de Interfaz para el Arquitecto
    window.title = "BioSim_AI | Sovereign Genesis"
    window.fps_counter.enabled = True
    window.fps_counter.color = color.green
    window.fps_counter.scale = 2 # Hacer los números más grandes
    window.color = color.black # Fondo para contraste
    
    # Solución al error de 'grid': Usamos un plano con textura manual
    ground = Entity(
        model='plane', 
        scale=100, 
        texture='white_cube', # Textura básica de Ursina
        texture_scale=(100,100), 
        color=color.dark_gray
    )
    
    # Iluminación básica (Soberanía visual)
    PointLight(parent=camera, position=(0,10,-10), color=color.white)
    
    # Cámara Libre
    EditorCamera()
    
    print("🔬 Sala Blanca: Cuadrícula restaurada e iluminación activa.")
    app.run()

if __name__ == "__main__":
    start_laboratory()