import os # for heroku
import datetime
from peewee import *
from flask_login import UserMixin
from playhouse.db_url import connect


if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL')) 

else:
	DATABASE = SqliteDatabase('tourneys.sqlite')


class Tourney(Model):
	name = CharField()
	date = CharField ()#(default= datetime.datetime.now)
	location = CharField()
	usapa = BooleanField()
	# added created_by to relate an issue to the person creating the issue
	# tourney_event = ForeignKeyField(Event, backref='tourneys')# Represents One-to-Many
	# have access to 'events' as list on tourney because tourney exists on Event

	class Meta:
		db_table = 'tourneys'
		database = DATABASE

class Event(Model):
	category = CharField()
	level = CharField()
	partner = CharField()
	results = CharField()
	# tourney = ForeignKeyField(Tourney, backref='events') 
	# user= ForeignKeyField(User, backref= 'events')	
														
	class Meta:
		db_table = 'events'
		database = DATABASE

class User(UserMixin, Model):
	name = CharField()
	age = IntegerField()
	gender = CharField()
	rating = CharField()
	events = ForeignKeyField(Event, backref= 'users')
	# has 'events' through events foreign key
	email = CharField(unique=True)
	password = CharField()


	def __str__(self):
		return '<User: {}, id: {}>'.format(self.email, self.id)

	def __repr__(self):
		return '<User: {}, id: {}>'.format(self.email, self.id)

	class Meta:
		db_table = 'users'
		database = DATABASE










def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Tourney, Event], safe=True) 
	print("TABLES CREATED")
	DATABASE.close()