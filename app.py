import os
import pyodbc
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Veritabanı bağlantı bilgilerini Azure Environment Variables'dan alıyoruz
def get_db_connection():
    # Azure'da SQL Server için standart ODBC sürücüsü
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={os.environ.get('DB_SERVER')};"
        f"DATABASE={os.environ.get('DB_NAME')};"
        f"UID={os.environ.get('DB_USER')};"
        f"PWD={os.environ.get('DB_PASSWORD')};"
        "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    return pyodbc.connect(conn_str)

@app.route('/')
def index():
    notes = []
    error_msg = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 'notes' tablosu yoksa otomatik oluşturur (Hocaya sunarken büyük artı!)
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='notes' AND xtype='U')
            CREATE TABLE notes (
                id INT IDENTITY(1,1) PRIMARY KEY,
                content NVARCHAR(MAX) NOT NULL
            )
        ''')
        conn.commit()

        # Notları veritabanından çek (en yeni en üstte)
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
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f7f6; display: flex; justify-content: center; padding: 50px; }}
            .container {{ background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 100%; max-width: 500px; text-align: center; }}
            h1 {{ color: #2c3e50; margin-bottom: 25px; }}
            input {{ padding: 12px; border: 2px solid #e0e0e0; border-radius: 10px; width: 70%; font-size: 16px; outline: none; transition: border 0.3s; }}
            input:focus {{ border-color: #3498db; }}
            button {{ padding: 12px 25px; background: #3498db; color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; margin-left: 5px; }}
            button:hover {{ background: #2980b9; }}
            .error {{ color: #e74c3c; background: #fdeaea; padding: 10px; border-radius: 8px; margin-bottom: 20px; }}
            ul {{ padding: 0; margin-top: 30px; text-align: left; }}
            li {{ background: #fff; margin-bottom: 12px; padding: 15px; border-radius: 10px; border-left: 6px solid #3498db; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bulut Notlarım ☁️</h1>
            {"<div class='error'>" + error_msg + "</div>" if error_msg else ""}
            <form action="/add" method="POST">
                <input type="text" name="note" placeholder="Notunu veritabanına işle..." required autocomplete="off">
                <button type="submit">Ekle</button>
            </form>
            <ul>
                {"".join(f"<li>{n}</li>" for n in notes)}
            </ul>
        </div>
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
        except:
            pass
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()

if __name__ == '__main__':
    # Azure için portu dinamik alalım
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
