import models
# import pdb # the python debugger
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required # need this for authorization
from playhouse.shortcuts import model_to_dict
# playhouse is from peewee

# first argument is blueprint's name
# second argument is it's import_name
event = Blueprint('events', 'event')
#blueprint is like the router in express, it records operations


#attach restful CRUD routes to issue blueprint

# Index Route (get)
@event.route('/<tourney_id>', methods=["GET"]) # GET is the default method
def get_all_events(tourney_id):
    # print(vars(request))
    # print(request.cookies)
    ## find the issues and change each one to a dictionary into a new array
    
    # print('Current User:',  current_user, "line 23", '\n')
    # Send all issues back to client. There is no valid reason for this not to work
    # so we don't use a try -> except.
    # IMPORTANT -> Use max_depth=0 if we want just the issue created_by id and not the entire
    # created_by object sent back to the client. 
    # Could also use exclude=[models.Issue.created_by] to entirely remove ref to created_by
    # http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#model_to_dict
    # all_issues = [model_to_dict(d, max_depth=0) for d in models.Issue.select()]

    # we want the entire object, so we are not going to use max_depth=0
    all_events = [model_to_dict(event) for event in models.Event.select().where(models.Event.tourney == tourney_id)]

    print(all_events, 'line 35', '\n')
    return jsonify(data=all_events, status={'code': 200, 'message': 'Success'})


# Create/New Route (post)
# @login_required <- look this up to save writing some code https://flask-login.readthedocs.io/en/latest/#flask_login.login_required
@event.route('/', methods=["POST"])
def create_event():
    ## see request payload analogous to req.body in express
    payload = request.get_json() # flask gives us a request object (similar to req.body)
    print(type(payload), 'payload')
    tourney_id = 1

    # Make sure to check if current_user is logged in
    # Make sure passing credentials from REACT
    #adding authorization step here...
    if not current_user.is_authenticated: # Check if user is authenticated and allowed to create a new issue
        print(current_user)
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create an event'})

    # Add tourney to payload by using tourney.id
    payload['tourney'] = tourney_id
    payload['user'] = current_user.id # Set the event to the tourney
    print(payload['tourney'], 'created by current user id')
   
    # print(payload, 'line 56')
    event = models.Event.create(**payload) ## ** spread operator
    # returns the id, see print(event)

    ## see the object
    print(event)
    # print(event.__dict__)
    ## Look at all the methods
    print(dir(event))
    # Change the model to a dict
    print(model_to_dict(event), 'model to dict')
    event_dict = model_to_dict(event)
    return jsonify(data=event_dict, status={"code": 201, "message": "Success"})


# Show/Read Route (get)
@event.route('/<id>', methods=["GET"])
def get_one_event(id):
    # print(id)
    try:
        # Try to find event with a certain id
        event = model_to_dict(models.Event.get(id=id))
        return jsonify(event)
    except models.DoesNotExist:
        # If the id does not match an id of an event in the database return 404 error
        return jsonify(data={}, status={'code': 404, 'message': 'Event not found'})

   
# Update/Edit Route (put)
@event.route('/<id>', methods=["PUT"])
def update_event(id):
    # print('hi')
    
    payload = request.get_json()
    # print(payload)

    # Get the issue we are trying to update. Could put in try -> except because
    # if we try to get an id that doesn't exist a 500 error will occur. Would 
    # send back a 404 error because the 'issue' resource wasn't found.
    event_to_update = models.Event.get(id=id)
    print(event_to_update, "line96")
    # if not current_user.is_authenticated: # Checks if user is logged in
    #     return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to edit an event'})

    # if event_to_update.user.id is not current_user.id: 
    #     # Checks if create_by (User) of issue has the same id as the logged in User.
    #     # If the ids don't match send 401 - unauthorized back to user
    #     return jsonify(data={}, status={'code': 401, 'message': 'You can only update an event you created'})

    # Given our form, we only want to update the subject of our issue
    # issue_to_update.update(
    #     subject=payload['subject']
    # ).execute()

    #new code
    event_to_update.category = payload['category']
    event_to_update.level = payload['level']
    event_to_update.partner = payload['partner']
    event_to_update.results = payload['results']

    event_to_update.save()

    # Get a dictionary of the updated event to send back to the client.
    # Use max_depth=0 because we want just the created_by id and not the entire
    # created_by object sent back to the client. 
    # update_event_dict = model_to_dict(event_to_update, max_depth=0)

    # we want the entire object, so we are not going to use max_depth=0
    update_event_dict = model_to_dict(event_to_update)
    return jsonify(status={'code': 200, 'msg': 'success'}, data=update_event_dict)    

# Delete Route (delete)
@event.route('/<id>', methods=["DELETE"])
def delete_event(id):
    # Get the issue we are trying to delete. Could put in try -> except because
    # if we try to get an id that doesn't exist a 500 error will occur. Would 
    # send back a 404 error because the 'issue' resource wasn't found.
    event_to_delete = models.Event.get(id=id)
    print(event_to_delete, 'line 129');
    # print(current_user, 'line 131');
    # if not current_user.is_authenticated: # Checks if user is logged in
    #     return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create an event'})
    # if issue_to_delete.created_by.id is not current_user.id: 
    #     # Checks if created_by (User) of issue has the same id as the logged in User
    #     # If the ids don't match send 401 - unauthorized back to user
    #     return jsonify(data={}, status={'code': 401, 'message': 'You can only delete the event you created'})
    
    # Delete the event and send success response back to user
    query = models.Event.delete().where(models.Event.id==id)
    query.execute()
    print(event_to_delete, 'line 174');
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "event deleted successfully"})

