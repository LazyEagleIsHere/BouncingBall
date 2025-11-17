import os, uuid, time, requests

API_BASE = os.getenv("API_BASE", "http://your-server:8000")
API_KEY = os.getenv("API_KEY", "change-me")

def submit(name, score, level=1, duration_ms=0):
  run_id = str(uuid.uuid4())
  headers = {"X-API-Key": API_KEY}
  payload = {
    "name": name,
    "score": score,
    "level": level,
    "duration_ms": duration_ms,
    "run_id": run_id
  }
  try:
    r = requests.post(f"{API_BASE}/scores/submit", json=payload, headers=headers, timeout=5)
    r.raise_for_status()
    return r.json()
  except Exception as e:
    with open("unsent_scores.log", "a") as f:
      f.write(f"{payload}\n")
    return {"status": "cached_offline", "error": str(e)}

def flush_cached():
  headers = {"X-API-Key": API_KEY}
  if not os.path.exists("unsent_scores.log"):
    return
  lines = open("unsent_scores.log").read().strip().splitlines()
  open("unsent_scores.log", "w").close()
  for line in lines:
    payload = eval(line)
    try:
      r = requests.post(f"{API_BASE}/scores/submit", json=payload, headers=headers, timeout=5)
      r.raise_for_status()
    except Exception:
      with open("unsent_scores.log", "a") as f:
        f.write(f"{line}\n")

if __name__ == "__main__":
  start = time.time()
  # ... run game ...
  duration_ms = int((time.time() - start) * 1000)
  print(submit("PlayerHK", score=12345, level=7, duration_ms=duration_ms))
  flush_cached()
