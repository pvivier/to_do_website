from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint("auth", __name__)

users = {
    "pierre": "297bmz48",
    "galeuse": "pierreleplusbeau",
    "marie-sarah": "merteuil1782",
    "kerstin": "Christi@n1",
    "christian": "Christi@n1",
    "laurent": "Christi@n1"
}

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("views.index"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)

@auth_bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("views.index"))