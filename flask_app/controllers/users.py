from flask import render_template,request, redirect, flash, session, jsonify
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import os, requests
print( os.environ.get("FLASK_APP_API_KEY") )

# CREATE

@app.route('/register', methods=['POST'])
def create():
  if not User.validate_user(request.form):
    return redirect('/')
  data ={ 
    "first_name": request.form['first_name'],
    "last_name": request.form['last_name'],
    "email": request.form['email'],
    "password": bcrypt.generate_password_hash(request.form['password'])
  }
  id = User.save(data)
  session['user_id'] = id 
  return redirect('/dashboard')

# READ

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/dashboard')
def show_info():
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    'id': session['user_id']
  }
  return render_template('dashboard.html', current_user=User.get_by_id(data), 
                                        all_users=User.get_all(), 
                                        all_messages=Message.get_by_id(data), 
                                        message_count=len(Message.get_by_id(data)), 
                                        user=User.get_by_id(data))

@app.route('/login',methods=['POST'])
def login():
  user = User.get_by_email(request.form)

  if not user:
    flash("Invalid Email", 'login')
    return redirect('/')

  if not bcrypt.check_password_hash(user.password, request.form['password']):
    flash("Invalid Password", 'login')
    return redirect('/')

  session['user_id'] = user.id
  return redirect('/dashboard')

@app.route('/users/<int:id>')
def show_one_user(id):
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    "id":id
  }
  user_data = {
    'id': session['user_id']
  }
  return render_template('users.html', current_user=User.get_by_id(user_data), all_messages=Message.get_by_id(user_data), user=User.get_by_id(data), messages=Message.get_all())

# UPDATE

# DELETE

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')

# json

@app.route('/searching')
def search():
  r = requests.get(f"https:api.information.com/{os.environ.get('FLASK_API_KEY')}")
  # we must keep in line with JSON format.
  # requests has a method to convert the data coming back into JSON.
  return jsonify( r.json() )