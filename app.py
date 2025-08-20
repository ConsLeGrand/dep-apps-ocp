# app.py
from flask import Flask
import mysql.connector
import os

app = Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'user': os.getenv('DB_USER', 'user1'),
    'password': os.getenv('DB_PASS', 'pass123'),
    'database': os.getenv('DB_NAME', 'mydb')
}

@app.route('/')
def index():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT NOW()")
        result = cursor.fetchone()
        return f"Connexion MySQL OK - Time: {result[0]}"
    except Exception as e:
        return f"Erreur connexion MySQL : {str(e)}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
