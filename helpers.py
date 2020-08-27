import os
import requests
import urllib.parse
from flask import redirect, render_template, request, session
from functools import wraps

# Import Slugify to convert country name into url slug for the API
from slugify import slugify


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return render_template("index.html")
        return f(*args, **kwargs)

    return decorated_function


def lookup(country):
    """Look up quote for symbol."""

    # Convert the user's input into a slug of a country name to be used in the query of the API
    country_name = slugify(country)

    # Contact API
    try:
        response = requests.get(
            f"https://api.covid19api.com/total/country/{urllib.parse.quote_plus(country_name)}"
        )
        response.raise_for_status()

    # if error in the request, return none
    except requests.RequestException:
        return None

    # Parse response
    try:
        # Store response in a variable called result
        result = response.json()

        # Get the relevant information from results
        active_cases = [d["Active"] for d in result]
        total_deaths = [d["Deaths"] for d in result]
        total_recovered = [d["Recovered"] for d in result]
        dates = [d["Date"] for d in result]

        # Compare the number of deaths on the current day with the day before
        compared_death_value = total_deaths[-1] - total_deaths[-2]

        # Formats the data output to make it more user friendly
        # Remove the hours and other not relevant information
        formated_date = []
        for index, i in enumerate(dates):
            formated_date.append(dates[index].replace(dates[index][10:], ""))

        # Return the information
        return {
            "country": result[-1]["Country"],
            "active": active_cases,
            "deaths": total_deaths,
            "new_deaths": compared_death_value,
            "recovered": total_recovered,
            "date": formated_date,
        }

    except (KeyError, TypeError, ValueError):
        return None
