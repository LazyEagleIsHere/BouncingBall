require('dotenv').config();
const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
});

// Ensure player exists
async function ensurePlayer(username) {
  const [rows] = await pool.query('SELECT id FROM players WHERE username=?', [username]);
  if (rows.length) return rows[0].id;
  const [result] = await pool.query('INSERT INTO players (username) VALUES (?)', [username]);
  return result.insertId;
}

// Submit score
app.post('/api/score', async (req, res) => {
  const { username, score } = req.body;
  if (!username || !score) return res.status(400).json({ error: 'Missing fields' });
  const playerId = await ensurePlayer(username);
  await pool.query('INSERT INTO scores (player_id, score) VALUES (?, ?)', [playerId, score]);
  res.json({ status: 'ok' });
});

// Leaderboard
app.get('/api/leaderboard', async (req, res) => {
  const [rows] = await pool.query(`
    SELECT p.username, MAX(s.score) AS best_score
    FROM scores s
    JOIN players p ON p.id = s.player_id
    GROUP BY p.username
    ORDER BY best_score DESC
    LIMIT 10
  `);
  res.json(rows);
});

app.listen(3000, () => console.log('Server running on port 3000'));
