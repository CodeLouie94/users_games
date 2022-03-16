from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = 'shhhhhhhh'

bcrypt = Bcrypt(app)

DATABASE = 'users_games_db'
