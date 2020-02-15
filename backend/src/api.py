import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def retrieve_drinks():
    selection = Drink.query.all()
    drinks = [drink.short() for drink in selection]
    # abort if there are no drinks in the database,
    if len(drinks) == 0:
        abort(404)
    return jsonify({
        'success': True,
        "drinks": drinks
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drink_detail(payload):
    selection = Drink.query.all()
    drinks = [drink.long() for drink in selection]
    if len(drinks) == 0:
        abort(404)
    return jsonify({
        "success": True,
        "drinks": drinks
    })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    try:
        body = request.get_json()
        new_title = body.get('title', None)
        new_recipe = body.get('recipe', None)
        # make sure that title and recipe are both present,
        if (new_title is None) or (new_recipe is None):
            abort(422)
        # If the recipe has not been input as a list,
        # format it correctly and create the drink object.
        if type(new_recipe) is not list:
            new_recipe = [new_recipe]
        drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        # abort if a drink in the database has the same name or recipe.
        database_drinks = Drink.query.all()
        for dbdrink in database_drinks:
            if (drink.title == dbdrink.title) or (drink.recipe == dbdrink.recipe):
                abort(422)
        # Otherwise, create a row in the database for the drink.
        drink.insert()
        return jsonify({
            'success': True,
            "drinks": [drink.long()]
        })
    except AuthError:
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    try:
        # Find the drink with the given id,
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404)
        # Retrieve the updated drink data.
        body = request.get_json()
        updated_title = body.get('title', None)
        updated_recipe = body.get('recipe', None)

        # Update the drink with the new values.
        if updated_title is not None:
            drink.title = updated_title
        if updated_recipe is not None:
            if type(updated_recipe) is not list:
                updated_recipe = [updated_recipe]
            drink.recipe = json.dumps(updated_recipe)
        drink.update()
        return jsonify({
        "success": True,
        "drinks": [drink.long()]
    })
    except AuthError:
        abort(422)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        # Find the drink with the given id,
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404)
        drink.delete()
        return jsonify({
            "success": True,
            "delete": id
        })
    except AuthError:
        abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
      }), 400

@app.errorhandler(401)
def unauthorized(error):
  return jsonify({
    "success": False,
    "error": 401,
    "message": "unauthorized"
    }), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
      }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
      }), 422

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def handle_invalid_usage(error):
    return jsonify({
        "success": False,
        "error": error.error,
        "message": error.status_code
    }), error.error
