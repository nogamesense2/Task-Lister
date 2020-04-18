from flask import Flask, redirect, render_template, request, session, flash, jsonify
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///task.db")

@app.route("/")
@login_required
def tasks():
    if "todos" not in session:
        session["todos"] = []
    return render_template("tasks.html", todos=session["todos"])

@app.route("/add", methods=["GET","POST"])
@login_required
def add():
    if request.method == "GET":
       return render_template("add.html")
    else:
        todo = request.form.get("task")
        session["todos"].append(todo)
        return redirect("/")

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
        rows = db.execute("SELECT * FROM registrants WHERE username = :username",
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

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    if request.method == "POST":
       if not request.form.get("username"):
           return apology("must provide username", 400)

        # Ensure password was submitted
       elif not request.form.get("password"):
           return apology("must provide password", 400)
       elif not request.form.get("Confirm Password") != request.form.get("password"):
           return apology("password do not match", 400)
       hash = generate_password_hash(request.form.get("password"))
       new_user_id = db.execute("INSERT INTO registrants (username, hash) VALUES(:username, :hash)",
                                 username=request.form.get("username"),
                                 hash=hash)
       if not new_user_id:
            return apology("username taken", 400)

        # Remember which user has logged in
       session["user_id"] = new_user_id

        # Display a flash message
       flash("Registered!")

        # Redirect user to home page
       return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

