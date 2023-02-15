from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from main import app
from db import db
from admin import *
from user import *

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session["admin"] != "":
                message = myCourses(session["admin"])
                if len(message) == 0:
                    return render_template("index.html", message="\
                        It looks like you have not seleceted any courses yet.", allCourses=showCourses())
                else:
                    return render_template("index.html", myCourses=message, allCourses=showCourses())   
        else:
            message = myCourses(session["username"])
            if len(message) == 0:
                return render_template("index.html", message="\
                    It looks like you have not seleceted any courses yet.", allCourses=showCourses())
            else:
                return render_template("index.html", myCourses=message, allCourses=showCourses())
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username) == 0 or len(password) == 0:
            return render_template("index.html")
        if logcheck(username, password):
            if adminCheck(username):
                session["admin"] = username
                message = myCourses(username)
                if len(message) == 0:
                    return render_template("index.html", message="\
                        It looks like you have not seleceted any courses yet.", allCourses=showCourses())
                else:
                    return render_template("index.html", myCourses=message, allCourses=showCourses())   
            else:
                session["username"] = username
                message = myCourses(username)
                if len(message) == 0:
                    return render_template("index.html", message="\
                        It looks like you have not seleceted any courses yet.", allCourses=showCourses())
                else:
                    return render_template("index.html", myCourses=message, allCourses=showCourses())
        else:
            return render_template("index.html", message="\
                Wrong username or password. Please try again.")

def logcheck(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if len(username) == 0 or len(password1) == 0 or len(password2) == 0:
            return render_template("register.html")
        if checkUser(username) == True:
            return render_template("register.html", message=\
                "Your chosen username is already in use. Please choose another username.")
        if len(username) > 30:
            return render_template("register.html", message=\
                "Your chosen username is too long. It must be 30 characters at most. Please choose another username.")
        if len(password1) < 8 or len(password1) > 20 or len(password2) < 8 or len(password2) > 20:
            return render_template("register.html", message=\
                "Your chosen password is not in the required lenght. It must be between 8 - 20 characters. Please try again")   
        if password1 != password2:
            return render_template("register.html", message=\
                "Passwords are not the same.\n Please try again.")
        if registerId(username, password1):
            return render_template("regConfir.html")
        else:
            return render_template("register.html", )

def registerId(username, password):
        if request.method == "POST":
            hash_value = generate_password_hash(password)
            try:
                sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
                db.session.execute(sql, {"username":username, "password":hash_value})
                db.session.commit()
            except:
                return False
            return index()

@app.route("/")
def showCourses():
    sql = "SELECT courses.name, courses.time FROM courses"
    db.session.execute(sql)
    result = db.session.execute(sql)
    messages = result.fetchall()
    return messages

@app.route("/")
def myCourses(username):
    sql = "SELECT courses.name, courses.time FROM courses, participants\
     WHERE participants.course_id = courses.id AND participants.user_id=:user_id"
    result = db.session.execute(sql, {"user_id":getUser(username)})
    messages = result.fetchall()
    return messages


