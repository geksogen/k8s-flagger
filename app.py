from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
   return "hello :)"

@app.route('/return')
def return_app_version():
    return "version 866"