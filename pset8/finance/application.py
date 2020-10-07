import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, check_strong_password

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Query stocks and cash per the user from database
    # rows is a list of dicts
    rows = db.execute("SELECT * FROM stocks WHERE user_id = :user_id",
                          user_id=session["user_id"])
    # user is a list of dicts
    user = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id=session["user_id"])

    cash = user[0]['cash']
    username = user[0]['username']

    stocks = []
    total = cash

    # for loop to lookup current stocks price the user has
    for index, row in enumerate(rows) :
        # lookup for symbol informations
        lookup_result = lookup(row['symbol'])

        # create a list which contains [symbol, name, amount, price, total price] of each stock and append it to a list of every stock owned by the user
        stocks.append(list((lookup_result['symbol'], lookup_result['name'], row['amount'], lookup_result['price'], round(lookup_result['price'] * row['amount'], 2))))
        # sum all the stocks values and add it to the total which is initiated at the amount of money the user has in his account
        total += stocks[index][4]

    # load index page with username, stocks, cash, total
    return render_template("index.html", username=username, stocks=stocks, cash=round(cash, 2), total=round(total, 2), symbols=rows)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST" :

        # Convert symbol to uppercase to prevent duplicate and different entires for the same stock
        symbol=request.form.get("symbol").upper()

        # Ensure symbol was submitted
        if not symbol:
            return apology("you must provide symbol", 400)

        # Ensure stock symbol is correct
        if not lookup(symbol):
            return apology("Could not find this symbol stock", 400)

        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("you must provide shares", 400)

        amount=int(request.form.get("shares"))

        stock_price = lookup(symbol)['price']

        value = amount * stock_price

        user = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id=session["user_id"])

        cash = user[0]['cash']

        if cash < value or cash == 0 :
            return apology("you dont have enough money", 400)

        # Check if user already has one or more stocks from the same company
        stock_exist = db.execute("SELECT amount FROM stocks WHERE user_id = :user_id AND symbol = :symbol",
                          user_id=session["user_id"], symbol=symbol)

        # Insert new row into the stock table
        if not stock_exist:
            db.execute("INSERT INTO stocks(user_id, symbol, amount) VALUES (:user_id, :symbol, :amount)",
                user_id=session["user_id"], symbol=symbol, amount=amount)

        # update row into the stock table
        else:
            # New variable to not overwrite "amount" variable, when we enter its value in transaction table below
            updated_amount = amount
            updated_amount += stock_exist[0]['amount']

            db.execute("UPDATE stocks SET amount = :amount WHERE user_id = :user_id AND symbol = :symbol",
                user_id=session["user_id"], symbol=symbol, amount=updated_amount)

        # Update transactions table
        db.execute("INSERT INTO transactions (user_id, symbol, amount, value) VALUES (:user_id, :symbol, :amount, :value)",
                    user_id=session["user_id"], symbol=symbol, amount=amount, value=stock_price)

        # Update the user's cash
        db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                          cash=round(cash-value, 2), user=session["user_id"])

        flash("Bought!")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Declare transactions to be a list of dicts
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = :user_id",
                          user_id=session["user_id"])

    # Empty dictionary to be temp placeholder for the stock name
    # before adding it to every dict in transactions list
    stock_names = {}

    # To add a new key called 'name' in each dict in transactions list
    for index in range(len(transactions)) :
        if transactions[index]['symbol'] == "$$$$" :
            transactions[index]['name'] = "Cash Deposit"
        else:
            stock_names[index] = lookup(transactions[index]['symbol'])['name']
            transactions[index]['name'] = stock_names[index]

    return render_template("history.html", transactions=transactions)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to login page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST" :

        # get symbol value from from
        symbol = request.form.get("symbol")

        # check whether value is empty or not
        if not symbol:
            return apology("symbol cannot be empty", 601)

        result = lookup(symbol) # lookup function returns None if there is no correct lookup

        # check if symbol is wrong or not
        if result == None :
            return apology("Wrong Symbol", 602)

        # render quoted.html to display the stock price for the symbol
        return render_template("quoted.html", result=result)

    # if the method is GET then go ahead and load quote.html page
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # If the user has submitted the form
    if request.method == "POST" :

        # Store the username the user has submitted
        username = request.form.get("username")
        # Store password from user
        password = request.form.get("password")
        password_again = request.form.get("password_again")

        # Ensure username was submitted
        if not username :
            return apology("Must provide username", 403)

        # Ensure password was submitted and match
        if not password:
            return apology("Must provide password", 403)
        elif password != password_again :
            return apology("The two passwords don't match", 403)

        # Check password for being strong
        alert, digit_count, upper_count, lower_count, special_count, len_password = check_strong_password(password)

        # If alert is true then the password is weak
        if alert :
            return  render_template("register.html", alert=alert, digit=digit_count, upper=upper_count, lower=lower_count, special=special_count, length=len_password)

        # Query the database for any users has the same name
        usernames = db.execute("SELECT username FROM users WHERE username = ?", username)

        # If there is one match then display an apology
        if len(usernames) != 0 :
            return apology("Username is already taken", 403)

        # Insert (username, password) into database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
                    username=username, password=generate_password_hash(password))

        # Query the user's id and store it in rows
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Store user's id to login in after redirected to homepage
        session["user_id"] = rows[0]["id"]

        flash("Registered!")

        # After inserting into database redirect user to homepage
        return redirect("/")

    # If the user has used the GET method
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Query database for available stocks for the user and their share
    available_symbols = db.execute("SELECT * FROM stocks WHERE user_id = :user_id",
              user_id=session["user_id"])

    if request.method == "POST" :

        # If user left symbol field blank return apology
        if not request.form.get("symbol") :
            return apology("missing symbol", 415)

        # If user left amount of shares field blank return apology
        if not request.form.get("shares") :
            return apology("share cannot be empty", 416)

        # Get the values the user has submitted
        sell_symbol = request.form.get("symbol")
        sell_amount = int(request.form.get("shares"))

        # Lookup current stock price for sell
        stock_price = lookup(sell_symbol)['price']

        # Iterate over available_symbols (list of dicts) to get the symbol information
        for current_symbol in available_symbols:

            # If we found the symbol the user wants to sell
            if sell_symbol == current_symbol['symbol'] :

                # We store the current amount the user has into a new variable
                current_amount = int(current_symbol['amount'])
                # Then we subtract the amount the user wants to sell from it
                current_amount = current_amount - sell_amount

                # If the current amount < 0 then apology that he doesnot have enough shares
                if current_amount < 0 :
                    return apology("No enough shares for you to sell")
                # If the current amount is now zero then delete this symbol from the user's record
                if current_amount == 0 :
                    # Delete symbol from database
                    db.execute("DELETE FROM stocks WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=sell_symbol)
                else:
                    # If current_amount is not <= 0
                    # Update the amount of shares the user has for this symbol
                    db.execute("UPDATE stocks SET amount = :amount WHERE user_id = :user_id AND symbol = :symbol",
                                user_id=session["user_id"], symbol=sell_symbol, amount = current_amount)

                # Update the transactions table
                db.execute("INSERT INTO transactions (user_id, symbol, amount, value) VALUES (:user_id, :symbol, :amount, :value)",
                            user_id=session["user_id"], symbol=sell_symbol, amount=(-(sell_amount)), value=stock_price)

                # Query user's cash
                cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]['cash']

                # New value of cash after stock sale
                new_cash = cash + stock_price * sell_amount

                # Update user's cash
                db.execute("UPDATE users SET cash = :new_cash WHERE id = :user",
                          new_cash=round(new_cash, 2), user=session["user_id"])

                # Break out of for loop because there will be no more symbols other than this one
                # to save time by not iterating over symbols that won't equal the user's required symbol
                break;

        flash("Sold!")
        # After successful sale opearation redirect user to homepage
        return redirect("/")

    return render_template("sell.html", symbols=available_symbols)


