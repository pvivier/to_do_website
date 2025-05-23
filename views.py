from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
import os
import random
from utils import load_prompts, save_prompts

views_bp = Blueprint("views", __name__)
PROMPTS_FILE = "texts/prompts.json"
TEXT_FILE = "texts/choderlos.txt"

success_messages = [
    "✔️ Saved successfully!",
    "💦🍑 Juicy", "🤐 Boring!", "🤖 Bip Bop Submission Complete", "⚽️ Allez Brest!",
    "🤬 You should be naked", "⛏️ Travail Termine", "🎂 Happy Birthday.... again"
]

@views_bp.route("/")
def index():
    return render_template("index.html")

@views_bp.route("/choderlos", methods=["GET", "POST"])
def choderlos():
    if request.method == "POST":
        new_text = request.form.get("text")
        os.makedirs(os.path.dirname(TEXT_FILE), exist_ok=True)
        with open(TEXT_FILE, "w", encoding="utf-8") as f:
            f.write(new_text or "")
        msg = random.choice(success_messages)
        return redirect(url_for("views.choderlos", saved_msg=msg))

    saved_text = ""
    if os.path.exists(TEXT_FILE):
        with open(TEXT_FILE, "r", encoding="utf-8") as f:
            saved_text = f.read()

    saved_msg = request.args.get("saved_msg", default=None)
    return render_template("choderlos.html", text=saved_text, saved_msg=saved_msg)

@views_bp.route("/random_stuff", methods=["GET", "POST"])
def random_stuff():
    prompts = load_prompts(PROMPTS_FILE)

    if request.method == "POST":
        new_text = request.form.get("text", "").strip()
        if new_text and "username" in session:
            new_prompt = {
                "text": new_text,
                "username": session["username"],
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            prompts.append(new_prompt)
            save_prompts(PROMPTS_FILE, prompts)

            others = [p for p in prompts if p != new_prompt]
            selected = random.sample(others, k=min(2, len(others)))
            prompts_to_show = [new_prompt] + selected

            return render_template("random.html", prompts=prompts_to_show)

    return render_template("random.html", prompts=None)

@views_bp.route("/surprises")
def surprises():
    if session.get("username") == "pierre":
        return render_template("surprises.html")
    else:
        return redirect(url_for("views.donald"))

@views_bp.route("/donald")
def donald():
    return render_template("donald.html")