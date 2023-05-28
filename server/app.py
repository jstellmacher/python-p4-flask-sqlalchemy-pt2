#!/usr/bin/env python3
# server/app.py

#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Our app.config is set up to point to our existing database, and 'SQLALCHEMY_TRACK_MODIFICATIONS' is set to False to avoid building up too much unhelpful data in memory when our application is running.

migrate = Migrate(app, db)
 # migrate instance configures the application and models for Flask-Migrate.

db.init_app(app)
# db.init_app connects our database to our application before it runs.


@app.route('/')
def index():
    response = make_response(
        '<h1>Welcome to the pet/owner directory!</h1>',
        200
    )
    return response
# @app.route determines which resources are available at which URLs and saves them to the application's URL map. Responses are what we return to the client after a request. The included response has a status code of 200, which means that the resource exists and is accessible at the provided URL.

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if not pet:
        response_body = '<h1>404 pet not found</h1>'
        response = make_response(response_body, 404)
        return response

    response_body = f'''
        <h1>Information for {pet.name}</h1>
        <h2>Pet Species is {pet.species}</h2>
        <h2>Pet Owner is {pet.owner.name}</h2>
    '''

    response = make_response(response_body, 200)

    return response

@app.route('/owner/<int:id>')
def owner_by_id(id):
    owner = Owner.query.filter(Owner.id == id).first()

    if not owner:
        response_body = '<h1>404 owner not found</h1>'
        response = make_response(response_body, 404)
        return response

    response_body = f'<h1>Information for {owner.name}</h1>'

    pets = [pet for pet in owner.pets]

    if not pets:
        response_body += f'<h2>Has no pets at this time.</h2>'

    else:
        for pet in pets:
            response_body += f'<h2>Has pet {pet.species} named {pet.name}.</h2>'

    response = make_response(response_body, 200)

    return response
#  Because we generated data with Faker, you will probably not see the same names, but your format should match below:


if __name__ == '__main__':
    app.run(port=5555, debug=True)
