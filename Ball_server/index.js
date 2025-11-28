// server.js
const express = require("express");
const mysql = require("mysql2/promise");
const cors = require("cors");
require("dotenv").config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// MySQL connection pool
const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// Test connection at startup
(async () => {
  try {
    const conn = await pool.getConnection();
    await conn.ping();
    console.log("✅ Connected to MySQL");
    conn.release();
  } catch (err) {
    console.error("❌ MySQL connection failed:", err.message);
  }
})();

/**
 * POST /api/score
 * Body: { "username": "Alice", "score": 7 }
 * Records a score for a player.
 */
app.post("/api/score", async (req, res) => {
  try {
    const { username, score } = req.body;

    if (
      typeof username !== "string" ||
      username.trim().length === 0 ||
      typeof score !== "number" ||
      !Number.isInteger(score) ||
      score < 1
    ) {
      return res.status(400).json({ error: "Invalid payload: username (string) and score (int >=1) required." });
    }

    const uname = username.trim();

    // Ensure player exists
    await pool.query(
      "INSERT INTO players (username) VALUES (?) ON DUPLICATE KEY UPDATE username = VALUES(username)",
      [uname]
    );

    // Insert score
    await pool.query(
      "INSERT INTO scores (player_id, score) VALUES ((SELECT id FROM players WHERE username = ?), ?)",
      [uname, score]
    );

    res.json({ message: "Score submitted!" });
  } catch (err) {
    console.error("Error submitting score:", err);
    res.status(500).json({ error: "Error submitting score" });
  }
});

/**
 * GET /api/leaderboard
 * Returns frequency of scores.
 * Always includes 1–10 (descending), plus any >10 sorted descending at the top.
 * Example: [{ score: 25, times: 2 }, { score: 24, times: 1 }, ..., { score: 10, times: 3 }, ..., { score: 1, times: 0 }]
 */
app.get("/api/leaderboard", async (req, res) => {
  try {
    const [rows] = await pool.query(
      `SELECT s.score, COUNT(*) AS times
       FROM scores s
       GROUP BY s.score
       ORDER BY s.score DESC`
    );

    // Build frequency map for quick lookup
    const freqMap = {};
    rows.forEach(r => { freqMap[r.score] = Number(r.times); });

    const result = [];

    // Add >10 scores first (already sorted DESC by the query)
    rows.forEach(r => {
      if (r.score > 10) result.push({ score: r.score, times: Number(r.times) });
    });

    // Add scores 10 down to 1 (ensure entries even if 0)
    for (let s = 10; s >= 1; s--) {
      result.push({ score: s, times: freqMap[s] || 0 });
    }

    res.json(result);
  } catch (err) {
    console.error("Error fetching leaderboard:", err);
    res.status(500).json({ error: "Error fetching leaderboard" });
  }
});

/**
 * DELETE /api/clear
 * Clears all players and scores.
 */
app.delete("/api/clear", async (req, res) => {
  try {
    await pool.query("TRUNCATE TABLE scores");
    await pool.query("TRUNCATE TABLE players");
    res.json({ message: "Leaderboard cleared!" });
  } catch (err) {
    console.error("Error clearing leaderboard:", err);
    res.status(500).json({ error: "Error clearing leaderboard" });
  }
});

app.listen(port, "0.0.0.0", () => {
  console.log(`🚀 Server running on port ${port}`);
});
