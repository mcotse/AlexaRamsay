from bs4 import BeautifulSoup
import urllib
from json import loads, dumps
from db.models import *
from app import Session


def scrape(recipe_url):
    r = urllib.urlopen(recipe_url).read()
    soup = BeautifulSoup(r, 'html.parser')
    script = soup.find('script', type='application/ld+json')
    metadata = loads(script.text)

    db_session = Session()

    db_recipe = Recipe()
    db_recipe.name = metadata['name']
    db_recipe.source = 1

    db_session.add(db_recipe)
    db_session.commit()

    for ingredient in metadata['recipeIngredient']:
        db_ingredient = Ingredient()
        db_ingredient.name = ingredient
        db_ingredient.recipe_id = db_recipe.id

        db_session.add(db_ingredient)

    step_number = 0
    for instruction in metadata['recipeInstructions']:
        step_number += 1
        db_instruction = Instruction()
        db_instruction.recipe_id = db_recipe.id
        db_instruction.step_number = step_number
        db_instruction.text = instruction

        db_session.add(db_instruction)

    db_session.commit()


scrape('http://www.marthastewart.com/332837/brick-chicken')
