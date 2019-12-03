import models
# import pdb # the python debugger
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required # need this for authorization
from playhouse.shortcuts import model_to_dict
# playhouse is from peewee

# first argument is blueprint's name
# second argument is it's import_name
tourney = Blueprint('tourneys', 'tourney')
#blueprint is like the router in express, it records operations


#attach restful CRUD routes to issue blueprint

# Index Route (get)
@tourney.route('/', methods=["GET"]) # GET is the default method
def get_all_tourneys():
    # print(vars(request))
    # print(request.cookies)
    ## find the issues and change each one to a dictionary into a new array
    
    print('Current User:',  current_user, "line 23", '\n')
    # Send all issues back to client. There is no valid reason for this not to work
    # so we don't use a try -> except.
    # IMPORTANT -> Use max_depth=0 if we want just the issue created_by id and not the entire
    # created_by object sent back to the client. 
    # Could also use exclude=[models.Issue.created_by] to entirely remove ref to created_by
    # http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#model_to_dict
    # all_issues = [model_to_dict(d, max_depth=0) for d in models.Issue.select()]

    # we want the entire object, so we are not going to use max_depth=0
    all_tourneys = [model_to_dict(tourney) for tourney in models.Tourney.select()]

    print(all_tourneys, 'line 31', '\n')
    return jsonify(data=all_tourneys, status={'code': 200, 'message': 'Success'})

# Create/New Route (post)
# @login_required <- look this up to save writing some code https://flask-login.readthedocs.io/en/latest/#flask_login.login_required
@tourney.route('/', methods=["POST"])
def create_tourney():
    ## see request payload anagolous to req.body in express
    payload = request.get_json() # flask gives us a request object (similar to req.body)
    print(type(payload), 'payload')
    

    if not current_user.is_authenticated: # Check if user is authenticated and allowed to create a new issue
        print(current_user)
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create a tourney'})

    payload['created_by'] = current_user.id # Set the 'created_by' of the issue to the current user
    print(payload['created_by'], 'created by current user id')
    #######################################################################
    print(payload, 'line 63')
    tourney = models.Tourney.create(**payload) ## ** spread operator
    # returns the id, see print(issue)

    ## see the object
    # print(issue)
    # print(issue.__dict__)
    ## Look at all the methods
    # print(dir(issue))
    # Change the model to a dict
    print(model_to_dict(tourney), 'model to dict')
    tourney_dict = model_to_dict(tourney)
    return jsonify(data=tourney_dict, status={"code": 201, "message": "Success"})


# Show/Read Route (get)
@tourney.route('/<tourney_id>', methods=["GET"])
def get_one_tourney(id):
    # print(id)
    try:
        # Try to find issue with a certain id
        issue = model_to_dict(models.Issue.get(id=issue_id, max_depth=0))
        return jsonify(issue)
    except models.DoesNotExist:
        # If the id does not match an id of an issue in the database return 404 error
        return jsonify(data={}, status={'code': 404, 'message': 'Issue not found'})


# Update/Edit Route (put)
@tourney.route('/<id>', methods=["PUT"])
def update_tourney(id):
    # print('hi')
    # pdb.set_trace()
    payload = request.get_json()
    # print(payload)

    # Get the issue we are trying to update. Could put in try -> except because
    # if we try to get an id that doesn't exist a 500 error will occur. Would 
    # send back a 404 error because the 'issue' resource wasn't found.
    tourney_to_update = models.Tourney.get(id=id)
    print(tourney_to_update, "94")
    if not current_user.is_authenticated: # Checks if user is logged in
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to edit a tournament'})

    if issue_to_update.created_by.id is not current_user.id: 
        # Checks if create_by (User) of issue has the same id as the logged in User.
        # If the ids don't match send 401 - unauthorized back to user
        return jsonify(data={}, status={'code': 401, 'message': 'You can only update a tournament you created'})



    #new code
    tourney_to_update.date = payload['date']
    tourney_to_update.save()

    # Get a dictionary of the updated issue to send back to the client.
    # Use max_depth=0 because we want just the created_by id and not the entire
    # created_by object sent back to the client. 
    # update_tourney_dict = model_to_dict(tourney_to_update, max_depth=0)

    # we want the entire object, so we are not going to use max_depth=0
    update_tourney_dict = model_to_dict(tourney_to_update)
    return jsonify(status={'code': 200, 'msg': 'success'}, data=update_tourney_dict)    



# Delete Route (delete)
@tourney.route('/<id>', methods=["DELETE"])
def delete_tourney(id):
    # Get the issue we are trying to delete. Could put in try -> except because
    # if we try to get an id that doesn't exist a 500 error will occur. Would 
    # send back a 404 error because the 'issue' resource wasn't found.
    tourney_to_delete = models.Tourney.get(id=id)
    print(tourney_to_delete, 'line 127');
    print(current_user, 'line 128');
    if not current_user.is_authenticated: # Checks if user is logged in
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create a tournament'})
    if tourney_to_delete.created_by.id is not current_user.id: 
        # Checks if created_by (User) of issue has the same id as the logged in User
        # If the ids don't match send 401 - unauthorized back to user
        return jsonify(data={}, status={'code': 401, 'message': 'You can only delete tournament you created'})
    
    # Delete the issue and send success response back to user
    query = models.Tourney.delete().where(models.Tourney.id==id)
    query.execute()
    print(tourney_to_delete, 'line 139');
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})



