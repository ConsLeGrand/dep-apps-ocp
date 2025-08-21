# app.py
from flask import Flask
import mysql.connector
import os
import elasticapm
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)

# Configuration APM
app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'flask-apm-ocp',
    'SERVER_URL': 'http://fleet01.heritage.africa:8200',  # à adapter selon ton infra
    'ENVIRONMENT': 'production'
}

# Initialiser APM
apm = ElasticAPM(app)

#config db
db_config = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'user': os.getenv('DB_USER', 'user1'),
    'password': os.getenv('DB_PASS', 'pass123'),
    'database': os.getenv('DB_NAME', 'mydb')
}

#connexion a la bd        
def get_connection():
    return mysql.connector.connect(**db_config)

# Créer table si pas encore créée
with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
    """)
    conn.commit()

#definition de la route racine
@app.route('/')
def index():
    return """
    <h2>Flask + MySQL Demo</h2>
    <form action="/add" method="get">
        <input type="text" name="name" placeholder="Enter a name">
        <input type="submit" value="Add">
    </form>
    <a href="/list">View all entries</a>
    """
#definition de la route pour ajouter une personne
@app.route('/add')
def add():
    name = request.args.get("name")
    if not name:
        return "Please provide ?name=..."
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO people (name) VALUES (%s)", (name,))
        conn.commit()
        return f"Added {name} ✅ <br><a href='/list'>See list</a>"
    except Exception as e:
        return f"Error inserting: {e}"

#definition de la route pour lister les personnes
@app.route('/list')
def list_entries():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM people")
        rows = cursor.fetchall()
        result = "<h2>People in DB</h2><ul>"
        for row in rows:
            result += f"<li>{row[0]} - {row[1]}</li>"
        result += "</ul><a href='/'>Back</a>"
        return result
    except Exception as e:
        return f"Error reading: {e}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
