#!/usr/bin/python3

"""[Unittest for place]
    """
from datetime import date, datetime
from unittest import TestCase
from models import place
import uuid
import pycodestyle
Place = place.Place


class Test_style(TestCase):
    """[Class created to test style and syntax requirements for the
    place class]
    """

    def test_pycode(self):
        """[Function that check Syntax from Peep8 branch called pycodestyle]
        """
        foo = pycodestyle.StyleGuide(quiet=True).check_files([
            'models/place.py'])
        self.assertEqual(foo.total_errors, 0,
                         "Found code style error (and warnings).")


class Test_place(TestCase):
    """[Class for testing all the function of place class]
    """
    @classmethod
    def setUpClass(cls):
        """Setting up a test object"""
        cls.place1 = Place()

    def test_empty_place(self):
        """[Testing if instance is correcty related]
        """
        self.assertIsNotNone(self.place1)
        self.assertIsInstance(self.place1, Place)

    def test_id_value(self):
        """[Cheking if id is an uuid version 4]
        """
        place_test2 = Place(id='1')
        with self.assertRaises(ValueError) as _:
            uuid.UUID(place_test2.id, version=4)
        place_test3 = Place(id=['1'])
        with self.assertRaises(AttributeError) as _:
            uuid.UUID(place_test3.id, version=4)

    def test_dates(self):
        """[Cheking dates are correctly created]
        """
        self.assertIsInstance(self.place1.created_at, datetime)
        self.assertIsInstance(self.place1.updated_at, datetime)

    def test__str__(self):
        """[Cheking correct output when printing]"""
        id1 = self.place1.id
        self.assertTrue(f'[Place] ({id1})' in str(self.place1))

    def test_save(self):
        """Checks if updated_at is changed with save method"""
        self.place1.save()
        self.assertNotEqual(self.place1.updated_at,
                            self.place1.created_at)

    def test_to_dict(self):
        """Checks to_dict method"""
        place_test4 = Place()
        dict_place4 = place_test4.to_dict()
        self.assertIsInstance(dict_place4, dict)
        self.assertIsInstance(dict_place4['created_at'], str)
        self.assertIsInstance(dict_place4['updated_at'], str)

    def test_attributes(self):
        """Checks correct attributes assignment"""
        place5 = Place(city_id=123)
        place5.user_id = 456
        place5.name = "Casa1"
        place5.description = "Big"
        place5.number_rooms = 5
        place5.number_bathrooms = 6
        place5.max_guest = 10
        place5.price_by_night = 25
        place5.latitude = 0.5
        place5.longitude = 1.45
        self.assertEqual(place5.city_id, 123)
        self.assertEqual(place5.name, 'Casa1')
        self.assertEqual(place5.description, 'Big')
        self.assertEqual(place5.number_rooms, 5)
        self.assertEqual(place5.number_bathrooms, 6)
        self.assertEqual(place5.max_guest, 10)
        self.assertEqual(place5.price_by_night, 25)
        self.assertEqual(place5.latitude, 0.5)
        self.assertEqual(place5.longitude, 1.45)

    def test_creating_with_kwargs(self):
        """[Checking creation with kwargs]"""
        obj = Place()
        dictionary = obj.to_dict()
        new_date = datetime.today()
        new_date_iso = new_date.isoformat()
        dictionary["created_at"] = new_date_iso
        dictionary["updated_at"] = new_date_iso
        id = dictionary["id"]
        obj = Place(**dictionary)
        self.assertEqual(obj.id, id)
        self.assertEqual(obj.created_at, new_date)
        self.assertEqual(obj.updated_at, new_date)

    def test_save_with_file(self):
        """ Checks if the generated key is saved in the json file"""
        obj = Place()
        obj.save()
        key_id = f"Place.{obj.id}"
        with open("file.json", mode="r", encoding="utf-8") as f:
            self.assertIn(key_id, f.read())
