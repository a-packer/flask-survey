from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

@app.route('/')
def home():
    title = satisfaction_survey.title
    return render_template('home.html', title=title)

@app.route('/start', methods=["GET", "POST"])
def start_survey():
    """Renders first question"""
    responses = []
    return redirect("/questions/0")


@app.route('/questions/<int:num>', methods=["GET", "POST"])
def question_page(num):
    """Renders current question"""
    # prevent user from trying to access a question number above our question count
    if (num > len(satisfaction_survey.questions)):
        return redirect(f'/questions/{len(responses)}')

    questions = satisfaction_survey.questions
    question = questions[int(num)].question
    choices = questions[int(num)].choices

    # if no responses, redirect to start
    if (responses is None):
        return redirect("/")
    # if user tries to access questions in wrong order, redirect them to current question
    if (num != len(responses)):
        flash("Invalid question number.")
        return redirect(f'/questions/{len(responses)}')

    return render_template('questions.html', num=num, question=question, choices=choices)

@app.route('/answer', methods=["POST"])
def answers():
    """Save response and redirect to next question."""
    # get the response choice
    choice = request.form['answer']
    responses.append(choice)

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/thanks")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/thanks')
def thank_user():
    """Renders the thank you page"""
    return render_template('thanks.html')



