from bs4 import BeautifulSoup
import urllib
from json import loads, dumps
from db.models import *
from app import Session


def clean():
    db_ingredients = db_session.query(Ingredient).all()

    db_user_ingredients = db_session.query(UserIngredients).all()

    for db_ingredient in db_ingredients:
        for db_user_ingredient in db_user_ingredients:
            if db_user_ingredient.name in db_ingredient.name:
                db_ingredient.name = db_user_ingredient.name
                db_session.add(db_ingredient)


db_session = Session()
clean()
db_session.commit()
