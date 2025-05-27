from extensions import db

class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(20), nullable=False, default="random")  # new field
