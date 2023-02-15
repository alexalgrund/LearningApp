from main import app
from db import db
from flask import redirect, render_template, request, session

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