from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, Boolean, TEXT, TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255))
    source = Column(Integer)

    def to_dict(self):
        return dict(
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
    recipe_id = Column(Integer)

    def to_dict(self):
        return dict(
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
        )


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String(255))

    def to_dict(self):
        return dict(
        )


class UserIngredients(Base):
    __tablename__ = "user_ingredients"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    name = Column(String(255))
    status_id = Column(Integer)

    user = relationship("User", backref="user_ingredients")

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
        )


class CurrentInstruction(Base):
    __tablename__ = "current_instruction"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    instruction_id = Column(Integer, ForeignKey("instruction.id"))
    status_id = Column(Integer)

    instruction = relationship("Instruction")

    def to_dict(self):
        return dict(
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