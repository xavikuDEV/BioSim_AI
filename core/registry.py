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

    def create_entity(self, pos=[0.0, 0.0, 0.0], mass=1.0):
        """Asigna un ID y componentes a una nueva entidad."""
        if not self.available_ids:
            return None
        
        # FIFO: Usamos el ID más antiguo disponible
        entity_id = self.available_ids.pop(0)
        self.active_entities.append(entity_id)
        
        # Inicialización de materia
        # Usamos list(pos) para evitar que todas las entidades compartan la misma referencia
        self.physics[entity_id] = PhysicsBody(pos=list(pos), vel=[0.0, 0.0, 0.0], mass=mass)
        self.biology[entity_id] = BioLayer()
        
        return entity_id

    def get_count(self):
        """Devuelve el número de entidades vivas."""
        return len(self.active_entities)

    def clear(self):
        """Piscina de purificación: Reinicia el universo en memoria."""
        self.active_entities = []
        self.available_ids = list(range(self.capacity))
        self.physics = [None] * self.capacity
        self.biology = [None] * self.capacity
        print("🧹 Registro limpiado: 10,000 IDs disponibles.")

# Instancia global única
REGISTRY = EntityRegistry()