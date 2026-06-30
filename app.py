from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "stylesync_secret_key"

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("stylesync.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()
        if user:
            session["email"] = email
            return redirect("/recommendation")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("stylesync.db")
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            conn.close()
            return "Email already registered. Please login or use another email."

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")
@app.route("/recommendation", methods=["GET", "POST"])
def recommendation():

    outfit = ""

    if request.method == "POST":

        weather = request.form["weather"]
        gender = request.form["gender"]
        occasion = request.form["occasion"]
        color = request.form["color"]

        if gender == "Female":

            if weather == "Hot" and occasion == "College":
                outfit = f"{color} Top + Blue Jeans + White Sneakers"

            elif weather == "Cold":
                outfit = f"{color} Jacket + Black Jeans + Boots"

            elif occasion == "Party":
                outfit = f"{color} Party Dress + Heels + Handbag"

            elif occasion == "Wedding":
                outfit = f"{color} Traditional Outfit + Jewellery"

            else:
                outfit = f"{color} Casual Outfit"

        else:

            if weather == "Hot" and occasion == "College":
                outfit = f"{color} T-Shirt + Jeans + Sneakers"

            elif weather == "Cold":
                outfit = f"{color} Hoodie + Trousers + Shoes"

            elif occasion == "Party":
                outfit = f"{color} Blazer + Formal Shoes"

            elif occasion == "Wedding":
                outfit = f"{color} Sherwani + Mojari"

            else:
                outfit = f"{color} Casual Outfit"

    return render_template("recommendation.html", outfit=outfit)
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")
@app.route("/wardrobe", methods=["GET", "POST"])
def wardrobe():

    conn = sqlite3.connect("stylesync.db")
    cursor = conn.cursor()

    if request.method == "POST":

        category = request.form["category"]
        item_name = request.form["item_name"]

        cursor.execute(
            "INSERT INTO wardrobe(category, item_name) VALUES (?, ?)",
            (category, item_name)
        )

        conn.commit()

    cursor.execute("SELECT * FROM wardrobe")
    items = cursor.fetchall()

    conn.close()

    return render_template("wardrobe.html", items=items)
@app.route("/profile")
def profile():

    conn = sqlite3.connect("stylesync.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username, email FROM users ORDER BY id DESC LIMIT 1")
    user = cursor.fetchone()

    conn.close()

    if user:
        return render_template(
            "profile.html",
            username=user[0],
            email=user[1]
        )

    return redirect("/login")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
