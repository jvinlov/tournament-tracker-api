import os
from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager
from resources.users import user
from resources.tourneys import tourney
from resources.events import event
import models

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

app.secret_key = "WEFGLBEQWF" ##Need this to encode the session
login_manager = LoginManager()#sets up the ability to set up the session
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id ==user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/api/v1/user')
app.register_blueprint(tourney, url_prefix='/api/v1/tourney')
app.register_blueprint(event, url_prefix='/api/v1/event')

# # The default URL ends in / ("my-website.com/").
# @app.route('/')
# def index():
#     return 'hi'

if 'ON_HEROKU' in os.environ:
	print('hitting')
	models.initialize()

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)

