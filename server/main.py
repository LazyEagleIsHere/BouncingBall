from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from .db import SessionLocal, init_db, Player, Score
import uuid, os

API_SECRET = os.getenv("API_SECRET", "change-me")

app = FastAPI(title="BouncingBall Sync API")
init_db()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def auth(x_api_key: str = Header(None)):
  if x_api_key != API_SECRET:
    raise HTTPException(status_code=401, detail="Unauthorized")

class PlayerUpsert(BaseModel):
  name: str = Field(min_length=1, max_length=64)

class ScoreSubmit(BaseModel):
  name: str
  score: int = Field(ge=0)
  level: int = Field(ge=1, default=1)
  duration_ms: int = Field(ge=0, default=0)
  run_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

@app.post("/players/upsert")
def upsert_player(payload: PlayerUpsert, db: Session = Depends(get_db), _=Depends(auth)):
  player = db.query(Player).filter(Player.name == payload.name).first()
  if not player:
    player = Player(name=payload.name)
    db.add(player)
    db.commit()
    db.refresh(player)
  return {"player_id": player.id, "name": player.name}

@app.post("/scores/submit")
def submit_score(payload: ScoreSubmit, db: Session = Depends(get_db), _=Depends(auth)):
  player = db.query(Player).filter(Player.name == payload.name).first()
  if not player:
    player = Player(name=payload.name)
    db.add(player)
    db.commit()
    db.refresh(player)
  existing = db.query(Score).filter(Score.run_id == payload.run_id).first()
  if existing:
    return {"status": "duplicate", "run_id": existing.run_id}
  score = Score(player_id=player.id, score=payload.score, level=payload.level,
                duration_ms=payload.duration_ms, run_id=payload.run_id)
  db.add(score)
  db.commit()
  db.refresh(score)
  return {"status": "ok", "score_id": score.id}

@app.get("/leaderboard/top")
def leaderboard_top(limit: int = 50, db: Session = Depends(get_db)):
  rows = (db.query(Player.name, Score.score, Score.level, Score.duration_ms, Score.created_at)
            .join(Score, Player.id == Score.player_id)
            .order_by(Score.score.desc(), Score.duration_ms.asc())
            .limit(limit).all())
  return [
    {
      "name": r[0],
      "score": r[1],
      "level": r[2],
      "duration_ms": r[3],
      "created_at": r[4].isoformat()
    }
    for r in rows
  ]
