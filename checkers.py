from main import app
from db import db
import re
from flask import redirect, render_template, request, session
from datetime import datetime

def adminCheck(username):
    sql = "SELECT user_id FROM admins WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        return True

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
