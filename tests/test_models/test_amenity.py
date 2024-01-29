#!/usr/bin/python3

"""[Unittest for amenity]
    """
from datetime import date, datetime
from unittest import TestCase
from models import amenity
import uuid
import pycodestyle
Amenity = amenity.Amenity


class Test_style(TestCase):
    """[Class created to test style and syntax requirements for the
    amenity class]
    """

    def test_pycode(self):
        """[Function that check Syntax from Peep8 branch called pycodestyle]
        """
        foo = pycodestyle.StyleGuide(quiet=True).check_files([
            'models/amenity.py'])
        self.assertEqual(foo.total_errors, 0,
                         "Found code style error (and warnings).")


class Test_amenity(TestCase):
    """[Class for testing all the function of amenity class]
    """
    @classmethod
    def setUpClass(cls):
        """Setting up a test object"""
        cls.amenity1 = Amenity()

    def test_empty_amenity(self):
        """[Testing if instance is correcty related]
        """
        self.assertIsNotNone(self.amenity1)
        self.assertIsInstance(self.amenity1, Amenity)

    def test_id_value(self):
        """[Cheking if id is an uuid version 4]
        """
        amenity_test2 = Amenity(id='1')
        with self.assertRaises(ValueError) as _:
            uuid.UUID(amenity_test2.id, version=4)
        amenity_test3 = Amenity(id=['1'])
        with self.assertRaises(AttributeError) as _:
            uuid.UUID(amenity_test3.id, version=4)

    def test_dates(self):
        """[Cheking dates are correctly created]
        """
        self.assertIsInstance(self.amenity1.created_at, datetime)
        self.assertIsInstance(self.amenity1.updated_at, datetime)

    def test__str__(self):
        """[Cheking correct output when printing]"""
        id1 = self.amenity1.id
        self.assertTrue(f'[Amenity] ({id1})' in str(self.amenity1))

    def test_save(self):
        """Checks if updated_at is changed with save method"""
        self.amenity1.save()
        self.assertNotEqual(self.amenity1.updated_at,
                            self.amenity1.created_at)

    def test_to_dict(self):
        """Checks to_dict method"""
        amenity_test4 = Amenity()
        dict_amenity4 = amenity_test4.to_dict()
        self.assertIsInstance(dict_amenity4, dict)
        self.assertIsInstance(dict_amenity4['created_at'], str)
        self.assertIsInstance(dict_amenity4['updated_at'], str)

    def test_attributes(self):
        """Checks correct attributes assignment"""
        amenity5 = Amenity(name='Towels')
        self.assertEqual(amenity5.name, 'Towels')

    def test_creating_with_kwargs(self):
        """[Checking creation with kwargs]"""
        obj = Amenity()
        dictionary = obj.to_dict()
        new_date = datetime.today()
        new_date_iso = new_date.isoformat()
        dictionary["created_at"] = new_date_iso
        dictionary["updated_at"] = new_date_iso
        id = dictionary["id"]
        obj = Amenity(**dictionary)
        self.assertEqual(obj.id, id)
        self.assertEqual(obj.created_at, new_date)
        self.assertEqual(obj.updated_at, new_date)

    def test_save_with_file(self):
        """ Checks if the generated key is saved in the json file"""
        obj = Amenity()
        obj.save()
        key_id = f"Amenity.{obj.id}"
        with open("file.json", mode="r", encoding="utf-8") as f:
            self.assertIn(key_id, f.read())
