from db import *
from checkers import *

def addCourse(courseName, startTime, endTime ):
    startSplit = startTime.split(".")
    endSplit = endTime.split(".")
    time = f"{int(startSplit[0]):01}.{int(startSplit[1]):01}.{startSplit[2]}\
    - {int(endSplit[0]):01}.{int(endSplit[1]):01}.{endSplit[2]}"
    sql = "INSERT INTO courses (name, time) VALUES (:name, :time)"
    db.session.execute(sql, {"name":courseName, "time":time})
    db.session.commit()
    return True

def showCourses():
    sql = "SELECT courses.id, courses.name, courses.time FROM courses"
    db.session.execute(sql)
    result = db.session.execute(sql)
    messages = result.fetchall()
    return messages

def myCourses(username):
    sql = "SELECT courses.name, courses.time FROM courses, participants\
     WHERE participants.course_id = courses.id AND participants.user_id=:user_id"
    result = db.session.execute(sql, {"user_id":getUser(username)})
    messages = result.fetchall()
    return messages

def showIssues():
    sql = "SELECT username, issues.topic, issues.issue\
          FROM issues"
    db.session.execute(sql)
    result = db.session.execute(sql)
    messages = result.fetchall()
    return messages

def registerId(username, password):
        if request.method == "POST":
            hash_value = generate_password_hash(password)
            try:
                sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
                db.session.execute(sql, {"username":username, "password":hash_value})
                db.session.commit()
            except:
                return False
            return True