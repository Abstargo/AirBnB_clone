#!/usr/bin/python3
"""[Module hat containts the TestFileStorage Class]
    """
import json
from typing import Type
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import unittest
import pycodestyle
import models
import inspect
import os

FileStorage = file_storage.FileStorage
classes = {BaseModel, User, Place, State, City, Amenity, Review}


class Test_style(unittest.TestCase):
    """[Class created to test style and syntax requirements for the
    base_model class]
    """
    @classmethod
    def setUpClass(cls) -> None:
        """[list the functions to docstring test]
        """
        cls.methods_ds = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pycode(self):
        """[Function that check Syntax from Peep8 branch called pycodestyle]
        """
        foo = pycodestyle.StyleGuide(quiet=True).check_files([
            'models/engine/file_storage.py'])
        self.assertEqual(foo.total_errors, 0,
                         "Found code style error (and warnings).")

    def test_docstring(self):
        """[Function to test docstring of the class and the module]
        """
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertIsNot(FileStorage.__doc__, None,
                         "class needs a docstring")
        self.assertTrue(len(file_storage.__doc__) > 0,
                        "file_storage.py needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) > 0,
                        "class needs a docstring")
        for method in self.methods_ds:
            self.assertIsNot(method[1].__doc__, None,
                             f"{method[0]} needs docstring")
            self.assertTrue(len(method[1].__doc__) >
                            0, f"{method[0]} needs docstring")


class TestFileStorage(unittest.TestCase):
    """Testing for FileStorage"""

    def test_all(self):
        """Test all method"""
        storage = FileStorage()
        dictionary = storage.all()
        self.assertIs(dictionary, storage._FileStorage__objects)
        self.assertEqual(dict, type(dictionary))

    def test_new(self):
        """ Testing new method
        """
        for value in classes:
            with self.subTest(value=value):
                obj = value()
                self.assertIn("{}.{}".format(obj.__class__.__name__,
                              obj.id), models.storage.all().keys())
        new_file_storage = FileStorage()
        back_up, FileStorage._FileStorage__objects\
            = FileStorage._FileStorage__objects, {}
        dictionary = {}
        for value in classes:
            with self.subTest(value=value):
                new_instance = value()
                key = f"{new_instance.__class__.__name__}.{new_instance.id}"
                new_file_storage.new(new_instance)
                dictionary[key] = new_instance
                self.assertEqual(
                    dictionary, new_file_storage._FileStorage__objects)
        FileStorage._FileStorage__objects = back_up

    def test_new_without_args(self):
        """[Testing when not arguments provided]"""
        for value in classes:
            with self.subTest(value):
                with self.assertRaises(TypeError):
                    models.storage.new(value(), '10')

    def test_new_With_None(self):
        """[Testing when is provided a None to .all method]
        """
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_save(self):
        """[Test implementation of save after new]
        """
        for value in classes:
            with self.subTest(value=value):
                obj = value()
                models.storage.new(obj)
                models.storage.save()
                with open("file.json", mode="r", encoding="utf-8") as f:
                    read_1 = f.read()
                    self.assertIn("{}.{}".format(
                        obj.__class__.__name__, obj.id), read_1)
        os.remove("file.json")
        new_file_storage = FileStorage()
        dictionary = {}
        for value in classes:
            obj = value()
            dictionary["{}.{}".format(obj.__class__.__name__, obj.id)] = obj

        back_up, FileStorage._FileStorage__objects =\
            FileStorage._FileStorage__objects, dictionary
        new_file_storage.save()
        FileStorage._FileStorage__objects = back_up
        for key, value in dictionary.items():
            dictionary[key] = value.to_dict()
        content = json.dumps(dictionary)
        with open("file.json", mode="r", encoding="utf-8")as f:
            json_string = f.read()
        self.assertEqual(json.loads(content), json.loads(json_string))

    def test_save_With_None(self):
        """[Test when is provided a None to .save method]
        """
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        """[Test implementation of reload after new + save]
        """
        for value in classes:
            with self.subTest(value=value):
                obj = value()
                models.storage.new(obj)
                models.storage.save()
                models.storage.reload()
                objects = FileStorage._FileStorage__objects
                self.assertIn("{}.{}".format(
                    obj.__class__.__name__, obj.id), objects)

    def test_reload_With_None(self):
        """[Test when is provided a None to .save method]
        """
        with self.assertRaises(TypeError):
            models.storage.reload(None)
