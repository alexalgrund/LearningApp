from main import *
from flask import redirect, render_template, request, session
from db import db

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

@main.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

