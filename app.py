import os
import pyodbc
from flask import Flask, render_template_string, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Veritabanı bağlantısı
def get_db_connection():
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )
    return pyodbc.connect(conn_str)

@app.route('/')
def index():
    notes = []
    error_msg = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # tablo yoksa oluştur
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='notes' AND xtype='U')
        CREATE TABLE notes (
            id INT IDENTITY(1,1) PRIMARY KEY,
            content NVARCHAR(MAX) NOT NULL
        )
        """)
        conn.commit()

        # notları çek
        cursor.execute("SELECT content FROM notes ORDER BY id DESC")
        notes = [row[0] for row in cursor.fetchall()]
        conn.close()

    except Exception as e:
        error_msg = f"Veritabanı bağlantısı kurulamadı: {str(e)}"

    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Azure Kalıcı Not Defteri</title>
    </head>
    <body style="font-family:Arial; text-align:center; margin-top:50px;">
        <h1>Bulut Notlarım ☁️</h1>

        {"<p style='color:red'>" + error_msg + "</p>" if error_msg else ""}

        <form action="/add" method="POST">
            <input type="text" name="note" required>
            <button type="submit">Ekle</button>
        </form>

        <ul style="list-style:none; padding:0;">
            {"".join(f"<li>{n}</li>" for n in notes)}
        </ul>
    </body>
    </html>
    '''
    return render_template_string(html)


@app.route('/add', methods=['POST'])
def add_note():
    note = request.form.get('note')

    if note:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (note,))
            conn.commit()
            conn.close()
        except Exception as e:
            print("Insert error:", e)

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Azure port ayarı
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

