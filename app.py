from flask import Flask, jsonify, request, render_template, send_from_directory, abort, redirect, url_for, session
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import random
from db.models import *
import bcrypt

engine = sa.create_engine(
    'mysql+mysqldb://ramsay:ramsay123@ramsay.cn8pndyiytrv.us-east-1.rds.amazonaws.com:3306/Ramsay?charset=utf8')
Session = sessionmaker(bind=engine, autoflush=True)

app = Flask(__name__)
app.secret_key = 'alexaramsay123'


@app.route('/')
def get_list():
    if 'doctor_id' not in session:
        return redirect(url_for('login'))
    doctor_id = session['doctor_id']
    db_session = Session()
    db_doctor = db_session.query(Doctor).get(doctor_id)
    return render_template('list.html', doctor=db_doctor)


@app.route('/user/<int:user_id>')
def user(user_id):
    if 'doctor_id' not in session:
        return redirect(url_for('login'))
    doctor_id = session['doctor_id']
    db_session = Session()
    db_doctor = db_session.query(Doctor).get(doctor_id)
    db_user = db_session.query(User).get(user_id)
    if not db_user:
        return redirect(url_for('get_list'))
    return render_template('user.html', user=db_user, doctor=db_doctor)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        db_session = Session()
        email = request.form['email']

        db_doctor = db_session.query(Doctor).filter_by(email=email).first()

        if db_doctor is None:
            return redirect(url_for('login'))

        password = request.form['password'].encode('utf-8')

        if not bcrypt.hashpw(password, db_doctor.password.encode('utf-8')) == db_doctor.password:
            return redirect(url_for('login'))
        session['doctor_id'] = db_doctor.id
        return redirect(url_for('get_list'))


def get_recipe_set(db_user_ingredients, db_session):
    recipe_id_set = None
    for db_user_ingredient in db_user_ingredients:
        db_ingredients = db_session.query(Ingredient).filter(
            Ingredient.name.like("%{}%".format(db_user_ingredient.name))).all()
        tmp_recipe_set = set(x.recipe_id for x in db_ingredients)
        if recipe_id_set is None:
            recipe_id_set = tmp_recipe_set
        else:
            recipe_id_set = recipe_id_set & tmp_recipe_set

    return recipe_id_set


@app.route("/recipe", methods=['GET', 'POST'])
def get_recipe():
    db_session = Session()
    try:
        alexa_id = request.args.get('userId')
        if not alexa_id:
            return jsonify({"error": "Invalid Alexa ID"}), 404
        db_user = db_session.query(User).filter_by(alexa_id=alexa_id).first()
        if not db_user:
            return jsonify({"error": "Unable to find user"}), 404

        db_session.query(CurrentRecipe).delete()
        db_session.query(CurrentInstruction).delete()
        db_session.query(CurrentUserIngredients).delete()

        # Get recipe based on user's ingredients
        if request.method == 'GET':
            db_user_ingredients = db_session.query(UserIngredients).filter_by(user_id=db_user.id).all()
            db_user_ingredients = random.sample(list(db_user_ingredients), 2)
            # db_user_allergies = db_session.query(UserAllergies).filter_by(user_id=db_user.id).all()
            recipe_id_set = get_recipe_set(db_user_ingredients, db_session)

            # for recipe_id in list(recipe_id_set):
            #     db_recipe = db_session.query(Recipe).get(recipe_id)
            #     for db_ingredient in db_recipe.ingredients:
            #         for db_user_allergy in db_user_allergies:
            #             if db_ingredient.name == db_user_allergy.name:
            #                 recipe_id_set.discard(recipe_id)

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
                return jsonify(db_recipe.to_dict())
            else:
                db_session.close()
                return jsonify({"error": "Could not find a valid recipe"}), 400

        # Get recipe based on input
        elif request.method == 'POST':
            ingredient_list = request.json['ingredients']

            recipe_id_set = None
            for ingredient_name in ingredient_list:
                db_ingredients = db_session.query(Ingredient).filter(
                    Ingredient.name.like("%{}%".format(ingredient_name))).all()
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
                return jsonify(db_recipe.to_dict())
            else:
                db_session.close()
                return jsonify({"error": "Could not find a valid recipe"}), 400
    except Exception as e:
        print e
    finally:
        db_session.close()


@app.route("/step", methods=['GET'])
def get_step():
    db_session = Session()

    alexa_id = request.args.get('userId')
    if not alexa_id:
        return jsonify({"error": "Invalid Alexa ID"}), 404
    db_user = db_session.query(User).filter_by(alexa_id=alexa_id).first()
    if not db_user:
        return jsonify({"error": "Unable to find user"}), 404

    db_current_recipe = db_session.query(CurrentRecipe).first()

    db_current_instruction = db_session.query(CurrentInstruction).filter_by(status_id=1).first()

    # Completed
    if db_current_instruction is None:
        db_current_recipe.status_id = 3
        db_session.add(db_current_recipe)

        db_completed_recipe = db_session.query(CompletedRecipe).filter_by(user_id=db_user.id,
                                                                          recipe_id=db_current_recipe.recipe_id).first()

        if not db_completed_recipe:
            db_completed_recipe = CompletedRecipe()
            db_completed_recipe.recipe_id = db_current_recipe.recipe_id
            db_completed_recipe.user_id = db_user.id
            db_session.add(db_completed_recipe)

        db_session.commit()
        return jsonify({"instruction": "You are done."})

    db_current_recipe.status_id = 2
    db_current_instruction.status_id = 3
    db_session.commit()
    return jsonify(db_current_instruction.to_dict())


@app.route("/first_step", methods=['GET'])
def get_first_step():
    db_session = Session()

    db_current_instructions = db_session.query(CurrentInstruction).all()

    for db_current_instruction in db_current_instructions:
        db_current_instruction.status_id = 1
        db_session.add(db_current_instruction)
    db_session.commit()

    db_current_instruction = db_session.query(CurrentInstruction).filter_by(status_id=1).first()
    return jsonify(db_current_instruction.to_dict())


@app.route("/previous_step", methods=['GET'])
def get_previous_step():
    db_session = Session()

    db_current_instruction = db_session.query(CurrentInstruction).filter_by(status_id=3).order_by(
        CurrentInstruction.id.desc()).first()

    if db_current_instruction is None:
        db_current_instruction = db_session.query(CurrentInstruction).filter_by(status_id=1).first()

    db_current_instruction.status_id = 3
    db_session.add(db_current_instruction)
    db_session.commit()

    return jsonify(db_current_instruction.to_dict())


@app.route("/current_recipe", methods=['GET'])
def get_current_recipe():
    db_session = Session()

    db_current_recipe = db_session.query(CurrentRecipe).first()

    return jsonify(db_current_recipe.to_dict())


@app.route("/add_ingredient", methods=['POST'])
def add_ingredient():
    user_id = int(request.form['user_id'])
    ingredient_name = request.form['ingredient']

    db_session = Session()
    db_user_ingredient = UserIngredients()
    db_user_ingredient.user_id = user_id
    db_user_ingredient.name = ingredient_name
    db_session.add(db_user_ingredient)
    db_session.commit()

    return redirect(url_for('get_list'))


@app.route("/remove_ingredient/<int:ingredient_id>", methods=['GET'])
def delete_ingredient(ingredient_id):
    db_session = Session()
    db_user_ingredient = db_session.query(UserIngredients).get(ingredient_id)
    if not db_user_ingredient:
        return redirect(url_for('get_list'))
    db_session.delete(db_user_ingredient)
    db_session.commit()

    return redirect(url_for('get_list'))
