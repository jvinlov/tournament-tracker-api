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



# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'hi'

if 'ON_HEROKU' in os.environ:
	print('hitting')
	models.initialize()

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)

