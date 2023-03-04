from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, session
from db import db
import re
from datetime import datetime

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

def checkUser(username):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        return True
        
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
    id = db.session.execute(sql, {"user_id":getUser(username), "course_id":course_id})
    messages = id.fetchone()
    if not messages:
        return True
    else:
        return False

def getUser(username):
    sql = ("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    id = result.fetchone()[0]
    return id

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