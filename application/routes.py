from application import app, db
from application.models import Ticket, Fix
from flask import render_template, request, redirect

@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/user', methods=["GET", "POST"])
def user():
    tickets= ""
    tickets=Ticket.query.all()
    if request.form:
        user = request.form['user']
        issue = request.form['issue']
        ticket = Ticket(user=user, issue=issue)
        db.session.add(ticket)
        db.session.commit()
        tickets = Ticket.query.all()
    return render_template("user.html", tickets=tickets)
    


@app.route('/tech', methods=["GET", "POST"])
def tech():
    fixes = ""
    fixes=Fix.query.all()
    if request.form:
        ticket_id=request.form['ticket_id']
        status=request.form['status']
        fix = Fix(ticket_id=ticket_id, status=status)
        db.session.add(fix)
        db.session.commit()
        fixes = Fix.query.all()
    return render_template("tech.html", fixes=fixes)


@app.route('/updateuser', methods=["GET", "POST"])
def updateuser():
    newissue=request.form.get("newissue")
    oldissue=request.form.get("oldissue")
    issue=Ticket.query.filter_by(issue=oldissue).first()
    issue.issue=newissue
    db.session.commit()
    return redirect("/user")

@app.route('/updatetech', methods=["GET", "POST"])
def updatetech():
    newstatus=request.form.get("newstatus")
    oldstatus=request.form.get("oldstatus")
    status=Fix.query.filter_by(status=oldstatus).first()
    status.status=newstatus
    db.session.commit()
    return redirect("/tech")