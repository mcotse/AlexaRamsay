from flask import Flask, jsonify, request, render_template, send_from_directory, abort
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import random
from db.models import *

engine = sa.create_engine(
    'mysql+mysqldb://ramsay:ramsay123@ramsay.cn8pndyiytrv.us-east-1.rds.amazonaws.com:3306/Ramsay?charset=utf8')
Session = sessionmaker(bind=engine, autoflush=True)

app = Flask(__name__)


@app.route("/recipe", methods=['GET', 'POST'])
def get_recipe():
    db_session = Session()
    if request.method == 'GET':
        db_session.query(CurrentRecipe).delete()
        db_session.query(CurrentInstruction).delete()
        db_session.query(CurrentUserIngredients).delete()

        db_user = db_session.query(User).get(1)
        db_user_ingredients = db_session.query(UserIngredients).filter_by(user_id=db_user.id, status_id=1).limit(2).all()
        recipe_id_set = None
        for db_user_ingredient in db_user_ingredients:
            db_ingredients = db_session.query(Ingredient).filter_by(name=db_user_ingredient.name).all()
            tmp_recipe_set = set(x.recipe_id for x in db_ingredients)
            if recipe_id_set is None:
                recipe_id_set = tmp_recipe_set
            else:
                recipe_id_set = recipe_id_set & tmp_recipe_set

            db_current_user_ingredient = CurrentUserIngredients()
            db_current_user_ingredient.user_ingredient_id = db_user_ingredient.id
            db_session.add(db_current_user_ingredient)

        if len(recipe_id_set) > 0:
            recipe_id = random.choice(list(recipe_id_set))
            db_recipe = db_session.query(Recipe).get(recipe_id)
            db_current_recipe = CurrentRecipe()
            db_current_recipe.recipe_id = recipe_id
            db_current_recipe.status_id = 1
            db_session.add(db_current_recipe)

            for recipe_instruction in db_recipe.recipe_instructions:
                db_current_instruction = CurrentInstruction()
                db_current_instruction.instruction_id = recipe_instruction.id
                db_current_instruction.status_id = 1
                db_session.add(db_current_instruction)

            db_session.commit()
            response = {"recipe_name": db_recipe.name}
            db_session.close()
            return jsonify(response)
        else:
            db_session.close()
            return jsonify({"error": "Could not find a valid recipe"}), 400
    elif request.method == 'POST':
        ingredient_list = request.json['ingredients']

        recipe_id_set = None
        for ingredient_name in ingredient_list:
            db_ingredients = db_session.query(Ingredient).filter_by(name=ingredient_name).all()
            tmp_recipe_set = set(x.recipe_id for x in db_ingredients)
            if recipe_id_set is None:
                recipe_id_set = tmp_recipe_set
            else:
                recipe_id_set = recipe_id_set & tmp_recipe_set

        if recipe_id_set is not None and len(recipe_id_set) > 0:
            recipe_id = random.choice(list(recipe_id_set))
            db_recipe = db_session.query(Recipe).get(recipe_id)
            db_current_recipe = CurrentRecipe()
            db_current_recipe.recipe_id = recipe_id
            db_current_recipe.status_id = 1
            db_session.add(db_current_recipe)

            for recipe_instruction in db_recipe.recipe_instructions:
                db_current_instruction = CurrentInstruction()
                db_current_instruction.instruction_id = recipe_instruction.id
                db_current_instruction.status_id = 1
                db_session.add(db_current_instruction)

            db_session.commit()
            response = {"recipe_name": db_recipe.name}
            db_session.close()
            return jsonify(response)
        else:
            db_session.close()
            return jsonify({"error": "Could not find a valid recipe"}), 400


@app.route("/step", methods=['GET'])
def get_step():
    db_session = Session()

    db_current_recipe = db_session.query(CurrentRecipe).first()

    db_current_instruction = db_session.query(CurrentInstruction).filter_by(status_id=1).first()

    if db_current_instruction is None:
        db_current_recipe.status_id = 3

        db_current_user_ingredients = db_session.query(CurrentUserIngredients).all()
        for db_current_user_ingredient in db_current_user_ingredients:
            db_current_user_ingredient.user_ingredient.status_id = 3
            db_session.add(db_current_user_ingredient.user_ingredient)

        db_session.commit()
        return jsonify({"instruction": "You are done."})

    db_current_recipe.status_id = 2
    db_current_instruction.status_id = 3
    db_session.commit()
    return jsonify({"instruction": db_current_instruction.instruction.text})
