import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import *

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
app.jinja_env.globals.update(usd=usd, lookup=lookup, int=int)

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
    # Get user cash
    cash = db.execute("SELECT cash FROM users WHERE id=:id",
                        id=session['user_id']
                        )[0]['cash']
    total = cash

    # Get user portfolio
    stocks = db.execute("SELECT stock, shares FROM portfolio WHERE user_id=:id",
                            id=session['user_id']
                            )
    if not stocks:
        return render_template("noHoldings.html")

    # Get information for table
    for stock in stocks:
        price = lookup(stock['stock'])['price']
        stockTotal = price * stock['shares']
        stock.update({'price': price, 'stockTotal': stockTotal})
        total += stockTotal

    return render_template("index.html", stocks=stocks, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "POST":

        symbol = request.form.get("symbol")
        nShares = int(request.form.get("amount"))

        if not symbol or not nShares:
            return apology("Please enter a share symbol and number of shares!")

        elif nShares <= 0:
            return apology("Please specify a positive value for shares!")

        stock = lookup(symbol)
        if stock is None:
            return apology("Please enter a valid stock symbol!")

        else:
            # Get user cash
            userCash = db.execute("SELECT cash FROM users WHERE id = :id",
                        id = session['user_id']
                        )[0]['cash']

            # Calculate cost of purchase
            cost = float(stock['price'] * nShares)

            # Check if user can afford
            if cost > float(userCash):
                return apology("You do not have enough cash for this transaction")

            # Deduct user cash
            db.execute("UPDATE users SET cash=cash-:cost WHERE id=:id",
                        cost=cost,
                        id=session["user_id"])

            # Add record of transaction
            add_transaction = db.execute("INSERT INTO transactions (user_id, symbol, shares, price, transacted, Type) VALUES (:user_id, :symbol, :shares, :price, :transacted, :tType)",
                                user_id=session["user_id"],
                                symbol=stock["symbol"],
                                shares=nShares,
                                price=stock['price'],
                                transacted=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                tType="buy")

            # Check if in portfolio already
            currentlyInPortfolio = db.execute("SELECT shares FROM portfolio WHERE stock=:stock AND user_id=:user_id",
                                    stock=stock["symbol"],
                                    user_id=session["user_id"])

            if not currentlyInPortfolio:
                db.execute("INSERT INTO portfolio (user_id, stock, shares, value) VALUES (:user_id, :stock, :shares, :value)",
                            user_id=session["user_id"],
                            stock=stock["symbol"],
                            shares=nShares,
                            value=float(stock['price'] * nShares))

            else:
                currentAmount = currentlyInPortfolio[0]['shares']
                currentValue = float(db.execute("SELECT value FROM portfolio WHERE stock=:stock AND user_id=:user_id",
                                stock=stock["symbol"],
                                user_id=session["user_id"])[0]['value'])

                db.execute("UPDATE portfolio SET shares=:shares, value=:value WHERE stock=:stock AND user_id=:user_id",
                            shares=currentAmount+nShares,
                            stock=stock["symbol"],
                            user_id=session["user_id"],
                            value=currentValue+cost)

            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Get transactions
    transactions = db.execute("SELECT symbol, shares, price, transacted, Type FROM transactions WHERE user_id=:id",
                            id=session['user_id']
                            )
    if not transactions:
        return apology("You haven't made any transactions yet!")

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

        # Redirect user to home page
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

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("No share found for this symbol!")

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    """Register user"""
    session.clear()

    if request.method == "POST":
        # Return apology if input blank or name already exists
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 403)

        # INSERT new user into users, storing hash of password
        password_hash = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT into users (username, hash) VALUES (:username, :hash)",
                                  username=request.form.get("username"), hash=password_hash)

        # Check username is unique
        if not new_user_id:
            return apology("Username already exists", 403)

        session["user_id"] = new_user_id
        return redirect("/")


    elif request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        nShares = int(request.form.get("shares"))

        # Validate input
        if not symbol or not nShares:
            return apology("Please specify a stock and amount to sell.")

        if nShares <= 0:
            return apology("Please specify a positive integer amount of shares.")

        # Ensure user has enough of stock to sell
        amountOwned = db.execute("SELECT shares FROM portfolio WHERE user_id=:id AND stock=:stock",
                            id=session['user_id'],
                            stock=symbol)[0]['shares']

        if nShares > amountOwned:
            return apology("You don't have enough of that stock to sell.")

        # Remove from portfolio
        stock = lookup(symbol)
        currentValue = float(db.execute("SELECT value FROM portfolio WHERE stock=:stock AND user_id=:user_id",
                                stock=stock["symbol"],
                                user_id=session["user_id"])[0]['value'])
        saleCost = float(stock['price'] * nShares)

        db.execute("UPDATE portfolio SET shares=:shares, value=:value WHERE stock=:stock AND user_id=:user_id",
                            shares=amountOwned-nShares,
                            stock=stock["symbol"],
                            user_id=session["user_id"],
                            value=currentValue-saleCost)

        # Add to cash
        db.execute("UPDATE users SET cash=cash+:saleCost WHERE id=:id",
                        saleCost=saleCost,
                        id=session["user_id"])

        # Log transaction
        add_transaction = db.execute("INSERT INTO transactions (user_id, symbol, shares, price, transacted, Type) VALUES (:user_id, :symbol, :shares, :price, :transacted, :tType)",
                                user_id=session["user_id"],
                                symbol=stock["symbol"],
                                shares=nShares,
                                price=stock['price'],
                                transacted=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                tType="sell")

        return redirect("/")

    else:
        # Render sell template
        stocks = db.execute("SELECT stock FROM portfolio WHERE user_id=:id",
                            id=session['user_id'])

        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
