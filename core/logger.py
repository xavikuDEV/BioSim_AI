# core/logger.py
import logging
import os
from pathlib import Path

# Forzar la creación de la ruta absoluta para evitar confusiones de Ursina
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "data" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "system.log"

# Configuración con codificación UTF-8 para evitar errores en Windows
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler() # También sale por consola
    ]
)

def get_logger(name):
    return logging.getLogger(name)

# Log de inicio para confirmar que funciona
get_logger("SYSTEM").info("🚀 Sistema de Logs iniciado correctamente.")