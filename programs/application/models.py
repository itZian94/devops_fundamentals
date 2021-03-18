from application import db

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column('user', db.String(30), nullable=False)
    issue = db.Column('issue', db.String(80), nullable=False)
    fixes = db.relationship('Fix', backref='fixes')

class Fix(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(30), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'),nullable=False)