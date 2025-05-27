from flask import Flask
from extensions import db
from flask_migrate import Migrate
from auth_routes import auth_bp
from views_routes import views_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(views_bp)

@app.route("/")
def index():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
