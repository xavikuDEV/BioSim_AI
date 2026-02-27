# laboratory/white_room.py
from ursina import *

def start_laboratory():
    # Inicialización estándar
    app = Ursina()
    
    # Configuración de ventana de Dios
    window.title = "BioSim_AI | The Sovereign Genesis (White Room)"
    window.borderless = False
    window.exit_button.visible = False
    window.fps_counter.enabled = True
    window.color = color.black
    
    # El plano de la realidad (Suelo)
    Entity(model='grid', scale=100, rotation=(90,0,0), color=color.dark_gray)
    
    # Cámara para el Arquitecto (Libre movimiento)
    EditorCamera()
    
    print("🔬 Sala Blanca lista para experimentos.")
    app.run()

if __name__ == "__main__":
    start_laboratory()