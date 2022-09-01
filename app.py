from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
   return "hello :)"

@app.route('/return_version')
def return_app_version():
    return "version 3.0"