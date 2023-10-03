from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# import car.py from model
from flask_app.models import car
# deal with email validation
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app import app
from flask_bcrypt import Bcrypt # deal with password
bcrypt = Bcrypt(app)

class User:
    db_schema_name = "car_deals"
    def __init__(self,data):
    # make instance of a user
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # list cars belong to a user
        self.cars = []

    # @staticmethod for  data validation 
    @staticmethod
    def validate_user_registration(user):
        is_valid = True
        if len(user['first_name']) == 0:
            flash("First name is required")
            is_valid = False
        elif len(user['first_name']) < 3:
            flash("Invalid First name")
            is_valid = False
        if len(user['last_name']) == 0:
            flash("Last name is required")
            is_valid = False
        elif len(user['last_name']) < 3:
            flash("Invalid Last name")
            is_valid = False
        if len(user['email']) == 0:
            flash("Email is required")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address")
            is_valid = False
        if len(user['password']) == 0:
            flash("Password is required")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Password does not match")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_user_login(user):
        is_valid = True
        if len(user['email']) == 0:
                        flash("Email is required")
                        is_valid = False
        elif not EMAIL_REGEX.match(user['email']) and len(user['email']) > 0:
                        flash("Invalid email address")
                        is_valid = False
        if len(user['password']) == 0:
                        flash("Password is required")
                        is_valid = False
        elif len(user['password']) < 8:
                        flash("Password has to has at least 8 characters")
                        is_valid = False
        return is_valid

    # @classmethod for data processing (CRUD)
    # Create
    @classmethod
    def save_user(cls, user_data):
        query = """
        INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());
        """
        print(f"[ Create A User - {user_data} ]")
        return connectToMySQL(cls.db_schema_name).query_db(query,user_data)
    
    # Read
    @classmethod
    def read_all_users(cls):
        query = """
        SELECT * FROM users;
        """
        group_of_users = connectToMySQL(cls.db_schema_name).query_db(query)
        print("[ Read All User ]")
        all_users = []
        for each_user in group_of_users:
            all_users.append(cls(each_user))
        return all_users

    @classmethod
    def read_one_user(cls,user_id):
        query = """
        SELECT * FROM users WHERE id = %(id)s;
    """
        user_data = {
            "id":user_id
        }
        the_user = connectToMySQL(cls.db_schema_name).query_db(query,user_data)
        print("[ Read One User ]")
        return cls(the_user[0])
    
    @classmethod
    def get_by_user_email(cls,user_data):
        query = """
        SELECT * FROM users WHERE email = %(email)s;
        """
        the_user = connectToMySQL(cls.db_schema_name).query_db(query,user_data)

        # didn't find matching user
        if len(the_user) < 1:
            return False
        print("[ Get User By Email ]")
        return cls(the_user[0])
    
    # Update
    # Delete