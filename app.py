from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from main import app
from db import db
from checkers import *
from courses import *
import secrets

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session["admin"] != "" and session["username"] == "":
            message = myCourses(session["admin"])
            return render_template("index.html",issues=showIssues(), myCourses=message, allCourses=showCourses())   
        if session["admin"] == "" and session["username"] != "":
            message = myCourses(session["username"])
            return render_template("index.html", issues=showIssues(), myCourses=message, allCourses=showCourses())
        
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if logCheck(username, password):
            if adminCheck(username):
                session["admin"] = username
                session["username"] = ""
                session["adminCheck"] = "on"
                session["userCheck"] = "off"
                session["csrf_token"] = secrets.token_hex(20)
                message = myCourses(username)
                return render_template("index.html", issues=showIssues(), myCourses=message, allCourses=showCourses())   
            else:
                session["username"] = username
                session["admin"] = ""
                session["adminCheck"] = "off"
                session["userCheck"] = "on"
                session["csrf_token"] = secrets.token_hex(20)
                message = myCourses(username)
                return render_template("index.html", issues=showIssues(), myCourses=message, allCourses=showCourses())
        else:
            return render_template("index.html", message="\
                Wrong username or password. Please try again.", usrn=username, pswrd=password)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if checkUser(username) == True:
            return render_template("register.html", message=\
                "Your chosen username is already in use. Please choose another username.", 
                usrn=username, pswrd1=password1, pswrd2=password2)
        if len(username) > 30:
            return render_template("register.html", message=\
                "Your chosen username is too long.\ It must be 30 characters at most. Please choose another username.", 
                usrn=username, pswrd1=password1, pswrd2=password2)
        if len(password1) < 8 or len(password1) > 20 or len(password2) < 8 or len(password2) > 20:
            return render_template("register.html", message=\
                "Your chosen password is not in the required lenght. It must be between 8 - 20 characters. Please try again",
                usrn=username, pswrd1=password1, pswrd2=password2)   
        if password1 != password2:
            return render_template("register.html", message=\
                "Passwords are not the same.\n Please try again.", 
                usrn=username, pswrd1=password1, pswrd2=password2)
        if registerId(username, password1):
            return render_template("regConfir.html")
        else:
            return render_template("register.html", )

@app.route("/create", methods=["GET"])
def create():
    if session["adminCheck"] == "on" and session["userCheck"] == "off":
        return render_template("create.html")

@app.route("/createCourse", methods=["GET", "POST"])
def createCourse():
    
    if session["adminCheck"] == "on" and session["userCheck"] == "off":
        if request.method == "GET":
            return render_template("create.html")
        if request.method == "POST":
            courseName = request.form["courseName"]
            startTime = request.form["startTime"]
            endTime = request.form["endTime"]
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            if len (courseName) > 50:
                return render_template("create.html", message="Your given course name is too long. Please choose another name.", 
                                    crsNm=courseName, strTm=startTime, endTm=endTime)
            if checkCourse(courseName):
                return render_template("create.html", message="The course you are trying to create already exists.", 
                    crsNm=courseName, strTm=startTime, endTm=endTime)
            if not checkTime(startTime, endTime):
                print(courseName)
                return render_template("create.html", message="Either your given time of starting or ending or both of them are invalid or does not exist. Please try again", 
                                    crsNm=courseName, strTm=startTime, endTm=endTime)
            else:
                addCourse(courseName, startTime, endTime)
                return render_template("create.html", message="A new course has been created.")

@app.route("/courseReg", methods=["POST"])
def courseReg():
    courses = request.form.getlist("course")
    
    if session["csrf_token"] != request.form["csrf_token"]:
        abort (403)

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
        return render_template("index.html", myCourses=message, allCourses=showCourses())   
    if session["adminCheck"] == "off" and session["userCheck"] == "on":
        message = myCourses(session["username"])
        return render_template("index.html", myCourses=message, allCourses=showCourses())

@app.route("/newIssue", methods=["GET"])
def issue():
        return render_template("newIssue.html")

@app.route("/createIssue", methods=["POST"])
def createIssue():
    if request.method == "POST":
        topic = request.form["topic"]
        issue = request.form["message"]
        
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if session["adminCheck"] == "on" and session["userCheck"] == "off":
            sql = "INSERT INTO issues (username, topic, issue) VALUES (:username, :topic, :issue)"
            db.session.execute(sql, {"username":session["admin"], "topic":topic, "issue":issue})
            db.session.commit()
        if session["adminCheck"] == "off" and session["userCheck"] == "on":
            sql = "INSERT INTO issues (username, topic, issue) VALUES (:username, :topic, :issue)"
            db.session.execute(sql, {"username":session["username"], "topic":topic, "issue":issue})
            db.session.commit()
        if len(topic) > 50:
            return render_template("newIssue.html", message="Your choosen topic is too long. Please try again.", tpc=topic, ise=issue)
        if len(issue) > 1000:
            return render_template("newIssue.html", message="Your written message is too long. Please try again.", tpc=topic, ise=issue)
        else:
            return render_template("newIssue.html", message="New issue has been added.")

@app.route("/logout")
def logout():
    if session["adminCheck"] == "on" and session["userCheck"] == "off":
        del session["admin"]
        del session["csrf_token"]
        return redirect("/")
    if session["adminCheck"] == "off" and session["userCheck"] == "on":
        del session["username"]
        del session["csrf_token"]
        return redirect("/")







