from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
  db = 'wall_schema'
  def __init__(self,data):
    self.id = data['id']
    self.first_name = data['first_name']
    self.last_name = data['last_name']
    self.email = data['email']
    self.password = data['password']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.tweets = []

  @classmethod
  def save(cls,data):
    query = """
    INSERT INTO users (first_name,last_name,email,password) 
    VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);
    """
    return connectToMySQL(cls.db).query_db(query,data)

  @classmethod
  def get_all(cls):
    query = "SELECT * FROM users"
    result = connectToMySQL(cls.db).query_db(query)
    emails = []
    for row in result:
      emails.append(cls(row))
    return result

  @classmethod
  def get_by_email(cls, data):
    query = "SELECT * FROM users WHERE email = %(email)s;"
    results = connectToMySQL(cls.db).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])

  @classmethod
  def get_by_id(cls,data):
    query = "SELECT * FROM users WHERE id = %(id)s;"
    results = connectToMySQL(cls.db).query_db(query,data)
    print(results[0])
    return cls(results[0])

  @classmethod
  def get_name_by_id(cls,data):
    data = {
      "id" : data
    }
    query = "SELECT * FROM users WHERE id = %(id)s;"
    results = connectToMySQL(cls.db).query_db(query,data)
    return cls(results[0]).first_name


  @classmethod
  def get_all_messages_with_creator(cls):
    query = "SELECT * FROM messages JOIN users ON messages.user_id = users.id;"
    results = connectToMySQL(cls.db).query_db(query)
    all_tweets = []
    for row in results:
      one_tweet = cls(row)
      one_tweets_author_info = {
        "id": row['users.id'], 
        "first_name": row['first_name'],
        "last_name": row['last_name'],
        "email": row['email'],
        "password": row['password'],
        "created_at": row['users.created_at'],
        "updated_at": row['users.updated_at']
      }
      author = User(one_tweets_author_info)
      # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
      one_tweet.creator = author
      # Append the Tweet containing the associated User to your list of tweets
      all_tweets.append(one_tweet)
    return all_tweets
  
  @classmethod
  def message_number(cls, data):
    data = {
      "id" : data
    }
    query = "UPDATE users SET sent_messages=sent_messages + 1 WHERE id = %(id)s;"
    results = connectToMySQL(cls.db).query_db(query,data)
    return cls(results[0])

  @staticmethod
  def validate_user( user ):
    is_valid = True
    
    if len(user['first_name']) < 3:
      flash("First Name must be longer than 3 letters!", 'register')
      is_valid = False
    
    if len(user['last_name']) < 3:
      flash("Last Name must be longer than 3 letters!", 'register')
      is_valid = False
    
    if not EMAIL_REGEX.match(user['email']):
      flash("Email cannot be blank!", 'register')
      is_valid = False
    
    if len(user['password']) < 8:
      flash("Password must be 8 characters long, contain special characters, and match confirmation", 'register')
      is_valid = False
    
    if user['password'] != user['password_confirm']:
      flash ("Confirm Password does not match Password", 'register')
      is_valid = False
    
    # if user['email'] != user['email']:
    #   flash ("Use another email", 'register')
    #   is_valid = False

    return is_valid