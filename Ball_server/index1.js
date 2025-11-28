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
 * Records a score for a player. Scores are expected to be integers (1–10).
 */
app.post("/api/score", async (req, res) => {
  try {
    const { username, score } = req.body;

    if (
      typeof username !== "string" ||
      username.trim().length === 0 ||
      typeof score !== "number" ||
      !Number.isInteger(score) ||
      score < 1 ||
      score > 100
    ) {
      return res.status(400).json({ error: "Invalid payload: username (string) and score (int 1–100) required." });
    }

    // Ensure player exists
    await pool.query(
      "INSERT INTO players (username) VALUES (?) ON DUPLICATE KEY UPDATE username = VALUES(username)",
      [username.trim()]
    );

    // Insert score
    await pool.query(
      "INSERT INTO scores (player_id, score) VALUES ((SELECT id FROM players WHERE username = ?), ?)",
      [username.trim(), score]
    );

    res.json({ message: "Score submitted!" });
  } catch (err) {
    console.error("Error submitting score:", err);
    res.status(500).json({ error: "Error submitting score" });
  }
});

/**
 * GET /api/leaderboard
 * Returns frequency of scores between 1 and 10, sorted with 10 at top.
 * [{ score: 10, times: 3 }, { score: 9, times: 1 }, ..., { score: 1, times: 0 }]
 */
app.get("/api/leaderboard", async (req, res) => {
  try {
    const [rows] = await pool.query(
      `SELECT s.score, COUNT(*) AS times
       FROM scores s
       WHERE s.score BETWEEN 1 AND 100
       GROUP BY s.score
       ORDER BY s.score DESC`
    );
    res.json(rows);
  } catch (err) {
    console.error("Error fetching leaderboard:", err);
    res.status(500).json({ error: "Error fetching leaderboard" });
  }
});

/**
 * DELETE /api/clear
 * Clears all players and scores (resets frequency).
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