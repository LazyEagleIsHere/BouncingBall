import uuid, os
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DB_URL = os.getenv("DB_URL", "sqlite:///./bouncing.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def now():
  return datetime.now(timezone.utc)

class Player(Base):
  __tablename__ = "players"
  id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
  name = Column(String, unique=True, nullable=False)
  created_at = Column(DateTime, default=now)
  scores = relationship("Score", back_populates="player")

class Score(Base):
  __tablename__ = "scores"
  id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
  player_id = Column(String, ForeignKey("players.id"), nullable=False)
  score = Column(Integer, nullable=False)
  level = Column(Integer, default=1)
  duration_ms = Column(Integer, default=0)
  run_id = Column(String, nullable=False)
  created_at = Column(DateTime, default=now)
  player = relationship("Player", back_populates="scores")
  __table_args__ = (UniqueConstraint("run_id", name="uq_scores_run_id"),)

def init_db():
  Base.metadata.create_all(bind=engine)
