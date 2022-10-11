from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.coffee import Roasts

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Users:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.roasts = []


    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('solo_roast').query_db(query, data)

    @classmethod
    def valid_login(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('solo_roast').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s'
        results = connectToMySQL('solo_roast').query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_all_by_id(cls, data):
        query = 'SELECT * FROM users LEFT JOIN roasts ON users.id = roasts.user_id WHERE users.id = %(id)s;'
        results = connectToMySQL('solo_roast').query_db(query, data)

        users = cls(results[0])
        for db_row in results:
            roast = {
                'id': db_row['roasts.id'],
                'user_id': db_row['user_id'],
                'name': db_row['name'],
                'origin': db_row['origin'],
                'start_temp': db_row['start_temp'],
                'start_time': db_row['start_time'],
                'degree': db_row['degree'],
                'first_temp': db_row['first_temp'],
                'first_time': db_row['first_time'],
                'level': db_row['level'],
                'time': db_row['time'],
                'share': db_row['share'],
                'created_at': db_row['roasts.created_at'],
                'updated_at': db_row['roasts.updated_at'],
            }
            users.roasts.append(Roasts(roast))
        return users















    @staticmethod
    def valid_register(users):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('solo_roast').query_db(query, users)
        if len(results) >= 1:
            flash("i'm sorry, but is seems that email address is already taken")
            is_valid = False
        if len(users['first_name']) <2:
            flash('Please enter your first name.')
            is_valid = False
        if len(users['last_name']) < 2:
            flash('Please enter your last name.')
            is_valid = False
        if not EMAIL_REGEX.match(users['email']):
            flash('Please enter a real email address.')
            is_valid = False
        if len(users['password']) < 8:
            flash('Your password must be at least 8 characters, please try again.')
            is_valid = False
        if (users['password']) != (users['confirm_password']):
            flash("I'm sorry, but it appears as though your passwords do not match. Please try again.")
            is_valid = False
        return is_valid

