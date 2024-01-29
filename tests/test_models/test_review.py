#!/usr/bin/python3

"""[Unittest for review]
    """
from datetime import date, datetime
from unittest import TestCase
from models import review
import uuid
import pycodestyle
Review = review.Review


class Test_style(TestCase):
    """[Class created to test style and syntax requirements for the
    review class]
    """

    def test_pycode(self):
        """[Function that check Syntax from Peep8 branch called pycodestyle]
        """
        foo = pycodestyle.StyleGuide(quiet=True).check_files([
            'models/review.py'])
        self.assertEqual(foo.total_errors, 0,
                         "Found code style error (and warnings).")


class Test_review(TestCase):
    """[Class for testing all the function of review class]
    """
    @classmethod
    def setUpClass(cls):
        """Setting up a test object"""
        cls.review1 = Review()

    def test_empty_review(self):
        """[Testing if instance is correcty related]
        """
        self.assertIsNotNone(self.review1)
        self.assertIsInstance(self.review1, Review)

    def test_id_value(self):
        """[Cheking if id is an uuid version 4]
        """
        review_test2 = Review(id='1')
        with self.assertRaises(ValueError) as _:
            uuid.UUID(review_test2.id, version=4)
        review_test3 = Review(id=['1'])
        with self.assertRaises(AttributeError) as _:
            uuid.UUID(review_test3.id, version=4)

    def test_dates(self):
        """[Cheking dates are correctly created]
        """
        self.assertIsInstance(self.review1.created_at, datetime)
        self.assertIsInstance(self.review1.updated_at, datetime)

    def test__str__(self):
        """[Cheking correct output when printing]"""
        id1 = self.review1.id
        self.assertTrue(f'[Review] ({id1})' in str(self.review1))

    def test_save(self):
        """Checks if updated_at is changed with save method"""
        self.review1.save()
        self.assertNotEqual(self.review1.updated_at,
                            self.review1.created_at)

    def test_to_dict(self):
        """Checks to_dict method"""
        review_test4 = Review()
        dict_review4 = review_test4.to_dict()
        self.assertIsInstance(dict_review4, dict)
        self.assertIsInstance(dict_review4['created_at'], str)
        self.assertIsInstance(dict_review4['updated_at'], str)

    def test_attributes(self):
        """Checks correct attributes assignment"""
        review5 = Review(place_id=123)
        review5.user_id = 456
        review5.text = 'hello world'
        self.assertEqual(review5.place_id, 123)
        self.assertEqual(review5.user_id, 456)
        self.assertEqual(review5.text, 'hello world')

    def test_creating_with_kwargs(self):
        """[Checking creation with kwargs]"""
        obj = Review()
        dictionary = obj.to_dict()
        new_date = datetime.today()
        new_date_iso = new_date.isoformat()
        dictionary["created_at"] = new_date_iso
        dictionary["updated_at"] = new_date_iso
        id = dictionary["id"]
        obj = Review(**dictionary)
        self.assertEqual(obj.id, id)
        self.assertEqual(obj.created_at, new_date)
        self.assertEqual(obj.updated_at, new_date)

    def test_save_with_file(self):
        """ Checks if the generated key is saved in the json file"""
        obj = Review()
        obj.save()
        key_id = f"Review.{obj.id}"
        with open("file.json", mode="r", encoding="utf-8") as f:
            self.assertIn(key_id, f.read())
