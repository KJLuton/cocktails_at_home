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
    cocktails = mongo.db.cocktails.find()
    return render_template("index.html", cocktails=cocktails)


@app.route("/cocktails")
def cocktails():
    cocktails = mongo.db.cocktails.find()
    return render_template(
        "cocktails.html", cocktails=cocktails, page_title="ALL COCKTAILS")


@app.route("/search", methods=["GET", "POST"])
def search():
    search = request.form.get("search")
    cocktails = mongo.db.cocktails.find({"$text": {"$search": search}})
    return render_template(
        "cocktails.html", cocktails=cocktails)


@app.route("/cocktails/<cocktail_id>")
def single_cocktail(cocktail_id):
    cocktails = mongo.db.cocktails.find(
    mongo.db.cocktails.find_one({"_id": ObjectId(cocktail_id)}))
    return render_template(
    "single_cocktail.html", cocktails=cocktails)


# create new bar / registration
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
        return redirect(url_for("mybar", emailaddress=session["user"]))

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
                return redirect(url_for(
                    "mybar", emailaddress=session["user"]))
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


@app.route("/mybar/<emailaddress>", methods=["GET", "POST"])
def mybar(emailaddress):
    # Grab the session users first name from the database
    emailaddress = mongo.db.users.find_one(
        {"emailaddress": session["user"]})["emailaddress"]

    if session["user"]:
        cocktails = mongo.db.cocktails.find()
        return render_template(
            "mybar.html", emailaddress=emailaddress,
            cocktails=cocktails, page_title="MY BAR")

    return redirect(url_for("login_mybar"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login_mybar"))


@app.route("/add_cocktail", methods=["GET", "POST"])
def add_cocktail():
    if session["user"]:
        # if session user exists, show form to add new cocktail to mongodb
        if request.method == "POST":
            cocktail = {
                "cocktail_name": request.form.get("cocktail_name"),
                "cocktail_description":
                request.form.get("cocktail_description"),
                "cocktail_category":
                request.form.getlist("cocktail_category"),
                "cocktail_ingredients":
                request.form.getlist("cocktail_ingredients"),
                "image_url": request.form.get("image_url"),
                "created_by": session["user"]
            }
            mongo.db.cocktails.insert_one(cocktail)
            flash("Cocktail added")
            return redirect(url_for("cocktails"))

    return render_template(
        "add_cocktail.html", page_title="ADD A NEW COCKTAIL")


@app.route("/edit_cocktail/<cocktail_id>", methods=["GET", "POST"])
def edit_cocktail(cocktail_id):
    if request.method == "POST":
        submit = {
            "cocktail_name": request.form.get("cocktail_name"),
            "cocktail_description": request.form.get("cocktail_description"),
            "cocktail_category": request.form.getlist("cocktail_category"),
            "cocktail_ingredients":
                request.form.getlist("cocktail_ingredients"),
            "image_url": request.form.get("image_url"),
            "created_by": session["user"]
        }
        mongo.db.cocktails.update_many(
            {"_id": ObjectId(cocktail_id)}, {"$set": submit})
        flash("Cocktail Updated")

    cocktail = mongo.db.cocktails.find_one({"_id": ObjectId(cocktail_id)})
    return render_template("edit_cocktail.html", cocktail=cocktail)


@app.route("/delete_cocktail/<cocktail_id>")
def delete_cocktail(cocktail_id):
    mongo.db.cocktails.delete_one({"_id": ObjectId(cocktail_id)})
    flash("Cocktail successfully deleted")
    return redirect(url_for("cocktails"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
