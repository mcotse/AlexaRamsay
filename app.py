from flask import Flask, jsonify, request, render_template, send_from_directory, abort
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from db.models import *

engine = sa.create_engine(
    'mysql+mysqldb://ramsay:ramsay123@ramsay.cn8pndyiytrv.us-east-1.rds.amazonaws.com:3306/Ramsay?charset=utf8')
Session = sessionmaker(bind=engine, autoflush=True)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
