import json
from pathlib import Path
from core.registry import REGISTRY

class EntityFactory:
    @staticmethod
    def spawn_from_assembly(assembly_name: str, position=[0,10,0]):
        """
        Ensambla una entidad leyendo piezas de entities/assembly/
        Ej: spawn_from_assembly("basic_head")
        """
        # En el futuro esto leerá múltiples JSON (head, torso, limbs)
        # Por ahora, simulamos el ensamblaje básico de la ERA 0
        eid = REGISTRY.create_entity(pos=position, mass=1.0)
        
        print(f"🧬 Entidad {eid} ensamblada y spawneada en {position}")
        return eid

# Instancia global
FACTORY = EntityFactory()