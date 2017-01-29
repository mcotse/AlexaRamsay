from bs4 import BeautifulSoup
import urllib
from json import loads, dumps
from db.models import *
from app import Session


def scrape(recipe_url, img_url):
    r = urllib.urlopen(recipe_url).read()
    soup = BeautifulSoup(r, 'html.parser')

    recipe_name = soup.find('h1', itemprop='name').text.strip()
    db_recipe = db_session.query(Recipe).filter_by(name=recipe_name).first()
    if db_recipe is not None:
        return
    db_recipe = Recipe()
    db_recipe.source = 2
    db_recipe.name = recipe_name
    db_recipe.img_url = img_url

    db_session.add(db_recipe)
    db_session.flush()

    ingredients = soup.find_all('li', itemprop="recipeIngredient")
    for ingredient in ingredients:
        name = ingredient.contents[3].text.strip() + " " + ingredient.contents[5].text.strip()
        db_ingredient = Ingredient()
        db_ingredient.name = name.strip()
        db_ingredient.recipe_id = db_recipe.id

        db_session.add(db_ingredient)

    instructions = soup.find('section', itemprop='recipeInstructions').find_all('li')
    all_instructions = ""

    for instruction in instructions:
        all_instructions += instruction.text.strip()

    instructions = all_instructions.split('.')
    step_number = 0
    for instruction in instructions:
        if instruction is not "":
            step_number += 1
            db_instruction = Instruction()
            db_instruction.recipe_id = db_recipe.id
            db_instruction.step_number = step_number
            db_instruction.text = instruction.strip() + "."

            db_session.add(db_instruction)


def search(query):
    for i in range(0, 100):
        r = urllib.urlopen(
            "http://www.realsimple.com/search/site/{query}?page={page}&f[0]=bundle%3Arecipe".format(query=query,
                                                                                                    page=i)).read()
        result_page = BeautifulSoup(r, 'html.parser')
        links = result_page.find_all('a', class_='b-inner')
        if len(links) == 0:
            break
        for link in links:
            print link.attrs['href']
            image = link.find('img', class_='field-image-thumb').attrs['src'].strip()
            scrape(link.attrs['href'], image)


db_session = Session()
search('pork')
search('lamb')
search('noodle')
search('beef')
search('vinegar')
search('mustard')
search('mayonnaise')
search('chili')
search('chicken')
search('egg')
search('rice')
search('meatballs')
search('baguette')
search('farro')
search('kale')
search('sage')
search('milk')
search('toast')
search('apple')
search('avocado')
db_session.commit()
