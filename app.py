from flask import Flask, render_template, request, redirect, session, url_for
import json
from logic import *
from formulas import *
import os 
import copy

# Creates Flask application
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load questions from JSON file 
with open("questions.json", "r", encoding="utf-8") as f:
    original_questions = json.load(f)

# Creates copy of the loaded questions 
questions = copy.deepcopy(original_questions)


# Routing to main page, displaying questions 
@app.route("/", methods=["GET", "POST"])
def question():

    # Function for reseting session, starting over with original questions 
    if request.args.get("reset") == "1":
        session.clear()
        global questions 
        questions = copy.deepcopy(original_questions)
        return redirect(url_for("question"))

    # Initializes session variables at first visit
    if "index" not in session:
        session["index"] = 0
        session["scores"] = []

    # Handles submission when user has answered a question in UI
    if request.method == "POST":
        process_answer(session, request, questions)

    # Handles redirection to weights when all questions are answered
    if session["index"] >= len(questions):
        return redirect(url_for("weights"))

    # Renders question template with relevant question data 
    return render_template(
        "question.html",
        question=questions[session["index"]],
        step=session["index"] + 1,
        qtype=questions[session["index"]].get("type", "number")
    )


# Routes to page for selecting weights 
@app.route("/weights", methods=["GET", "POST"])
def weights():

    # Stores weights in session when user submits weights, redirects to result page
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

    # Get existing weights or set default None 
    current_weights = session.get("weights", {
        "economic": None ,
        "environment": None ,
        "social":None 
    })

    # Renders weight template 
    return render_template("weights.html", weights=current_weights)


# Route for displaying results 
@app.route("/results")
def results():

    # Retrieves score and weights from session 
    scores = session.get("scores", [])
    weights = session.get("weights")

    if not weights:
        return redirect(url_for("weights"))

    # Calculates results based on answers and weights 
    averages, total = calculate_results(questions, scores, weights)

    # Renders results page based on calculated data 
    return render_template(
        "result.html",
        averages=averages,
        total=total
    )


# Main method for running the app 
if __name__ == "__main__":
    app.run(debug=True) # Debug activated for error messages when developing 