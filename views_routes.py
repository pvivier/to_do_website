from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
import random
from extensions import db
from models import Prompt

views_bp = Blueprint("views", __name__)

success_messages = [
    "✔️ Saved successfully!", "✔️ Saved successfully!",
    "💦🍑 Juicy", "🤐 Boring!", "🤖 Bip Bop Submission Complete", "⚽️ Allez Brest!",
    "🤬 You should be naked", "⛏️ Travail Termine", "🎂 Happy Birthday.... again"
]

@views_bp.route("/")
def index():
    username = session.get('username')
    return render_template('index.html', username=username)

@views_bp.route("/choderlos", methods=["GET", "POST"])
def choderlos():
    if request.method == "POST":
        new_text = request.form.get("text", "").strip()
        if new_text:
            username = session.get("username", "unknown")
            new_prompt = Prompt(
                text=new_text,
                username=username,
                date=datetime.now().strftime("%Y-%m-%d"),
                category="choderlos"
            )
            db.session.add(new_prompt)
            db.session.commit()
            msg = random.choice(success_messages)
            return redirect(url_for("views.choderlos", saved_msg=msg))

    saved_msg = request.args.get("saved_msg", default=None)
    # get last choderlos entry or empty string if none
    last_entry = Prompt.query.filter_by(category="choderlos").order_by(Prompt.id.desc()).first()
    saved_text = last_entry.text if last_entry else ""
    return render_template("choderlos.html", text=saved_text, saved_msg=saved_msg)

@views_bp.route("/random_stuff", methods=["GET", "POST"])
def random_stuff():
    if request.method == "POST":
        new_text = request.form.get("text", "").strip()
        if new_text:
            username = session.get("username", "unknown")
            new_prompt = Prompt(
                text=new_text,
                username=username,
                date=datetime.now().strftime("%Y-%m-%d"),
                category="random"
            )
            db.session.add(new_prompt)
            db.session.commit()

            others = Prompt.query.filter(Prompt.category=="random", Prompt.id != new_prompt.id).all()
            selected = random.sample(others, k=min(2, len(others)))

            prompts_to_show = [new_prompt] + selected
            return render_template("random.html", prompts=prompts_to_show)

    all_prompts = Prompt.query.filter_by(category="random").all()
    initial_prompts = random.sample(all_prompts, k=min(3, len(all_prompts))) if all_prompts else []

    return render_template("random.html", prompts=initial_prompts)

@views_bp.route("/surprises", methods=["GET", "POST"])
def surprises():
    if session.get("username") != "pierre":
        return redirect(url_for("views.donald"))

    if request.method == "POST":
        new_text = request.form.get("text", "").strip()
        if new_text:
            username = session.get("username", "unknown")
            new_prompt = Prompt(
                text=new_text,
                username=username,
                date=datetime.now().strftime("%Y-%m-%d"),
                category="surprises"
            )
            db.session.add(new_prompt)
            db.session.commit()
            msg = random.choice(success_messages)
            return redirect(url_for("views.surprises", saved_msg=msg))

    saved_msg = request.args.get("saved_msg", default=None)
    last_entry = Prompt.query.filter_by(category="surprises").order_by(Prompt.id.desc()).first()
    saved_text = last_entry.text if last_entry else ""
    return render_template("surprises.html", text=saved_text, saved_msg=saved_msg)

@views_bp.route("/donald")
def donald():
    return render_template("donald.html")
