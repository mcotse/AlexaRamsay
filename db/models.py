from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, Boolean, TEXT, TIMESTAMP, CHAR
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255))
    source = Column(Integer)
    img_url = Column(String(255))

    def to_dict(self):
        return dict(
            id=self.id,
            recipe_name=self.name,
            source=self.source,
            img_url=self.img_url,
            ingredients=list(x.to_dict() for x in self.ingredients)
        )


class Source(Base):
    __tablename__ = "source"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255))

    def to_dict(self):
        return dict(
        )


class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255))
    recipe_id = Column(Integer, ForeignKey("recipe.id"))

    recipe = relationship("Recipe", backref="ingredients")

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            recipe_id=self.recipe_id
        )


class Instruction(Base):
    __tablename__ = "instruction"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    step_number = Column(Integer)
    text = Column(TEXT)

    recipe = relationship("Recipe", backref="recipe_instructions")

    def to_dict(self):
        return dict(
            recipe=self.recipe.to_dict(),
            step_number=self.step_number,
            instruction=self.text
        )


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String(45))
    last_name = Column(String(45))
    email = Column(String(255))
    alexa_id = Column(String(255))
    height = Column(Integer)
    weight = Column(Integer)
    age = Column(Integer)
    gender = Column(CHAR)
    img_url = Column(String(255))

    doctor_id = Column(Integer, ForeignKey("doctor.id"))

    doctor = relationship("Doctor", backref="patients", lazy='subquery')

    def to_dict(self):
        return dict(
        )


class UserIngredients(Base):
    __tablename__ = "user_ingredients"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    name = Column(String(45))

    user = relationship("User", backref="user_ingredients")

    def to_dict(self):
        return dict(
        )


class UserAllergies(Base):
    __tablename__ = "user_allergies"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    name = Column(String(45))

    user = relationship("User", backref="user_allergies")

    def to_dict(self):
        return dict(
        )


class CurrentRecipe(Base):
    __tablename__ = "current_recipe"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    status_id = Column(Integer)

    recipe = relationship("Recipe")

    def to_dict(self):
        return dict(
            recipe_name=self.recipe.name,
            status_id=self.status_id
        )


class CurrentInstruction(Base):
    __tablename__ = "current_instruction"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    instruction_id = Column(Integer, ForeignKey("instruction.id"))
    status_id = Column(Integer)

    instruction = relationship("Instruction")

    def to_dict(self):
        return dict(
            instruction=self.instruction.text,
            status_id=self.status_id
        )


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(45))

    def to_dict(self):
        return dict(
        )


class CurrentUserIngredients(Base):
    __tablename__ = "current_user_ingredients"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_ingredient_id = Column(Integer, ForeignKey("user_ingredients.id"))

    user_ingredient = relationship("UserIngredients")

    def to_dict(self):
        return dict(
        )


class Doctor(Base):
    __tablename__ = "doctor"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String(45))
    password = Column(String(255))
    first_name = Column(String(45))
    last_name = Column(String(45))

    def to_dict(self):
        return dict(
            id=self.id,
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name
        )


class CompletedRecipe(Base):
    __tablename__ = "completed_recipes"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    recipe_id = Column(Integer, ForeignKey("recipe.id"))

    user = relationship("User", backref="completed_recipes")
    recipe = relationship("Recipe", backref="completed_recipes")

    def to_dict(self):
        return dict(
            id=self.id,
            user=self.user.to_dict(),
            recipe=self.recipe.to_dict()
        )

class CompletedIngredient(Base):
    __tablename__ = "completed_ingredients"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"))

    user = relationship("User", backref="completed_ingredients")
    ingredient = relationship("Ingredient", backref="completed_ingredients")

    def to_dict(self):
        return dict(
            id=self.id,
            user=self.user.to_dict(),
            ingredient=self.ingredient.to_dict()
        )
