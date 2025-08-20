# app.py
from flask import Flask
import mysql.connector
import os
import time

app = Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'user': os.getenv('DB_USER', 'user1'),
    'password': os.getenv('DB_PASS', 'pass123'),
    'database': os.getenv('DB_NAME', 'mydb')
}

for i in range(5):
    try:
        conn = mysql.connector.connect(**db_config)
        break
    except Exception as e:
        print(f"Tentative {i+1}/5: MySQL pas encore prêt...")
        time.sleep(5)
        
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
        
@app.route('/debug')
def debug():
    return str(db_config)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
