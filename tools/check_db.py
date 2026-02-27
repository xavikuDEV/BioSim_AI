import sqlite3
import pandas as pd # Si no lo tienes: uv pip install pandas

def analyze_last_deaths():
    conn = sqlite3.connect('data/db/biosim.db')
    # Extraemos los últimos 20 registros
    query = "SELECT id, cause_of_death, timestamp FROM entities ORDER BY uid DESC LIMIT 20"
    df = pd.read_sql_query(query, conn)
    
    if df.empty:
        print("📭 La base de datos está vacía. ¡Haz que mueran algunas entidades!")
    else:
        print("\n--- 📜 REPORTE DE MORTALIDAD (Soberanía de Datos) ---")
        print(df.to_string(index=False))
        
        # Estadística rápida
        total = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
        print(f"\n📊 Total de eventos registrados: {total}")
    conn.close()

if __name__ == "__main__":
    analyze_last_deaths()