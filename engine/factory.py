# engine/factory.py
import json
from pathlib import Path
from core.components import PhysicsBody, BioLayer
from core.genome import Genome

class EntityFactory:
    @staticmethod
    def spawn_from_assembly(assembly_name: str, position=[0,10,0]):
        """
        Ensambla una entidad leyendo piezas de entities/assembly/
        """
        # (Tu lógica original de la ERA 0 se mantiene aquí)
        from core.registry import REGISTRY
        eid = REGISTRY.create_entity(pos=position, mass=1.0)
        print(f"🧬 Entidad {eid} ensamblada desde assembly '{assembly_name}' en {position}")
        return eid

    @staticmethod
    def create_primordial_agent(pos):
        """
        Nuevo método ERA I: Crea los componentes con ADN aleatorio.
        Se devuelve el par (PhysicsBody, BioLayer) para que el Registry los almacene.
        """
        dna = Genome()
        
        # Física inyectada con genes
        physics = PhysicsBody(
            pos=list(pos),
            vel=[0.0, 0.0, 0.0],
            mass=dna.mass,
            radius=dna.size / 2
        )
        
        # Biología inyectada con genes
        biology = BioLayer()
        biology.genome = dna
        
        return physics, biology

# Instancia global
FACTORY = EntityFactory()