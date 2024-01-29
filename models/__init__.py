#!/usr/bin/python3
"""[__init__ magic method to create a unique FileStorage
instance for the aplication]"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
