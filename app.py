from flask import Flask, render_template, request, redirect, url_for, session
import os
import random
app = Flask(__name__)
app.secret_key = "talons"  # Needed to use sessions securely

users = {
    "pierre": "297bmz48",
    "galeuse": "pierreleplusbeau"
}

success_messages = [
    "✔️ Saved successfully!","✔️ Saved successfully!","✔️ Saved successfully!",
    "✔️ Saved successfully!","✔️ Saved successfully!","✔️ Saved successfully!",
    "✔️ Saved successfully!","✔️ Saved successfully!","✔️ Saved successfully!",
    "💦🍑 Juicy",
    "🤐 Boring!",
    "🤖 Bip Bop Submission Complete",
    "⚽️ Allez Brest!",
    "🤬 You should be naked",
    "⛏️ Travail Termine",
    "🎂 Happy Birthday.... again",
]

TEXT_FILE = 'texts/choderlos.txt'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route('/choderlos', methods=['GET', 'POST'])
def choderlos():
    if request.method == 'POST':
        new_text = request.form.get('text')
        os.makedirs('texts', exist_ok=True)
        with open(TEXT_FILE, 'w', encoding='utf-8') as f:
            f.write(new_text or '')
        # Pick a random success message
        msg = random.choice(success_messages)
        # Redirect passing the message as a query param (URL-encoded)
        return redirect(url_for('choderlos', saved_msg=msg))

    saved_text = ''
    if os.path.exists(TEXT_FILE):
        with open(TEXT_FILE, 'r', encoding='utf-8') as f:
            saved_text = f.read()

    saved_msg = request.args.get('saved_msg', default=None)
    return render_template('choderlos.html', text=saved_text, saved_msg=saved_msg)

@app.route("/surprises")
def surprises():
    # Only you can access this page
    if session.get("username") == "pierre":
        return render_template("surprises.html")
    else:
        return redirect(url_for("donald"))

@app.route("/donald")
def donald():
    return render_template("donald.html")

@app.route("/random")
def random_stuff():
    return render_template("random.html")

if __name__ == "__main__":
    app.run(debug=True)