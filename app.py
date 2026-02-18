from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Notların tutulacağı liste (Şimdilik geçici, uygulama her restart olduğunda sıfırlanır)
notes = []

@app.route('/')
def index():
    # Basit bir HTML tasarımı
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kankamın Not Defteri</title>
        <style>
            body { font-family: sans-serif; margin: 40px; background-color: #f4f4f4; }
            .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            input[type="text"] { padding: 10px; width: 70%; border: 1px solid #ddd; border-radius: 5px; }
            button { padding: 10px 20px; background: #0078d4; color: white; border: none; border-radius: 5px; cursor: pointer; }
            ul { list-style: none; padding: 0; }
            li { background: #eee; margin: 5px 0; padding: 10px; border-radius: 5px; display: flex; justify-content: space-between; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Not Defteri 📝</h1>
            <form action="/add" method="POST">
                <input type="text" name="note" placeholder="Bir şeyler yaz..." required>
                <button type="submit">Ekle</button>
            </form>
            <hr>
            <ul>
                {% for note in notes %}
                    <li>{{ note }}</li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, notes=notes)

@app.route('/add', method=['POST'])
def add_note():
    note = request.form.get('note')
    if note:
        notes.append(note)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
