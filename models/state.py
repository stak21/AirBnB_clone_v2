#!/usr/bin/python3
"""This is the state class"""
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    name = ""

    cities = relationship("City", cascade="all,delete", backref="state")
