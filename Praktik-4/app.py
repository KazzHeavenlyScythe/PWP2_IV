import os
from flask import Flask, render_template
import mysql.connector
from dotenv import load_dotenv

# Konfigurasi .env di flask
load_dotenv()

# Deklarasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi koneksi mysql di flask
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=3033
    )

# Menampilkan data todolist dengan HTTP GET
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Ambil semua data dari tabel todos
    cursor.execute("SELECT * FROM todos ORDER BY deadline ASC")
    todos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Render template index.html dengan membawa data todos
    return render_template('index.html', todos=todos)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
