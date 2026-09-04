from flask import Flask, request, render_template
import sqlite3

# Flask object creation
app = Flask(__name__)

# sqlite3 object creation
with sqlite3.connect('vulnerable.db') as db:
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT
        )
    ''')

    cursor.execute('''
        INSERT OR IGNORE INTO users ('name','password') VALUES('Ebube','passsword1')
    ''')

    cursor.execute('''
        INSERT OR IGNORE INTO users ('name','password') VALUES('Chidera','password2')
    ''')
    db.commit()

@app.route('/')
def main():
    return render_template("index.html")

# vulnerable login route
@app.route("/vulnerable_login", methods = ['POST', 'GET'])
def vul_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with sqlite3.connect('vulnerable.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM users WHERE name = '{username}' AND password = '{password}'")
            exists = cursor.fetchall()

            if exists:
                return "Login successful"
            else:
                return "Login failed try login again"

    return render_template("vulnerable_login.html")

# Secure login route
@app.route("/secure_login", methods = ['POST', 'GET'])
def secure_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with sqlite3.connect('vulnerable.db') as db:
            cursor = db.cursor()
            query = (username,password)
            cursor.execute("SELECT * FROM users WHERE name = ? AND password = ?", query)
            exists = cursor.fetchall()

            if exists:
                return "Login successful"
            else:
                return "Login failed try login again"

    return render_template("secure_login.html")
if __name__ == "__main__":
    app.run(debug=True)