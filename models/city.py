#!/usr/bin/python3
"""[models/city module]"""
from models.base_model import BaseModel


class City(BaseModel):
    """[City class]
    inherits from BaseModel
    """
    state_id = ""
    name = ""
