# core/constants.py
import yaml
from pathlib import Path
from pydantic import BaseModel

class WorldConfig(BaseModel):
    GRAVITY: float
    AIR_DENSITY: float
    GROUND_FRICTION: float
    TIME_STEP: float
    COLLISION_ELASTICITY: float

class MetabolicConfig(BaseModel):
    GLYCOGEN_BURN_RATE: float
    FAT_TO_ENERGY_RATIO: float
    PROTEIN_DECAY_RATE: float
    BASE_METABOLIC_RATE: float
    EFFORT_MULTIPLIER: float

def load_config():
    base_path = Path(__file__).parent.parent / "config"
    
    with open(base_path / "world_settings.yaml", "r") as f:
        world_data = yaml.safe_load(f)["world_constants"]
        
    with open(base_path / "metabolic_rules.yaml", "r") as f:
        metabolic_data = yaml.safe_load(f)["metabolism"]
        
    return WorldConfig(**world_data), MetabolicConfig(**metabolic_data)

# Inyección global de constantes
WORLD, METABOLISM = load_config()