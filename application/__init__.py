from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@34.89.52.54/support_ticket'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

from application import routes