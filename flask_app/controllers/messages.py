from flask import render_template, request, redirect, flash, session
from flask_app import app
from flask_app.models.message import Message
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import os
print( os.environ.get("FLASK_APP_API_KEY") )

# CREATE

@app.route('/create/message', methods=['POST'])
def create_message():
  if 'user_id' not in session:
    return redirect('/logout')
  if not Message.validate_message(request.form):
    return redirect('/dashboard')
  data = { 
    "content": request.form['content'],
    "user_id": request.form['user_id'],
    "recipient_id": request.form['recipient_id'],
  }
  Message.create_message(data) # inserting the message into the database
  return redirect('/dashboard')

@app.route('/user/create/message', methods=['POST'])
def user_create_message():
  if 'user_id' not in session:
    return redirect('/logout')
  if not Message.validate_message(request.form):
    return redirect('/dashboard')
  data = { 
    "content": request.form['content'],
    "user_id": request.form['user_id'],
    "recipient_id": request.form['recipient_id'],
  }
  id = request.form['recipient_id']
  Message.create_message(data) # inserting the message into the database
  return redirect(f'/users/{id}')

# READ

# UPDATE

@app.route('/update/message/<int:id>', methods=['POST'])
def update_message(id):
  print("??????????????????", request.form)
  if 'user_id' not in session:
    return redirect('/logout')
  if not Message.validate_message(request.form):
    return redirect('/dashboard')
  data = { 
    "content": request.form['content'],
    "id": id,
  }
  Message.update(data)
  return redirect('/dashboard')

@app.route('/update/message/form/<int:id>')
def update_message_form(id):
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    "id":id
  }
  user_data = { # this will probably have to be one of the parameters in the variables passed by the render
    "id" : session['user_id']
  }
  return render_template("update_users.html", current_user=User.get_by_id(user_data),
                                        all_messages=Message.get_by_id(data), 
                                        message_count=len(Message.get_by_id(data)),
                                        message=Message.get_one_message(data))

# DELETE

@app.route('/delete/message/<int:id>')
def delete_message(id):
  Message.delete(id)
  return redirect('/dashboard')