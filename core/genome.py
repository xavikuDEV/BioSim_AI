# core/genome.py
import random

class Genome:
    def __init__(self):
        # Hardware
        self.mass = random.uniform(0.5, 2.5)
        self.strength = random.uniform(0.5, 2.0)
        self.longevity = random.uniform(0.8, 1.5)
        
        # Software
        self.metabolic_efficiency = random.uniform(0.8, 1.2)
        self.immunity = random.uniform(0.1, 1.0)
        
        # Fenotipo
        self.size = 0.3 + (self.mass * 0.4)