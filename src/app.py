## Import libraries
from flask import Flask, render_template

## Create the flask application
app = Flask(__name__) #'__main__'

## Setup the endpoint
@app.route('/') # www.mysite.com/api/ - Empty endpoint that will run the below

## Basic function to execute when calling the api
def hello_method():
    return render_template('login.html')

## If we are in main, execute the program
if __name__ == '__main__':
    app.run()