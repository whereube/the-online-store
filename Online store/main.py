from flask import Flask, redirect, render_template, request, flash, session, g
from db import *
import uuid

app = Flask(__name__, static_url_path='/static')
app.run(debug=True)
app.config['SECRET_KEY'] = 'thisissecret'
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def start():
    categories = get_categories_from_db()
    for row in categories:
        headline = row[1]

    articles = get_articles_from_db()
    return render_template("index.html", articles=articles, categories=categories, headline=headline)

@app.route("/login", methods=['POST', 'GET'])
def login_form():
    if request.method == 'POST':
        user_email = request.form.get("user_email")
        user_password = request.form.get("user_password")
        current_user = user_in_db(user_email, user_password)
        if current_user == False:
            flash("Felaktigt e-postadress eller lösenord.")
            return render_template("login.html")
        else:
            for item in current_user:
                user_id = item[0]
                user_name = item[1]
                session["USER_ID"] = user_id
                session['USER_NAME'] = user_name
                return redirect("/")
    else:                
        return render_template("login.html")

    return render_template("login.html")

@app.route("/create_profile", methods=['POST', 'GET'])
def create_profile_form():
    user_name =request.form.get("user_name")
    user_email = request.form.get("user_email")
    user_password = request.form.get("user_password")
    
    if request.method == 'POST':
        create_profile_in_db(user_name, user_email, user_password)
        flash("Success!")
        return redirect("/login")
        

    return render_template("create_profile.html")

@app.route("/article/<article_id>")
def show_article(article_id):
    articles = get_articles_from_db()


    for row in articles:
        if row[0] == article_id:
            headline = row[1]
            description = row[2]
            price = row[3]
    return render_template("/article.html", headline=headline, description=description, price=price)