import os
import psycopg2
from flask import Flask

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "example"),
        dbname=os.environ.get("DB_NAME", "postgres"),
    )

@app.route("/")
def home():
    return "Hello from my first Docker app!"

@app.route("/names")
def names():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM test;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return ", ".join(r[0] for r in rows)

@app.route("/add/<name>")
def add(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO test (name) VALUES (%s);", (name,))
    conn.commit()
    cur.close()
    conn.close()
    return f"Added {name}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)