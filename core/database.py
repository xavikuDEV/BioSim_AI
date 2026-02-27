# core/database.py
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Simulation(Base):
    __tablename__ = 'simulations'
    id = Column(Integer, primary_key=True)
    seed = Column(Integer)
    status = Column(String) # ERA_0, ERA_I, etc.

class EntityRecord(Base):
    __tablename__ = 'entities'
    id = Column(String, primary_key=True) # UUID
    simulation_id = Column(Integer, ForeignKey('simulations.id'))
    generation = Column(Integer)
    dna = Column(JSON)
    cause_of_death = Column(String, nullable=True)

# Inicializador de base de datos
DB_PATH = "sqlite:///data/db/biosim.db"
engine = create_engine(DB_PATH)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Creamos las tablas usando el objeto metadata
    Base.metadata.create_all(bind=engine)
    
    # Activar modo WAL para concurrencia Dashboard-Simulador
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL;"))
        conn.commit()