#Import the flask dependency
from flask import Flask

#Create an instamce using the magic method
app = Flask(__name__)

#Create the first route aka root
@app.route('/')

#Create a function 'hello world'
def hello_world():
        return 'Hello world'