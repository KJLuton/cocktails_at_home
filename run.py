import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html", page_title="ABOUT C@H")


@app.route("/cocktails")
def cocktails():
    cocktails = mongo.db.cocktails.find()
    return render_template("cocktails.html",
    cocktails=cocktails, page_title="COCKTAILS")


@app.route("/gin.html")
def gin():
    return render_template("gin.html", page_title="GIN BASED DRINKS")


@app.route("/vodka.html")
def vodka():
    return render_template("vodka.html", page_title="VODKA BASED DRINKS")


@app.route("/rye.html")
def rye():
    return render_template("rye.html", page_title="RYE BASED DRINKS")


@app.route("/register_mybar", methods=["GET", "POST"])
def register_mybar():
    if request.method == "POST":
        # check if username already exists in db 
        existing_user = mongo.db.users.find_one(
            {"emailaddress": request.form.get("emailaddress")})

        if existing_user:
            flash("Email address already exists")
            return redirect(url_for("register_mybar"))

        register_mybar = {
            "firstname": request.form.get("firstname"),
            "lastname": request.form.get("lastname"),
            "emailaddress": request.form.get("emailaddress"),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register_mybar)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("emailaddress")
        flash("Regsitration Successful!")
    return render_template("register_mybar.html", page_title="REGISTER")


@app.route("/login_mybar", methods=["GET", "POST"])
def login_mybar():
    if request.method == "POST":
        # check if email address matches user in DB
        existing_user = mongo.db.users.find_one(
            {"emailaddress": request.form.get("emailaddress")})

        if existing_user: 
            # ensure hashed password matches record in db
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("emailaddress")
                flash("Welcome, {}".format(request.form.get("firstname")))
            else:
                # invalid password match
                flash("Incorrect email address or password provided.\
                    Please try again.")
                return redirect(url_for("login_mybar"))

        else:
            # email address doesn't exist
            flash("Incorrect email address or password provided.\
                Please try again.")
            return redirect(url_for("login_mybar"))

    return render_template("login_mybar.html", page_title="MY BAR LOG IN")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
