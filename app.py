from flask import Flask, request, jsonify
import sqlite3, time

app = Flask(__name__)

def db():
  conn = sqlite3.connect("leaderboard.db")
  conn.row_factory = sqlite3.Row
  return conn

def init_db():
  conn = db()
  cur = conn.cursor()
  cur.execute("""
  CREATE TABLE IF NOT EXISTS scores(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL,
    level TEXT,
    created_at INTEGER NOT NULL
  )""")
  conn.commit()
  conn.close()

@app.post("/api/submit-score")
def submit_score():
  data = request.get_json(force=True)
  score = data.get("score")
  level = data.get("level")

  conn = db()
  cur = conn.cursor()
  ts = int(time.time() * 1000)
  cur.execute("INSERT INTO scores(score, level, created_at) VALUES(?,?,?)",
              (int(score), level, ts))
  conn.commit()
  conn.close()
  return jsonify({"ok": True})

@app.get("/api/leaderboard")
def leaderboard():
  conn = db()
  cur = conn.cursor()
  cur.execute("""
    SELECT score, level, created_at
    FROM scores
    ORDER BY score DESC, created_at ASC
    LIMIT 50
  """)
  rows = [dict(r) for r in cur.fetchall()]
  conn.close()
  return jsonify(rows)

if __name__ == "__main__":
  init_db()
  app.run(host="0.0.0.0", port=8000)
