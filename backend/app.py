from flask import Flask
from flask_cors import CORS, cross_origin
from datetime import timedelta

UPLOAD_FOLDER='C:/uploads'

app=Flask(__name__)
app.secret_key="tatenda musodza"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']=16*1024*1024
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(minutes=10)
CORS(app)