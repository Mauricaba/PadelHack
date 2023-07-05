from flask import Flask , render_template, request

import os

app = Flask(__name__)

@app.route('/')
def landing_page():
  return render_template('landing_page.html')

@app.route('/home')
def home():
  return render_template('homepage.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/register')
def register():
  return render_template('register.html')

@app.route('/dashboard')
def dashboard():
  return render_template('dashboard.html')


if __name__ == '__main__':
  app.run(host='127.0.0.1', port= 8000, debug = True)