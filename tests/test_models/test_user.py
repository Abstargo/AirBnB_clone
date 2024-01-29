#!/usr/bin/python3

"""[Unittest for user]
    """
from datetime import date, datetime
from unittest import TestCase
from models import user
import uuid
import pycodestyle
User = user.User


class Test_style(TestCase):
    """[Class created to test style and syntax requirements for the
    user class]
    """

    def test_pycode(self):
        """[Function that check Syntax from Peep8 branch called pycodestyle]
        """
        foo = pycodestyle.StyleGuide(quiet=True).check_files([
            'models/user.py'])
        self.assertEqual(foo.total_errors, 0,
                         "Found code style error (and warnings).")


class Test_base(TestCase):
    """[Class for testing all the function of user class]
    """
    @classmethod
    def setUpClass(cls):
        """Setting up a test object"""
        cls.user1 = User()

    def test_user_creation(self):
        """[Testing if instance is correcty related]
        """
        self.assertIsNotNone(self.user1)
        self.assertIsInstance(self.user1, User)

    def test_id_value(self):
        """[Cheking if id is an uuid version 4]
        """
        user2 = User(id='1')
        with self.assertRaises(ValueError) as _:
            uuid.UUID(user2.id, version=4)
        user3 = User(id=['1'])
        with self.assertRaises(AttributeError) as _:
            uuid.UUID(user3.id, version=4)

    def test_dates(self):
        """[Cheking dates are correctly created]
        """
        self.assertIsInstance(self.user1.created_at, datetime)
        self.assertIsInstance(self.user1.updated_at, datetime)

    def test__str__(self):
        """[Cheking correct output when printing]"""
        id1 = self.user1.id
        self.assertTrue(f'[User] ({id1})' in str(self.user1))

    def test_save(self):
        """Checks if updated_at is changed with save method"""
        self.user1.save()
        self.assertNotEqual(self.user1.updated_at,
                            self.user1.created_at)

    def test_to_dict(self):
        """Checks to_dict method"""
        user4 = User()
        dict_user4 = user4.to_dict()
        self.assertIsInstance(dict_user4, dict)
        self.assertIsInstance(dict_user4['created_at'], str)
        self.assertIsInstance(dict_user4['updated_at'], str)

    def test_attributes(self):
        """Checks correct attributes assignment"""
        user5 = User(email="abc@email.com")
        user5.password = 123
        user5.first_name = "Jane"
        user5.last_name = "Foster"
        self.assertEqual(user5.email, "abc@email.com")
        self.assertEqual(user5.password, 123)
        self.assertEqual(user5.first_name, "Jane")
        self.assertEqual(user5.last_name, "Foster")

    def test_creating_with_kwargs(self):
        """[Checking creation with kwargs]"""
        obj = User()
        dictionary = obj.to_dict()
        new_date = datetime.today()
        new_date_iso = new_date.isoformat()
        dictionary["created_at"] = new_date_iso
        dictionary["updated_at"] = new_date_iso
        id = dictionary["id"]
        obj = User(**dictionary)
        self.assertEqual(obj.id, id)
        self.assertEqual(obj.created_at, new_date)
        self.assertEqual(obj.updated_at, new_date)

    def test_save_with_file(self):
        """ Checks if the generated key is saved in the json file"""
        obj = User()
        obj.save()
        key_id = f"User.{obj.id}"
        with open("file.json", mode="r", encoding="utf-8") as f:
            self.assertIn(key_id, f.read())
