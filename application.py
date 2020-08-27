import os

from cs50 import SQL
import re
from flask import Flask, flash, jsonify, redirect, render_template, request, session
#from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from quickchart import QuickChart
from helpers import lookup, apology, login_required


# Configure application
app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'F\x8eV\xe4y\xabk?\xc2m\x82\xb5\x10\xbfL\xea'

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
#app.config["SESSION_FILE_DIR"] = mkdtemp()
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("postgres://kcljriopkqstnn:772e48fc5ad6f7776e303f01f2fb9f0f1e95347d277daf466d715a6db7635e5a@ec2-54-246-87-132.eu-west-1.compute.amazonaws.com:5432/ddt45nfgtfdhke")


@app.route("/", methods=["GET"])
@login_required
def home_page():
    """HomePage page"""

    # Welcome user with his/her name
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])

    return render_template("homepage.html", username=name[0]["username"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # \*---- Server-side protection to ensure user gave valid inputs ----/*

        # Very interesting function that check if an email is valid, not blacklisted, properly formatted and really exists.
        # https://github.com/karolyi/py3-validate-email

        # Not so useful the regex here.
        if not re.fullmatch(
            r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
            request.form.get("email"),
        ):
            return apology("The e-mail you gave doesn't exist or it's invalid.", 403)

        if request.form.get("email") is "":
            return apology("must provide a email", 403)

        if not request.form.get("email"):
            return apology("must provide a email", 403)

        if len(request.form.get("email")) > 320:
            return apology("maximum email lenght is 320 charachters", 403)

        if not re.fullmatch(
            r"^[a-zA-Z][a-zA-Z0-9-_\.]{1,16}$", request.form.get("username")
        ):
            return apology("invalid username", 403)

        if not request.form.get("username"):
            return apology("must provide a username", 403)

        if len(request.form.get("username")) > 16:
            return apology("maximum username lenght is 16 charachters", 403)

        if request.form.get("password") is "" or request.form.get("confirmation") is "":
            return apology("must provide password", 403)

        if (
            len(request.form.get("password")) < 8
            or len(request.form.get("confirmation")) < 8
        ):
            return apology(
                "the password must has a minimun lenght of 8 characters", 403
            )

        if not re.fullmatch(
            r"(?=.*([A-Z]){1,})(?=.*[!@#$%^&*]{1,})(?=.*[0-9]{1,})(?=.*[a-z]{1,}).{8,100}$",
            request.form.get("password"),
        ):
            return apology(
                "Must contain at least one number, one uppercase and lowercase letter, one of the follow special characters !@#$%^&* characters and at least 8 or more characters",
                403,
            )

        # \*---- END ----/*

        # Check if there isn't other identical username on the database
        # the result will be stored in roll
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # If the len of the row is equal to 0, that means the username the user gave is unique
        # otherwise, if the len is equal to 1, that means the username already exists on the database
        if len(rows) == 1:
            flash("The username you selected is already in use. Try another one.")
            return redirect("/register")

        # Check if there isn't other identical email on the database
        rows_email = db.execute(
            "SELECT * FROM users WHERE email = ?", request.form.get("email")
        )

        # If the len of the row is equal to 0, that means the email the user gave is unique
        # otherwise, if the len is equal to 1, that means the email already exists on the database
        if len(rows_email) == 1:
            flash("The email you selected is already in use. Try another one.")
            return redirect("/register")

        # If password and confirmation don't match, accuse error
        if request.form.get("password") != request.form.get("confirmation"):
            flash("Password and Confirmation don't match. Try again.")
            return redirect("/register")

        else:

            # Hashes password before storying it into the database
            pass_hash = generate_password_hash(
                request.form.get("password"), method="pbkdf2:sha256", salt_length=8
            )

            # Store user's information in the database
            new_user = db.execute(
                "INSERT INTO users (username, email, hash, country) VALUES (?, ?, ?, ?)",
                request.form.get("username"),
                request.form.get("email"),
                pass_hash,
                request.form.get("country"),
            )

            # Start a session for the user after register
            session["user_id"] = new_user

            # Display a flash message that the registration occured
            flash("Registered!")

            return redirect("/")

    # Request method = GET
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("Invalid username and/or password.")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to HomePage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.pop('user_id', None)

    # Redirect user to index page
    return render_template("index.html")


@app.route("/change", methods=["GET", "POST"])
def change_password():
    """Allows user to change password"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # \*---- Server-side protection to ensure user gave valid inputs ----/*

        if request.form.get("username") is "":
            return apology("must provide a username", 403)

        if len(request.form.get("username")) > 16:
            return apology("maximum username lenght is 16 charachters", 403)

        if request.form.get("password") is "" or request.form.get("confirmation") is "":
            return apology("must provide password", 403)

        if (
            len(request.form.get("password")) < 8
            or len(request.form.get("confirmation")) < 8
        ):
            return apology(
                "the password must has a minimun lenght of 8 characters", 403
            )

        if not re.fullmatch(
            r"(?=.*([A-Z]){1,})(?=.*[!@#$%^&*]{1,})(?=.*[0-9]{1,})(?=.*[a-z]{1,}).{8,100}$",
            request.form.get("password"),
        ):
            return apology(
                "Must contain at least one number, one uppercase and lowercase letter, one of the follow special characters !@#$%^&* characters and at least 8 or more characters",
                403,
            )

        # \*---- END ----/*

        # If password and confirmation don't match, accuse error
        if request.form.get("new_password") != request.form.get("confirmation"):
            flash("The New Password and the Confirmation don't match. Try again.")
            return render_template("change.html")

        else:

            # Query database for username
            rows = db.execute(
                "SELECT * FROM users WHERE username = ?", request.form.get("username")
            )

            # Ensure username and password are correct to procede with the change
            if len(rows) != 1 or not check_password_hash(
                rows[0]["hash"], request.form.get("old_password")
            ):
                flash("Invalid username and/or password.")
                return render_template("change.html")

            else:

                # Hashes new password before storying it into the database
                pass_hash = generate_password_hash(
                    request.form.get("new_password"),
                    method="pbkdf2:sha256",
                    salt_length=8,
                )

                # Store usersname and password into database
                db.execute(
                    "UPDATE users SET hash = ? WHERE username = ?",
                    pass_hash,
                    request.form.get("username"),
                )

                # Display a flash message that the password was changed
                flash("Password changed!")

                return redirect("/")

    # Request method = GET
    else:
        return render_template("change.html")


@app.route("/write", methods=["GET", "POST"])
@login_required
def write():
    """Allows user to write entrances in his/her diary"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Insert into table the diary entries that the user gave
        db.execute(
            "INSERT INTO diary (user_id, date, event, local, people, feel) VALUES (?, ?, ?, ?, ?, ?)",
            session["user_id"],
            request.form.get("date"),
            request.form.get("event"),
            request.form.get("local"),
            request.form.get("people"),
            request.form.get("option"),
        )

        # Display a flash message
        flash("Done!")

        # Render the template
        return render_template("write.html")

    # Request method = GET
    else:
        return render_template("write.html")


@app.route("/diary", methods=["GET", "POST"])
@login_required
def diary():
    """Display user's diary"""

    # Get information from the database
    diary_history = db.execute(
        "SELECT date, event, local, people, feel FROM diary WHERE user_id = ? ORDER BY date DESC",
        session["user_id"],
    )

    return render_template("diary.html", diary_history=diary_history)


@app.route("/information", methods=["GET", "POST"])
@login_required
def covid_info():
    """Get Covid-19 informations about a country."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Call the function lookup to get the newest data about the Covid-19 from the API
        covid_info = lookup(request.form.get("country"))

        # If invalid input
        if covid_info == None:
            flash("Invalid country. Try again.")
            return redirect("/information")

        # Create a Bar Chart with the information returned from the API
        qc = QuickChart()
        qc.width = 500
        qc.height = 300
        qc.device_pixel_ratio = 2.0
        qc.config = {
            "type": "bar",
            "data": {
                "labels": covid_info["date"][22::2],
                "datasets": [
                    {"label": "Infected Persons", "data": covid_info["active"][22::2]},
                    {"label": "Total Deaths", "data": covid_info["deaths"][22::2]},
                ],
            },
        }

        image_url = qc.get_url()

        # return information
        return render_template(
            "information_result.html",
            country=covid_info["country"],
            active_cases=covid_info["active"][-1],
            total_deaths=covid_info["deaths"][-1],
            new_deaths=covid_info["new_deaths"],
            total_recovered=covid_info["recovered"][-1],
            date=covid_info["date"][-1],
            image_url=image_url,
        )

    # Request method = GET
    else:
        return render_template("information.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
