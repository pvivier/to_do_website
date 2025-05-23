from flask import Flask, render_template
from auth import auth_bp
from views import views_bp
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(views_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)