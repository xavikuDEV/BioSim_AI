# core/components.py
from dataclasses import dataclass

@dataclass(slots=True)
class PhysicsBody:
    """Componente de Materia: Define la existencia física."""
    pos: list[float]      # [x, y, z]
    vel: list[float]      # [vx, vy, vz]
    mass: float
    radius: float = 0.5

@dataclass(slots=True)
class BioLayer:
    """Componente de Metabolismo: Los 3 tanques de energía."""
    glycogen: float = 100.0  # Energía inmediata
    fat: float = 10.0       # Reserva largo plazo
    protein: float = 100.0  # Estructura (Salud)