from main import app
from db import db
import re
from flask import redirect, render_template, request, session
from datetime import datetime


@app.route("/create", methods=["GET"])
def create():
    if session["admin"] != "":
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
        if checkCourse(courseName):
            return render_template("create.html", message="The course you are trying to create\
                already exists.")
        if not checkTime(startTime, endTime):
            return render_template("create.html", message="Either your given time of starting or ending or both of them\
                                   are invalid or does not exist. Please try again")
        else:
            addCourse(courseName, startTime, endTime)
            return render_template("create.html", message="A new course has been created.")


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

def adminCheck(username):
    sql = "SELECT user_id FROM admins WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        return True

def addCourse(courseName, startTime, endTime ):
    startSplit = startTime.split(".")
    endSplit = endTime.split(".")
    time = f"{int(startSplit[0]):02}.{int(startSplit[1]):02}.{startSplit[2]}\
    - {int(endSplit[0]):02}.{int(endSplit[1]):02}.{endSplit[2]}"
    sql = "INSERT INTO courses (name, time) VALUES (:name, :time)"
    db.session.execute(sql, {"name":courseName, "time":time})
    db.session.commit()
    return True

def checkCourse(courseName):
    sql = "SELECT id FROM courses WHERE name=:name"
    result = db.session.execute(sql, {"name":courseName})
    course = result.fetchone()
    if not course:
        return False
    else:
        return True

@app.route("/adminLogout")
def adminLogout():
    del session["admin"]
    return redirect("/")