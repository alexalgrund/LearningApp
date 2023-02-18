from main import app
from db import db
from checkers import *
import re
from flask import redirect, render_template, request, session
from datetime import datetime


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

@app.route("/adminLogout")
def adminLogout():
    del session["admin"]
    return redirect("/")

