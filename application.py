# Skeleton of code taken from CS50 staff implementation of finance-2018
import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, Markup
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.route("/")
@login_required
def index():
    # Show bar graph w/ votes
    return render_template("index.html")


@app.route("/student_check", methods=["GET"])
def student_check():
    # Return true if username available, else false, in JSON format

    # Get username
    username = request.args.get("username")

    # Check for username (in both student and staff databases)
    if not len(username) or db.execute("SELECT 1 FROM student_users WHERE username = :username", username=username.lower()) or db.execute("SELECT 1 FROM staff_users WHERE username = :username", username=username.lower()):
        return jsonify(False)
    else:
        return jsonify(True)

@app.route("/staff_check", methods=["GET"])
def staff_check():
    # Return true if username available, else false, in JSON format

    # Get username
    username = request.args.get("username")

    # Check for username (in both student and staff databases)
    if not len(username) or db.execute("SELECT 1 FROM staff_users WHERE username = :username", username=username.lower()) or db.execute("SELECT 1 FROM student_users WHERE username = :username", username=username.lower()):
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Log user in

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query student database for username
        student_rows = db.execute("SELECT * FROM student_users WHERE username = :username",
                          username=request.form.get("username"))

        # Query staff database for username
        staff_rows = db.execute("SELECT * FROM staff_users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(student_rows) != 1 or not check_password_hash(student_rows[0]["hash"], request.form.get("password")):
            if len(staff_rows) != 1 or not check_password_hash(staff_rows[0]["hash"], request.form.get("password")):
                return apology("invalid username and/or password", 403)
        elif len(staff_rows) != 1 or not check_password_hash(staff_rows[0]["hash"], request.form.get("password")):
            if len(student_rows) != 1 or not check_password_hash(student_rows[0]["hash"], request.form.get("password")):
                return apology("invalid username and/or password", 403)

        # Determine if the user is a student or a staff member
        if len(student_rows) == 1 and check_password_hash(student_rows[0]["hash"], request.form.get("password")):
            # Remember which user has logged in
            session["user_id"] = student_rows[0]["id"]
        elif len(staff_rows) == 1 and check_password_hash(staff_rows[0]["hash"], request.form.get("password")):
            # Remember which user has logged in
            session["user_id"] = staff_rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Log user out

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/student_register", methods=["GET", "POST"])
def student_register():
    # Register student user for an account

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("username"):
            return apology("missing username")
        elif not request.form.get("password"):
            return apology("missing password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Add user to database
        id = db.execute("INSERT INTO student_users (username, hash) VALUES(:username, :hash)",
                        username=request.form.get("username"),
                        hash=generate_password_hash(request.form.get("password")))
        if not id:
            return apology("username taken")

        # Log user in
        session["user_id"] = id

        # Let user know they're registered
        flash("Registered!")
        return redirect("/")

    # GET
    else:
        return render_template("student_register.html")


@app.route("/staff_register", methods=["GET", "POST"])
def staff_register():
    # Register staff user for an account

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("username"):
            return apology("missing username")
        elif not request.form.get("password"):
            return apology("missing password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Add user to database
        id = db.execute("INSERT INTO staff_users (username, hash) VALUES(:username, :hash)",
                        username=request.form.get("username"),
                        hash=generate_password_hash(request.form.get("password")))
        if not id:
            return apology("username taken")

        # Log user in
        session["user_id"] = id

        # Let user know they're registered
        flash("Registered!")
        return redirect("/")

    # GET
    else:
        return render_template("staff_register.html")


@app.route("/staff_meal_entries", methods=["GET", "POST"])
@login_required
def staff_meal_entries():
    # Enable registered staff members to input yesterday's meals

    # POST
    if request.method == "POST":

        # Check that user is a staff member
        staff_row = db.execute("SELECT * FROM staff_users WHERE id = :id", id=session["user_id"])
        if not staff_row:
            return apology("only staff members can complete this form", 403)
        if not check_password_hash(staff_row[0]["hash"], request.form.get("password")):
            return apology("invalid password", 403)

        # Validate rest of form submission
        if not request.form.get("lunch"):
            return apology("missing lunch")
        elif not request.form.get("dinner"):
            return apology("missing dinner")

        # Input yesterday's meals into the meals database
        db.execute("INSERT INTO meals (lunch, dinner) VALUES(:lunch, :dinner)", lunch=request.form.get("lunch"), dinner=request.form.get("dinner"))

        # Bring user back to index.html
        return redirect("/")

    # GET
    else:
        return render_template("staff_meal_entries.html")


@app.route("/student_survey", methods=["GET", "POST"])
@login_required
def student_survey():
    # Enable registered students to rate yesterday's meals (the most recent meals input by the staff)

    # POST
    if request.method == "POST":

        # Check that user is a student
        student_row = db.execute("SELECT * FROM student_users WHERE id = :id", id=session["user_id"])
        if not student_row:
            return apology("only students can complete this form", 403)
        if not check_password_hash(student_row[0]["hash"], request.form.get("password")):
            return apology("invalid password", 403)

        # Validate rest of form submission
        for field in ["lunch", "dinner"]:
            value = request.form.get(field)
            if not value:
                return apology("must rate both lunch and dinner", 403)

        # Retrieve the meals row that should theoretically correspond to the nth day (https://stackoverflow.com/questions/7604893/sql-select-row-from-table-where-id-maxid)
        meal = db.execute("SELECT * FROM meals ORDER BY id DESC LIMIT 1")

        # Confirm that the user has not already responded for this particular meal
        current_meal_responses = db.execute("SELECT * FROM votes WHERE student_user_id = :student_user_id AND meals_id = :meals_id",
                                            student_user_id=session["user_id"],
                                            meals_id=meal[0]["id"])
        if len(current_meal_responses) > 0:
            return apology("you have already rated the meals for the most recent staff input", 403)


        # Insert information into votes database
        db.execute("INSERT INTO votes (lunch_rating, dinner_rating, student_user_id, meals_id) VALUES(:lunch_rating, :dinner_rating, :student_user_id, :meals_id)",
                    lunch_rating=int(request.form.get("lunch")),
                    dinner_rating=int(request.form.get("dinner")),
                    student_user_id=session["user_id"],
                    meals_id=meal[0]["id"])

        # Bring user back to index.html
        return redirect("/")

    # GET
    else:
        # Retrieve the staff input for lunch and dinner (https://stackoverflow.com/questions/7604893/sql-select-row-from-table-where-id-maxid)
        meals = db.execute("SELECT * FROM meals ORDER BY id DESC LIMIT 1")
        lunch = meals[0]["lunch"]
        dinner = meals[0]["dinner"]

        return render_template("student_survey.html", lunch=lunch, dinner=dinner)


@app.route("/survey_results", methods=["GET"])
@login_required
def survey_results():
    # Display the results of the student survey

    # Retrieve the staff input for lunch and dinner (https://stackoverflow.com/questions/7604893/sql-select-row-from-table-where-id-maxid)
    meals = db.execute("SELECT * FROM meals ORDER BY id DESC LIMIT 1")
    lunch = meals[0]["lunch"]
    dinner = meals[0]["dinner"]

    # Retrieve the vote counts for the lunch
    lunch_frequency_1 = db.execute("SELECT COUNT(*) FROM votes WHERE lunch_rating = 1")
    lunch_1 = lunch_frequency_1[0]['COUNT(*)']
    lunch_frequency_2 = db.execute("SELECT COUNT(*) FROM votes WHERE lunch_rating = 2")
    lunch_2 = lunch_frequency_2[0]['COUNT(*)']
    lunch_frequency_3 = db.execute("SELECT COUNT(*) FROM votes WHERE lunch_rating = 3")
    lunch_3 = lunch_frequency_3[0]['COUNT(*)']
    lunch_frequency_4 = db.execute("SELECT COUNT(*) FROM votes WHERE lunch_rating = 4")
    lunch_4 = lunch_frequency_4[0]['COUNT(*)']
    lunch_frequency_5 = db.execute("SELECT COUNT(*) FROM votes WHERE lunch_rating = 5")
    lunch_5 = lunch_frequency_5[0]['COUNT(*)']

    # Retrieve the vote counts for the dinner
    dinner_frequency_1 = db.execute("SELECT COUNT(*) FROM votes WHERE dinner_rating = 1")
    dinner_1 = dinner_frequency_1[0]['COUNT(*)']
    dinner_frequency_2 = db.execute("SELECT COUNT(*) FROM votes WHERE dinner_rating = 2")
    dinner_2 = dinner_frequency_2[0]['COUNT(*)']
    dinner_frequency_3 = db.execute("SELECT COUNT(*) FROM votes WHERE dinner_rating = 3")
    dinner_3 = dinner_frequency_3[0]['COUNT(*)']
    dinner_frequency_4 = db.execute("SELECT COUNT(*) FROM votes WHERE dinner_rating = 4")
    dinner_4 = dinner_frequency_4[0]['COUNT(*)']
    dinner_frequency_5 = db.execute("SELECT COUNT(*) FROM votes WHERE dinner_rating = 5")
    dinner_5 = dinner_frequency_5[0]['COUNT(*)']

    return render_template("survey_results.html", lunch=lunch, dinner=dinner, lunch_1=lunch_1, lunch_2=lunch_2, lunch_3=lunch_3, lunch_4=lunch_4,
                            lunch_5=lunch_5, dinner_1=dinner_1, dinner_2=dinner_2, dinner_3=dinner_3, dinner_4=dinner_4, dinner_5=dinner_5)


def errorhandler(e):
    # Handle error
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)