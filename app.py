from flask import Flask, render_template, request, session
import random

app = Flask(__name__)

# Secret key for session management
app.secret_key = "stone-paper-scissors"


# Available choices
choices = ["rock", "paper", "scissors"]


@app.route("/", methods=["GET", "POST"])
def home():

    # Initialize scores
    if "user_score" not in session:
        session["user_score"] = 0
        session["computer_score"] = 0

    message = "Play your move"
    result = ""

    user_choice = ""
    computer_choice = ""

    # Check if user submitted a choice
    if request.method == "POST":

        # Reset game
        if request.form.get("reset"):

            session["user_score"] = 0
            session["computer_score"] = 0

            message = "Game Reset! Play your move."

        else:

            user_choice = request.form.get("choice")

            if user_choice in choices:

                # Computer randomly selects a choice
                computer_choice = random.choice(choices)

                # Check for draw
                if user_choice == computer_choice:

                    message = "It's a Draw!"
                    result = "draw"

                # Check if user wins
                elif (
                    (user_choice == "rock" and computer_choice == "scissors")
                    or
                    (user_choice == "paper" and computer_choice == "rock")
                    or
                    (user_choice == "scissors" and computer_choice == "paper")
                ):

                    session["user_score"] += 1

                    message = (
                        f"You won! {user_choice} beats {computer_choice}"
                    )

                    result = "win"

                # Otherwise computer wins
                else:

                    session["computer_score"] += 1

                    message = (
                        f"You lost. {computer_choice} beats your {user_choice}"
                    )

                    result = "lose"

    # Display the game
    return render_template(
        "index.html",
        user_score=session["user_score"],
        computer_score=session["computer_score"],
        message=message,
        result=result,
        user_choice=user_choice,
        computer_choice=computer_choice
    )


# Run Flask application
if __name__ == "__main__":
    app.run(debug=True)
