import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
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
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def check_strong_password(password):

    # Declare some variables to check password and to display alert on register.html
    alert=False
    digit_count=0   # Count no. of digits in a password
    upper_count=0   # Count no. of uppercase letters in a password
    lower_count=0   # Count no. of lowercase letters in a password
    special_count=0 # Count no. of special letters in a password
    len_password=len(password)

    # Iterate over every char in password
    for char in password :
        # Count no. of digits
        if char.isdigit():
            digit_count += 1
        # Count no. of uppercase chars
        elif char.isalpha() and char.isupper():
            upper_count += 1
        # Count no. of lowercase chars
        elif char.isalpha() and char.islower():
            lower_count += 1
        # Count no. of symbols
        else:
            special_count += 1

    # Display an alert if the no. of digits is not enough
    if digit_count < 8 :
        alert=True
        # Display an alert if the no. of uppercase or lowercase letters is not enough
    elif upper_count < 1 or lower_count < 1 :
        alert=True
    # Display an alert if the no. of special chars is not enough
    elif special_count < 1 :
        alert=True
    # Display an alert if the length of password is not enough
    elif len_password < 12 :
        alert=True

    return alert, digit_count, upper_count, lower_count, special_count, len_password