#!/usr/bin/python3

"""[Unittest for base_model]
    """
from datetime import date, datetime
from unittest import TestCase
from models import base_model
import uuid
import pycodestyle
BaseModel = base_model.BaseModel


class Test_style(TestCase):
    """[Class created to test style and syntax requirements for the
    base_model class]
    """

    def test_pycode(self):
        """[Function that check Syntax from Peep8 branch called pycodestyle]
        """
        foo = pycodestyle.StyleGuide(quiet=True).check_files([
            'models/base_model.py'])
        self.assertEqual(foo.total_errors, 0,
                         "Found code style error (and warnings).")


class Test_base(TestCase):
    """[Class for testing all the function of base class]
    """
    @classmethod
    def setUpClass(cls):
        """Setting up a test object"""
        cls.base_test1 = BaseModel()

    def test_empty_base(self):
        """[Testing if instance is correcty related]
        """
        self.assertIsNotNone(self.base_test1)
        self.assertIsInstance(self.base_test1, BaseModel)

    def test_id_value(self):
        """[Cheking if id is an uuid version 4]
        """
        base_test2 = BaseModel(id='1')
        with self.assertRaises(ValueError) as _:
            uuid.UUID(base_test2.id, version=4)
        base_test3 = BaseModel(id=['1'])
        with self.assertRaises(AttributeError) as _:
            uuid.UUID(base_test3.id, version=4)

    def test_dates(self):
        """[Cheking dates are correctly created]
        """
        self.assertIsInstance(self.base_test1.created_at, datetime)
        self.assertIsInstance(self.base_test1.updated_at, datetime)

    def test__str__(self):
        """[Cheking correct output when printing]"""
        id1 = self.base_test1.id
        self.assertTrue(f'[BaseModel] ({id1})' in str(self.base_test1))

    def test_creating_with_kwargs(self):
        """[Checking creation with kwargs]"""
        obj = BaseModel()
        dictionary = obj.to_dict()
        new_date = datetime.today()
        new_date_iso = new_date.isoformat()
        dictionary["created_at"] = new_date_iso
        dictionary["updated_at"] = new_date_iso
        id = dictionary["id"]
        obj = BaseModel(**dictionary)
        self.assertEqual(obj.id, id)
        self.assertEqual(obj.created_at, new_date)
        self.assertEqual(obj.updated_at, new_date)

    def test_save(self):
        """Checks if updated_at is changed with save method"""
        self.base_test1.save()
        self.assertNotEqual(self.base_test1.updated_at,
                            self.base_test1.created_at)

    def test_save_with_file(self):
        """ Checks if the generated key is saved in the json file"""
        obj = BaseModel()
        obj.save()
        key_id = f"BaseModel.{obj.id}"
        with open("file.json", mode="r", encoding="utf-8") as f:
            self.assertIn(key_id, f.read())

    def test_to_dict(self):
        """Checks to_dict method"""
        base_test4 = BaseModel()
        dict_base4 = base_test4.to_dict()
        self.assertIsInstance(dict_base4, dict)
        self.assertIsInstance(dict_base4['created_at'], str)
        self.assertIsInstance(dict_base4['updated_at'], str)
