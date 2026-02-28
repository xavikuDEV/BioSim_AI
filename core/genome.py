# core/genome.py
import random

class Genome:
    def __init__(self):
        # Gen 1: Masa (Afecta inercia)
        self.mass = random.uniform(0.5, 2.0)
        
        # Gen 2: Eficiencia (Afecta gasto energético)
        self.metabolic_efficiency = random.uniform(0.8, 1.2)
        
        # Fenotipo: El tamaño visual se deriva de la masa
        self.size = 0.4 + (self.mass * 0.4)