from ursina import Text, color

class LabUI:
    def __init__(self):
        self.status_text = Text(
            text="Velocidad: 1.0x", 
            position=(-0.85, 0.45), 
            color=color.yellow,
            scale=1.5
        )

    def update_status(self, paused, speed):
        if paused:
            self.status_text.text = "PAUSADO"
            self.status_text.color = color.red
        else:
            self.status_text.text = f"Velocidad: {speed}x"
            self.status_text.color = color.yellow