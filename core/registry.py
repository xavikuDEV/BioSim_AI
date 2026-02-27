# core/registry.py
import numpy as np
from core.components import PhysicsBody, BioLayer

class EntityRegistry:
    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        # Pools de componentes (Pre-asignación de memoria)
        self.physics = [None] * capacity
        self.biology = [None] * capacity
        
        # Gestión de IDs
        self.active_entities = []
        self.available_ids = list(range(capacity))

    def create_entity(self, pos=[0,0,0], mass=1.0):
        if not self.available_ids:
            return None
        
        entity_id = self.available_ids.pop()
        self.active_entities.append(entity_id)
        
        # Asignar componentes iniciales
        self.physics[entity_id] = PhysicsBody(pos=pos, vel=[0,0,0], mass=mass)
        self.biology[entity_id] = BioLayer()
        
        return entity_id

    def get_count(self):
        return len(self.active_entities)

# Instancia global del registro
REGISTRY = EntityRegistry()