@app.route("/settings")
@login_required
def settings():
    """Settings Page to change password or add deposit"""
    # user is a list of dicts
    user = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id=session["user_id"])
    username = user[0]['username']

    return render_template("settings.html", username=username)


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Change Password"""
    if request.method=="POST" :

        # Check for password being empty
        if not request.form.get("old_password") :
            return apology("current password cannot be empty")

        elif not request.form.get("new_password") :
            return apology("new password cannot be empty")

        elif not request.form.get("new_password_again") :
            return apology("password (again) is left blank")
        # Check if the two passwords match
        elif request.form.get("new_password") != request.form.get("new_password_again") :
            return apology("the two passwords don't match")

        # Check password for being strong
        alert, digit_count, upper_count, lower_count, special_count, len_password = check_strong_password(request.form.get("new_password"))

        # If alert is true then the password is weak
        if alert :
            return  render_template("password.html", alert=alert, digit=digit_count, upper=upper_count, lower=lower_count, special=special_count, length=len_password)

        # Query database to get the hashed password of the user
        user = db.execute("SELECT * FROM users where id = :user_id", user_id=session["user_id"])

        # Check whether the old_password matches database or not
        if not check_password_hash(user[0]['hash'], request.form.get("old_password")) :
            return apology("Current password is not correct")
        else:
            # If matches then update database with the new one
            db_password = generate_password_hash(request.form.get("new_password"))
            db.execute("UPDATE users SET hash= :new_password WHERE id= :user_id", new_password=db_password, user_id=session["user_id"])

        flash("Password Changed!")
        # redirect user to homepage if we want
        return redirect("/")
        # log user out to enter the new password if we want
        # return redirect("/logout")

    return render_template("password.html")

@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Add Deposit"""
    user = db.execute("SELECT * FROM users WHERE id= :user_id", user_id=session['user_id'])
    cash = user[0]['cash']

    if request.method == "POST" :

        if not request.form.get("deposit_amount") :
            return apology("Deposit amount cannot be blank")

        cash = cash + int(request.form.get("deposit_amount"))

        db.execute("UPDATE users SET cash=:new_cash WHERE id= :user_id", new_cash=cash, user_id=session['user_id'])
        db.execute("INSERT INTO transactions (user_id, symbol, amount, value) VALUES(?, ?, ?, ?)",
                    session['user_id'], "$$$$", 1, int(request.form.get("deposit_amount")))

        flash("Cash Deposited!")
        return redirect("/")


    return render_template("deposit.html", cash=cash)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
