from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, Boolean, TEXT, TIMESTAMP
from datetime import datetime

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
    name = Column(TEXT)
    recipe_id = Column(Integer)

    def to_dict(self):
        return dict(
        )


class Instruction(Base):
    __tablename__ = "instruction"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    recipe_id = Column(Integer)
    step_number = Column(Integer)
    text = Column(TEXT)

    def to_dict(self):
        return dict(
        )