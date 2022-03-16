#import the function that will return an instance of a connection
from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash, session

#model the class after the friend table from our database
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw = data['pw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @property
    def fullname(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"


    #C
    @classmethod
    def create(cls, data:dict) -> int:
        query = "INSERT INTO users (first_name, last_name, email, pw) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    #R
    @classmethod
    def get_one(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])


    @classmethod
    def get_one_by_email(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])

    #U
    @classmethod
    def update_one(cls, data:dict) -> None:
        query = "UPDATE users SET first_name = %(first_name)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    #D
    @classmethod
    def delete_one(cls, data:dict) -> None:
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_registration(data:dict) -> bool:
        is_valid = True
        
        if len(data['first_name']) < 1:
            is_valid = False
            flash("First name is required", "err_users_first_name")
        
        if len(data['last_name']) < 1:
            is_valid = False
            flash("Last name is required", "err_users_last_name")
        
        if len(data['email']) < 1:
            is_valid = False
            flash("Email is required", "err_users_email")
        
        if len(data['pw']) < 1:
            is_valid = False
            flash("Password is required", "err_users_pw")
        
        elif len(data['confirm_pw']) != data['pw']:
            is_valid = False
            flash("Passwords do not match", "err_users_confirm_pw")

        return is_valid


    @staticmethod
    def validate_login(data:dict) -> bool:
        is_valid = True
                
        if len(data['email']) < 1:
            is_valid = False
            flash("Email is required", "err_users_email")
        
        if len(data['pw']) < 1:
            is_valid = False
            flash("Password is required", "err_users_pw")
        else:
            potential_user = User.get_one_by_email({'email':data['email']})
            if not bcrypt.check_password_hash(potential_user.pw, data["pw"]):
                flash("Invalid Credentials", "err_users_pw")
                is_valid = False
            session['uuid'] = potential_user.id
        return is_valid