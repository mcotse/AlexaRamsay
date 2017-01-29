from db.models import *
from app import Session
import csv


def output_file():
    ingredient_set = set()
    db_ingredients = db_session.query(Ingredient).all()

    for ingredient in db_ingredients:
        if len(ingredient.name) > 2 and len(ingredient.name) < 12 and ingredient.name.count(' ') < 1:
            ingredient_set.add(ingredient.name)
    with open('ingredients.csv', 'wb') as csvfile:
        for i in ingredient_set:
            spamwriter = csv.writer(csvfile, delimiter='\n')
            spamwriter.writerow([unicode(i).encode('utf-8')])


db_session = Session()

output_file()

db_session.close()
