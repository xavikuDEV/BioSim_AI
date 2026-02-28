# tools/health_check.py
import sqlite3
from pathlib import Path
import sys

def check_system_integrity():
    db_path = Path("data/db/biosim.db")
    print("🩺 INICIANDO DIAGNÓSTICO DE SALUD...")
    
    # 1. Comprobación de Base de Datos
    if not db_path.exists():
        print("❌ ERROR: Base de datos no encontrada.")
    else:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        count = c.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
        causes = c.execute("SELECT cause_of_death, COUNT(*) FROM entities GROUP BY cause_of_death").fetchall()
        
        print(f"✅ Base de Datos: {count} registros totales.")
        for cause, n in causes:
            print(f"   - {cause}: {n}")
        conn.close()

    # 2. Comprobación de Estructura SSoT
    required_dirs = ["core", "engine", "data/db", "docs/systems"]
    for d in required_dirs:
        if Path(d).exists():
            print(f"✅ Carpeta '{d}' integrada.")
        else:
            print(f"⚠️ AVISO: Falta la carpeta crítica '{d}'.")

if __name__ == "__main__":
    check_system_integrity()