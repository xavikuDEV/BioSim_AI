# core/database.py
from sqlalchemy import Column, Integer, String, JSON, Float, ForeignKey, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from pathlib import Path

Base = declarative_base()

class Simulation(Base):
    __tablename__ = 'simulations'
    id = Column(Integer, primary_key=True)
    seed = Column(Integer)
    status = Column(String)

class EntityRecord(Base):
    __tablename__ = 'entities'
    uid = Column(Integer, primary_key=True, autoincrement=True) 
    id = Column(String)
    simulation_id = Column(Integer, ForeignKey('simulations.id'), nullable=True)
    generation = Column(Integer, default=0)
    dna = Column(JSON, nullable=True)
    cause_of_death = Column(String, nullable=True)
    timestamp = Column(String, default=lambda: datetime.now().isoformat())

class SnapshotRecord(Base):
    __tablename__ = 'snapshots'
    tick = Column(Integer, primary_key=True)
    count = Column(Integer)
    avg_glycogen = Column(Float)
    avg_mass = Column(Float)

DB_PATH = "sqlite:///data/db/biosim.db"
engine = create_engine(DB_PATH)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Crear carpeta si no existe
    Path("data/db").mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL;"))
        conn.commit()

def log_snapshot(tick, registry):
    """Guarda telemetría de la población en la base de datos."""
    active = [eid for eid in registry.active_entities if registry.biology[eid]]
    if not active: return
    
    count = len(active)
    avg_glycogen = sum(registry.biology[eid].glycogen for eid in active) / count
    avg_mass = sum(registry.physics[eid].mass for eid in active) / count

    session = SessionLocal()
    try:
        snap = SnapshotRecord(tick=tick, count=count, avg_glycogen=avg_glycogen, avg_mass=avg_mass)
        session.merge(snap) # merge evita errores de duplicado en el mismo tick
        session.commit()
    except Exception as e:
        print(f"⚠️ Error en snapshot: {e}")
    finally:
        session.close()

def log_death(entity_id, cause="Impacto"):
    try:
        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO entities (id, cause_of_death, timestamp) VALUES (:id, :cause, :time)"),
                {"id": str(entity_id), "cause": cause, "time": datetime.now().isoformat()}
            )
            conn.commit()
    except Exception as e:
        print(f"⚠️ Error de persistencia: {e}")