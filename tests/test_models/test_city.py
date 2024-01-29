#!/usr/bin/python3

"""[Unittest for city]
    """
from datetime import date, datetime
from unittest import TestCase
from models import city
import uuid
import pycodestyle
City = city.City


class Test_style(TestCase):
    """[Class created to test style and syntax requirements for the
    city class]
    """

    def test_pycode(self):
        """[Function that check Syntax from Peep8 branch called pycodestyle]
        """
        foo = pycodestyle.StyleGuide(quiet=True).check_files([
            'models/city.py'])
        self.assertEqual(foo.total_errors, 0,
                         "Found code style error (and warnings).")


class Test_city(TestCase):
    """[Class for testing all the function of city class]
    """
    @classmethod
    def setUpClass(cls):
        """Setting up a test object"""
        cls.city1 = City()

    def test_empty_city(self):
        """[Testing if instance is correcty related]
        """
        self.assertIsNotNone(self.city1)
        self.assertIsInstance(self.city1, City)

    def test_id_value(self):
        """[Cheking if id is an uuid version 4]
        """
        city_test2 = City(id='1')
        with self.assertRaises(ValueError) as _:
            uuid.UUID(city_test2.id, version=4)
        city_test3 = City(id=['1'])
        with self.assertRaises(AttributeError) as _:
            uuid.UUID(city_test3.id, version=4)

    def test_dates(self):
        """[Cheking dates are correctly created]
        """
        self.assertIsInstance(self.city1.created_at, datetime)
        self.assertIsInstance(self.city1.updated_at, datetime)

    def test__str__(self):
        """[Cheking correct output when printing]"""
        id1 = self.city1.id
        self.assertTrue(f'[City] ({id1})' in str(self.city1))

    def test_save(self):
        """Checks if updated_at is changed with save method"""
        self.city1.save()
        self.assertNotEqual(self.city1.updated_at,
                            self.city1.created_at)

    def test_to_dict(self):
        """Checks to_dict method"""
        city_test4 = City()
        dict_city4 = city_test4.to_dict()
        self.assertIsInstance(dict_city4, dict)
        self.assertIsInstance(dict_city4['created_at'], str)
        self.assertIsInstance(dict_city4['updated_at'], str)

    def test_attributes(self):
        """Checks correct attributes assignment"""
        city5 = City(state_id=123)
        city5.name = "Cali"
        self.assertEqual(city5.state_id, 123)
        self.assertEqual(city5.name, 'Cali')

    def test_creating_with_kwargs(self):
        """[Checking creation with kwargs]"""
        obj = City()
        dictionary = obj.to_dict()
        new_date = datetime.today()
        new_date_iso = new_date.isoformat()
        dictionary["created_at"] = new_date_iso
        dictionary["updated_at"] = new_date_iso
        id = dictionary["id"]
        obj = City(**dictionary)
        self.assertEqual(obj.id, id)
        self.assertEqual(obj.created_at, new_date)
        self.assertEqual(obj.updated_at, new_date)

    def test_save_with_file(self):
        """ Checks if the generated key is saved in the json file"""
        obj = City()
        obj.save()
        key_id = f"City.{obj.id}"
        with open("file.json", mode="r", encoding="utf-8") as f:
            self.assertIn(key_id, f.read())
