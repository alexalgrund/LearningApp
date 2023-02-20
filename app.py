from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from main import app
import re
from db import db

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
        if logCheck(username, password):
            if adminCheck(username):
                session["admin"] = username
                session["adminCheck"] = "on"
                session["userCheck"] = "off"
                message = myCourses(username)
                if len(message) == 0:
                    return render_template("index.html", message="\
                        It looks like you have not seleceted any courses yet.", allCourses=showCourses())
                else:
                    return render_template("index.html", myCourses=message, allCourses=showCourses())   
            else:
                session["username"] = username
                session["adminCheck"] = "off"
                session["userCheck"] = "on"
                message = myCourses(username)
                if len(message) == 0:
                    return render_template("index.html", message="\
                        It looks like you have not seleceted any courses yet.", allCourses=showCourses())
                else:
                    return render_template("index.html", myCourses=message, allCourses=showCourses())
        else:
            return render_template("index.html", message="\
                Wrong username or password. Please try again.")



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

@app.route("/courseReg", methods=["POST"])
def courseReg():
    courses = request.form.getlist("course")
    for id in courses:
        if session["adminCheck"] == "on" and session["userCheck"] == "off" and checkParticipant(session["admin"], id):
                sql = "INSERT INTO participants (user_id, course_id) VALUES (:user_id, :course_id)"
                db.session.execute(sql, {"user_id":getUser(session["admin"]), "course_id":id})
                db.session.commit()
        if session["adminCheck"] == "off" and session["userCheck"] == "on" and checkParticipant(session["username"], id):
                sql = "INSERT INTO participants (user_id, course_id) VALUES (:user_id, :course_id)"
                db.session.execute(sql, {"user_id":getUser(session["username"]), "course_id":id})
                db.session.commit()

    if session["adminCheck"] == "on" and session["userCheck"] == "off":
                message = myCourses(session["admin"])
                if len(message) == 0:
                    return render_template("index.html", message="\
                        It looks like you have not seleceted any courses yet.", allCourses=showCourses())
                else:
                    return render_template("index.html", myCourses=message, allCourses=showCourses())   
    if session["adminCheck"] == "off" and session["userCheck"] == "on":
        message = myCourses(session["username"])
        if len(message) == 0:
            return render_template("index.html", message="\
                It looks like you have not seleceted any courses yet.", allCourses=showCourses())
        else:
            return render_template("index.html", myCourses=message, allCourses=showCourses())


def logCheck(username, password):
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

def adminCheck(username):
    sql = "SELECT user_id FROM admins WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        return True

def checkParticipant(username, course_id):
    sql = "SELECT user_id FROM participants WHERE participants.user_id=:user_id AND\
        participants.course_id=:course_id"
    id = db.session.execute(sql, {"user_id":getUser(username), "course_id":int(course_id)})
    messages = id.fetchone()
    if not messages:
        return True
    else:
        return False

def checkCourse(courseName):
    sql = "SELECT id FROM courses WHERE name=:name"
    result = db.session.execute(sql, {"name":courseName})
    course = result.fetchone()
    if not course:
        return False
    else:
        return True

def checkTime(startTime, endTime):
    if not re.search("^[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{4}$", startTime) or not re.search("^[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{4}$", endTime):
        return False
    else:
        try:
            startSplit = startTime.split(".")
            dateTime = datetime(int(startSplit[2]), int(startSplit[1]), int(startSplit[0]))
            endSplit = endTime.split(".")
            dateTime = datetime(int(endSplit[2]), int(endSplit[1]), int(endSplit[0]))
        except:
            return False
        return True


@app.route("/create", methods=["GET"])
def create():
    if session["adminCheck"] == "on" and session["userCheck"] == "off":
        return render_template("create.html")

@app.route("/createCourse", methods=["GET", "POST"])
def createCourse():
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        courseName = request.form["courseName"]
        startTime = request.form["startTime"]
        endTime = request.form["endTime"]
        print(endTime)
        if len(courseName) == 0 or len(startTime) == 0 or len(endTime) == 0:
            return render_template("create.html")
        if len (courseName) > 50:
            return render_template("create.html", message="Your given course name is too long.\
                                   Please choose another name.")
        if checkCourse(courseName):
            return render_template("create.html", message="The course you are trying to create\
                already exists.")
        if not checkTime(startTime, endTime):
            return render_template("create.html", message="Either your given time of starting or ending or both of them\
                                   are invalid or does not exist. Please try again")
        else:
            addCourse(courseName, startTime, endTime)
            return render_template("create.html", message="A new course has been created.")

def addCourse(courseName, startTime, endTime ):
    startSplit = startTime.split(".")
    endSplit = endTime.split(".")
    time = f"{int(startSplit[0]):01}.{int(startSplit[1]):01}.{startSplit[2]}\
    - {int(endSplit[0]):01}.{int(endSplit[1]):01}.{endSplit[2]}"
    sql = "INSERT INTO courses (name, time) VALUES (:name, :time)"
    db.session.execute(sql, {"name":courseName, "time":time})
    db.session.commit()
    return True

@app.route("/")
def showCourses():
    sql = "SELECT courses.id, courses.name, courses.time FROM courses"
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

@app.route("/adminLogout")
def adminLogout():
    del session["admin"]
    return redirect("/")

def checkUser(username):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        return True

def getUser(username):
    sql = ("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    id = result.fetchone()[0]
    return id

@app.route("/userLogout")
def userLogout():
    del session["username"]
    return redirect("/")





