from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users

class Roasts:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.origin = data['origin']
        self.start_temp = data['start_temp']
        self.start_time = data['start_time']
        self.degree = data['degree']
        self.first_temp = data['first_temp']
        self.first_time = data['first_time']
        self.level = data['level']
        self.time = data['time']
        self.share = data['share']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.users = None

    @classmethod
    def get_all(cls):
        query = 'SELECT roasts.id, name, origin, start_temp, start_time, degree, first_temp, first_time, level, time, share, roasts.created_at, roasts.updated_at, users.id as user_id, first_name, last_name, email, password, users.created_at as created, users.updated_at as updated FROM roasts JOIN users ON users.id = roasts.user_id;'
        roast_data = connectToMySQL('solo_roast').query_db(query)

        roasts = []
        for roast in roast_data:
            ro = cls(roast)
            ro.users = users.Users(
                {
                    'id': roast['user_id'],
                    'first_name': roast['first_name'],
                    'last_name': roast['last_name'],
                    'email': roast['email'],
                    'password': roast['password'],
                    'created_at': roast['created'],
                    'updated_at': roast['updated'],
                }
            )
            roasts.append(ro)

        return roasts

    @classmethod
    def submit(cls, data):
        query = 'INSERT INTO roasts (user_id, name, origin, start_temp, start_time, degree, first_temp, first_time, level, time, share) VALUES (%(user_id)s, %(name)s, %(origin)s, %(start_temp)s, %(start_time)s, %(degree)s, %(first_temp)s, %(first_time)s, %(level)s, %(time)s, %(share)s);'
        return connectToMySQL('solo_roast').query_db(query, data)

    @classmethod
    def get_id(cls, data):
        query = 'SELECT * FROM roasts JOIN users on users.id = roasts.user_id WHERE users.id = %(id)s;'
        results = connectToMySQL('solo_roast').query_db(query, data)

        results = results[0]
        roast = cls(results)
        roast.users = users.Users(
            {
                'id': results['user_id'],
                'first_name': results['first_name'],
                'last_name': results['last_name'],
                'email': results['email'],
                'password': results['password'],
            }
        )
        return roast

    @classmethod
    def one_roast(cls, roast_id):
        data = {'id': roast_id}
        query = 'SELECT * FROM roasts JOIN users ON users.id = roasts.user_id WHERE roasts.id = %(id)s;'
        result = connectToMySQL('solo_roast').query_db(query, data)

        result = result[0]
        roast = cls(result)
        roast.users = users.Users(
            {
                'id': result['user_id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at'],
            }
        )
        return roast

    @classmethod
    def update_roast(cls, data):
        

        query = 'UPDATE roasts SET degree = %(degree)s, first_time = %(first_time)s, first_temp = %(first_temp)s, level = %(level)s, time = %(time)s, share = %(share)s WHERE roasts.id = %(id)s;'
        result = connectToMySQL('solo_roast').query_db(query, data)

        return result
        

    @classmethod
    def delete(cls, roast_id):
        data ={ 'id': roast_id }
        query = 'DELETE FROM roasts WHERE id = %(id)s;'
        connectToMySQL('solo_roast').query_db(query, data)
        return roast_id






    @staticmethod
    def validate_roastname(roasts):
        is_valid = True
        if len(roasts['name']) < 3:
            flash('Please name your roast.')
            is_valid = False
        
        return is_valid