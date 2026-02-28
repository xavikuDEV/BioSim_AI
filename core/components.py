# core/components.py
from dataclasses import dataclass, field

# Componente de Materia: Define la existencia física.
@dataclass(slots=True)
class PhysicsBody:
    pos: list[float]
    vel: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    mass: float = 1.0
    radius: float = 0.5

# Componente de Energía: Define la existencia metabólica.
@dataclass(slots=True)
class BioLayer:
    # --- JERARQUÍA DE TANQUES (SSoT) ---
    glycogen: float = 100.0   # Tanque 1: Uso inmediato (Carbohidratos)
    fat: float = 10.0        # Tanque 2: Reserva (Lípidos)
    protein: float = 100.0   # Tanque 3: Estructura muscular (Vida/Salud)
    
    # --- ESTADOS VITALES ---
    is_alive: bool = True
    age: int = 0
    generation: int = 0
    genome: object = None    # Referencia al ADN del individuo