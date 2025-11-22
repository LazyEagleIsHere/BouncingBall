from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'gameclient'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'leaderboard'

mysql = MySQL(app)

@app.route('/scores', methods=['POST'])
def post_score():
  data = request.get_json()
  name = data.get('name', 'Anonymous')[:50]
  score = int(data.get('score', 0))
  cur = mysql.connection.cursor()
  cur.execute("INSERT INTO scores (name, score) VALUES (%s, %s)", (name, score))
  mysql.connection.commit()
  cur.close()
  return jsonify({'status': 'ok'}), 201

@app.route('/scores', methods=['GET'])
def get_scores():
  cur = mysql.connection.cursor()
  cur.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 50")
  rows = cur.fetchall()
  cur.close()
  return jsonify([{'name': r[0], 'score': r[1]} for r in rows])

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
