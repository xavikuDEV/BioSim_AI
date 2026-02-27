# core/database.py
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class Simulation(Base):
    __tablename__ = 'simulations'
    id = Column(Integer, primary_key=True)
    seed = Column(Integer)
    status = Column(String) # ERA_0, ERA_I, etc.

class EntityRecord(Base):
    __tablename__ = 'entities'
    # uid es la verdadera llave primaria (autoincremental)
    uid = Column(Integer, primary_key=True, autoincrement=True) 
    id = Column(String) # ID de la entidad en el Registry (ej: '42')
    simulation_id = Column(Integer, ForeignKey('simulations.id'), nullable=True)
    generation = Column(Integer, default=0)
    dna = Column(JSON, nullable=True)
    cause_of_death = Column(String, nullable=True)
    timestamp = Column(String, default=lambda: datetime.now().isoformat())

# Inicializador de base de datos
DB_PATH = "sqlite:///data/db/biosim.db"
engine = create_engine(DB_PATH)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Crea el archivo y las tablas si no existen
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        # Activamos modo WAL para que no se bloquee al escribir 10k registros
        conn.execute(text("PRAGMA journal_mode=WAL;"))
        conn.commit()

def log_death(entity_id, cause="Impacto"):
    """Inserta un registro de muerte sin importar si el ID ya existía."""
    try:
        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO entities (id, cause_of_death, timestamp) VALUES (:id, :cause, :time)"),
                {"id": str(entity_id), "cause": cause, "time": datetime.now().isoformat()}
            )
            conn.commit()
    except Exception as e:
        print(f"⚠️ Error de persistencia: {e}")