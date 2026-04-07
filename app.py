from flask import Flask, render_template, request, redirect, session, url_for
import json
from logic import *
from formulas import *
import os 

app = Flask(__name__)
app.secret_key = os.urandom(24)

with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

@app.route("/", methods=["GET", "POST"])
def question():

    if request.args.get("reset") == "1":
        session.clear()
        return redirect(url_for("question"))

    if "index" not in session:
        session["index"] = 0
        session["scores"] = []

    if request.method == "POST":
        process_answer(session, request, questions)

    if session["index"] >= len(questions):
        return redirect(url_for("weights"))

    current_question = questions[session["index"]]
    q_type = current_question.get("type", "number")

    return render_template(
        "question.html",
        question=current_question,
        step=session["index"] + 1,
        qtype=q_type
    )


@app.route("/weights", methods=["GET", "POST"])
def weights():

    if request.method == "POST":
        try:
            session["weights"] = {
                "economic": float(request.form["economic"]),
                "environment": float(request.form["environment"]),
                "social": float(request.form["social"])
            }
        except (ValueError, KeyError):
            pass

        return redirect(url_for("results"))

    current_weights = session.get("weights", {
        "economic": None ,
        "environment": None ,
        "social":None 
    })

    return render_template("weights.html", weights=current_weights)


@app.route("/results")
def results():

    scores = session.get("scores", [])
    weights = session.get("weights")

    if not weights:
        return redirect(url_for("weights"))

    averages, total = calculate_results(questions, scores, weights)

    return render_template(
        "result.html",
        averages=averages,
        total=total
    )


if __name__ == "__main__":
    app.run(debug=True)