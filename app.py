from flask import Flask, render_template_string, request, redirect, url_for
import os

app = Flask(__name__)

# Notları tutan liste
notes = ["Azure üzerinde ilk notum!"]

@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Not Defteri</title>
        <style>
            body { font-family: sans-serif; margin: 40px; background-color: #f0f2f5; text-align: center; }
            .container { max-width: 500px; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: auto; }
            input { padding: 12px; width: 60%; border: 1px solid #ddd; border-radius: 8px; }
            button { padding: 12px 20px; background: #0084ff; color: white; border: none; border-radius: 8px; cursor: pointer; }
            li { background: #fff; margin: 10px 0; padding: 10px; border-radius: 8px; border-left: 5px solid #0084ff; list-style: none; text-align: left; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Not Defteri 📝</h1>
            <form action="/add" method="POST">
                <input type="text" name="note" placeholder="Not yaz..." required>
                <button type="submit">Ekle</button>
            </form>
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

@app.route('/add', methods=['POST'])
def add_note():
    note = request.form.get('note')
    if note:
        notes.append(note)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Azure için portu dinamik alalım
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
