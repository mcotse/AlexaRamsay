from bs4 import BeautifulSoup
import urllib
from json import loads, dumps
from db.models import *
from app import Session
import nltk


def clean_ingredients():
    db_ingredients = db_session.query(Ingredient).all()
    prefixes = ['teaspoon', 'tablespoon', 'cup', 'ounce', 'slice']
    for db_ingredient in db_ingredients:
        print db_ingredient.id
        if db_ingredients.name == '':
            db_session.delete(db_ingredient)
        else:
            tokens = nltk.word_tokenize(db_ingredient.name.strip())
            tags = nltk.pos_tag(tokens)
            nouns = list(x[0] for x in list(filter((lambda x: 'NN' in x[1]), tags)))
            db_ingredient.name = ' '.join(nouns)
            for p in prefixes:
                if "{}s".format(p) in db_ingredient.name:
                    db_ingredient.name = db_ingredient.name.replace("{}s".format(p), "").strip()
                    break
                elif p in db_ingredient.name:
                    db_ingredient.name = db_ingredient.name.replace(p, "").strip()
                    break
            db_session.add(db_ingredient)
    db_session.commit()


def clean_instructions():
    db_recipes = db_session.query(Recipe).all()

    for db_recipe in db_recipes:
        print db_recipe.id
        db_instructions = db_session.query(Instruction).filter_by(recipe_id=db_recipe.id).all()
        all_instructions = ""

        for db_instruction in db_instructions:
            all_instructions += db_instruction.text
            db_session.delete(db_instruction)

        instruction_list = all_instructions.split('.')

        for idx, val in enumerate(instruction_list):
            db_instruction = Instruction()
            db_instruction.recipe_id = db_recipe.id
            db_instruction.step_number = idx + 1
            db_instruction.text = val + "."
            db_session.add(db_instruction)


def clean_empty_instructions():
    db_instructions = db_session.query(Instruction).all()

    for db_instruction in db_instructions:
        print db_instruction.id
        if db_instruction.text == "":
            db_session.delete(db_instruction)


db_session = Session()
clean_ingredients()
print "Committing"
db_session.commit()
