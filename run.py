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
            "emailaddress": request.form.get("emailaddress"),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register_mybar)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("emailaddress")
        flash("Regsitration Successful!")
    return render_template("register_mybar.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
