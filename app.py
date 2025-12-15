from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, UserMixin
)

from model import predict_stock_price
from db import init_db
import sqlite3

# -----------------------------
# App Setup
# -----------------------------
app = Flask(__name__)
app.secret_key = "super-secret-key"

init_db()

# -----------------------------
# Login Manager
# -----------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# -----------------------------
# User Model
# -----------------------------
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("predictions.db")
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()

    if row:
        return User(row[0], row[1])
    return None

# -----------------------------
# NSE Stocks
# -----------------------------
NSE_STOCKS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "SBIN.NS", "ITC.NS", "LT.NS"
]

# -----------------------------
# Home Route (Protected)
# -----------------------------
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    current_price = forecast = chart = forecast_chart = error = None
    symbol = ""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        (
            current_price,
            forecast,
            chart,
            forecast_chart,
            error
        ) = predict_stock_price(symbol)

    return render_template(
        "index.html",
        stocks=NSE_STOCKS,
        symbol=symbol,
        current_price=current_price,
        forecast=forecast,
        chart=chart,
        forecast_chart=forecast_chart,
        error=error
    )

# -----------------------------
# Login Route
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("predictions.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            login_user(User(user[0], user[1]))
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials")

    return render_template("login.html")

# -----------------------------
# Logout Route
# -----------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
