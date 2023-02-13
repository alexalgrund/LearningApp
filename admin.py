from main import app
from db import db
from flask import redirect, render_template, request, session


def adminCheck(username):
    sql = "SELECT user_id FROM admins WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        return True

@app.route("/adminLogout")
def adminLogout():
    del session["admin"]
    return redirect("/")