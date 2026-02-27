# tools/monitor_deaths.py
import sqlite3
import sys
from pathlib import Path

def analyze_deaths():
    db_path = Path("data/db/biosim.db")
    if not db_path.exists():
        print("❌ Error: No se encuentra la base de datos en data/db/biosim.db")
        print("Ejecuta el laboratorio primero para generar datos.")
        return

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Consultamos exactamente las columnas que queremos en el orden correcto
    query = """
    SELECT id, cause_of_death, timestamp 
    FROM entities 
    ORDER BY uid DESC 
    LIMIT 15
    """
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        print("\n--- 📜 ÚLTIMOS REGISTROS DE MORTALIDAD (Soberanía de Datos) ---")
        # Formateamos con espacios fijos para que parezca una tabla pro
        print(f"{'ID_Sim':<10} | {'Causa':<25} | {'Fecha/Hora'}")
        print("-" * 70)
        
        for row in rows:
            eid = str(row[0]) if row[0] is not None else "N/A"
            cause = str(row[1]) if row[1] is not None else "Impacto"
            time = str(row[2]) if row[2] is not None else "N/A"
            # Recortamos el timestamp para que no ocupe toda la pantalla
            short_time = time.split('.')[0].replace('T', ' ')
            print(f"{eid:<10} | {cause:<25} | {short_time}")
            
        count = cursor.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
        print(f"\n📊 Total de defunciones registradas: {count}")
        
    except sqlite3.OperationalError as e:
        print(f"❌ Error al leer la DB: {e}")
        print("Pista: Asegúrate de haber borrado la DB vieja anteriormente.")
    finally:
        conn.close()

if __name__ == "__main__":
    analyze_deaths()