import models
from flask_bcrypt import generate_password_hash


models.Tourney.create(
	name = 'Vail Pickleball Open',
	date = '08-26-2020',#(default= datetime.datetime.now)
	location = 'Vail, CO',
	usapa = True
)

models.User.create(
	name = 'Josh',
	gender = 'Male',
	rating = '5',
	email = 'joe@joe.com',
	password = generate_password_hash('123')
)

models.Event.create(
	category = 'MD',
	level = '4.5',
	partner = 'Jim',
	results = 'Gold',
	tourney = 1,
	user = 1
)