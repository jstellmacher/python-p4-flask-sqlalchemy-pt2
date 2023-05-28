#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

from app import app
from models import db, Owner, Pet

fake = Faker()

with app.app_context():

    Pet.query.delete()
    Owner.query.delete()

    owners = []
    for n in range(50):
        owner = Owner(name=fake.name())
        owners.append(owner)

    db.session.add_all(owners)

    pets = []
    species = ['Dog', 'Cat', 'Chicken', 'Hamster', 'Turtle']
    for n in range(100):
        pet = Pet(name=fake.first_name(), species=rc(species), owner=rc(owners))
        pets.append(pet)

    db.session.add_all(pets)
    db.session.commit()


# ! You'll notice that this looks virtually identical to our seed scripts from Phase 3: we delete all records from the database, make lists of owner and pet instances, generate attributes with random and faker, then commit the transaction.

#! Let's go over the differences:

#! 1 - We need to create an application context with app.app_context() before we begin. This will not necessarily be used, but it ensures that applications fail quickly if they are not configured with this important context.
#! 2 - Deletion of all records is handled through models with Model.query.delete() rather than session.query(Model).delete(). This syntax is carried through other SQLAlchemy statements and queries as well. Because the session is managed through the Flask application, there is no need to call it explicitly when we run these statements and queries.
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#

# from models import db, Pet, Owner
# >> from app import app
# >> with app.app_context():
# ...     Pet.query.all()
# ...
#  => [<Pet Richard, Turtle>, <Pet Jonathan, Cat>, <Pet Victoria, Chicken>, ...]
# We can also narrow our search using filters or chains of filters:

# // imports
# >> with app.app_context():
# = 'Ben').all()
#  => [<Pet Owner Brenda Hernandez>, <Pet Owner Brian Stone>, ...]

# >> with app.app_context():
# ...     Owner.query.filter(Owner.name <= 'Ben').limit(2).all()
# ...
#  => [<Pet Owner Alan Bryant>, <Pet Owner Allison Phillips DDS>]