from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

#model the class after the friend table from our database
class Game:
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #C
    @classmethod
    def create(cls, data:dict) -> int:
        query = "INSERT INTO games (title, genre, time_played, user_id) VALUES (%(title)s, %(genre)s, %(time_played)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    #R
    @classmethod
    def get_one(cls, data:dict) -> list:
        query = "SELECT * FROM games WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_all(cls, data:dict) -> list:
        query = "SELECT * FROM games WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False


    #U
    @classmethod
    def update_one(cls, data:dict) -> None:
        query = "UPDATE games SET title = %(title)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    #D
    @classmethod
    def delete_one(cls, data:dict) -> None:
        query = "DELETE FROM games WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate(data:dict) -> bool:
        is_valid = True
        
        if len(data['title']) <1:
            flash('title is required', 'err_game_title')
            is_valid = False
        
        if len(data['genre']) <1:
            flash('genre is required', 'err_game_genre')
            is_valid = False
        
        # if (data['time_played']):
        #     flash('time_played is required', 'err_game_time_played')
        #     is_valid = False
        
        return is_valid