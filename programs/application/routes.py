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
        fix = Fix(status=status, ticket_id=ticket_id)
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

@app.route('/deleteuser', methods=["GET", "POST"])
def deleteuser():
    issue= request.form.get("issue")
    user= request.form.get("user")
    ticket = Ticket.query.filter_by(issue=issue, user=user).first()
    db.session.delete(ticket)
    db.session.commit()
    return redirect("/user")

@app.route('/deletetech', methods=["GET", "POST"])
def deletetech():
    ticket_id=request.form.get("ticket_id")
    status=request.form.get("status")
    fix = Fix.query.filter_by(ticket_id=ticket_id, status=status).first()
    db.session.delete(fix)
    db.session.commit()
    return redirect("/tech")