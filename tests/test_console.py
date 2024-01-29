#!/usr/bin/python3
"""[Unittest for base_model]"""
from unittest import TestCase
from models import storage
from models.base_model import BaseModel
import console
import pycodestyle
from unittest.mock import patch
from io import StringIO
import os
from models.engine.file_storage import FileStorage

classes = {'BaseModel', 'User', 'Place', 'State', 'City', 'Amenity', 'Review'}


class Test_style(TestCase):
    """[Class created to test style and syntax requirements for the
    console]
    """

    def test_pycode(self):
        """[Function that check Syntax from Peep8 branch called pycodestyle]
        """
        foo = pycodestyle.StyleGuide(quiet=True).check_files([
            'console.py'])
        self.assertEqual(foo.total_errors, 0,
                         "Found code style error (and warnings).")


class Test_console(TestCase):
    """[Class for testing console]"""

    def test_docstring(self):
        """Cheking docstring of console"""
        self.assertTrue(len(console.__doc__) >= 1)

    def test_emptyline(self):
        """Testing empty line output"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(console.HBNBCommand().onecmd(""))
            self.assertEqual(f.getvalue().strip(), '')

    def test_prompt(self):
        """[Testing prompt]"""
        self.assertEqual("(hbnb) ", console.HBNBCommand.prompt)

    def test_quit(self):
        """Testing quit method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(console.HBNBCommand().onecmd("quit"))
            self.assertEqual(f.getvalue(), '')

    def test_EOF(self):
        """Testing EOF method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(console.HBNBCommand().onecmd("EOF"))
            self.assertEqual(f.getvalue(), '\n')

    def test_all(self):
        """Testing all method"""
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("all BaseModel")
            self.assertIn('["[BaseModel] (', f.getvalue())

    def test_create(self):
        """Testing create method"""
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("create BaseModel")
        key_id = 'BaseModel.' + f.getvalue().split('\n')[0]
        objects = storage.all()
        self.assertIn(key_id, objects)

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("create")
        self.assertEqual(f.getvalue(), "** class name missing **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("create whatever")
        self.assertEqual(f.getvalue(), "** class doesn't exist **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(console.HBNBCommand().onecmd("invalid.create()"))
            self.assertEqual(f.getvalue().strip(), "")

        for value in classes:
            with self.subTest(value=value):
                with patch('sys.stdout', new=StringIO()) as f:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"{value}.create()"))
                    self.assertEqual(f.getvalue().strip(), "")

    def test_show(self):
        """Testing show method"""
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("show")
        self.assertEqual(f.getvalue(), "** class name missing **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("show whatever")
        self.assertEqual(f.getvalue(), "** class doesn't exist **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("show BaseModel")
        self.assertEqual(f.getvalue(), "** instance id missing **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("show BaseModel 123")
        self.assertEqual(f.getvalue(), "** no instance found **\n")

        base1 = BaseModel()
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("show BaseModel " + base1.id)
        base1_str = "[BaseModel] ({})".format(base1.id)
        self.assertIn(base1_str, f.getvalue())

    def test_destroy(self):
        """Test for destroy method"""
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("destroy")
        self.assertEqual(f.getvalue(), "** class name missing **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("destroy whatever")
        self.assertEqual(f.getvalue(), "** class doesn't exist **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("destroy BaseModel")
        self.assertEqual(f.getvalue(), "** instance id missing **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("destroy BaseModel 123")
        self.assertEqual(f.getvalue(), "** no instance found **\n")

    def test_update(self):
        """Test for update method"""
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("update")
        self.assertEqual(f.getvalue(), "** class name missing **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("update whatever")
        self.assertEqual(f.getvalue(), "** class doesn't exist **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("update BaseModel")
        self.assertEqual(f.getvalue(), "** instance id missing **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("update BaseModel 123")
        self.assertEqual(f.getvalue(), "** no instance found **\n")

        b2 = BaseModel()
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("update BaseModel {}".format(b2.id))
        self.assertEqual(f.getvalue(), "** attribute name missing **\n")

        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd(
                "update BaseModel {} name".format(b2.id))
        self.assertEqual(f.getvalue(), "** value missing **\n")

    def test_count(self):
        """Testing count method"""
        counter = 0
        for obj in storage.all().values():
            if "BaseModel" == obj.__class__.__name__:
                counter += 1
        with patch('sys.stdout', new=StringIO()) as f:
            console.HBNBCommand().onecmd("count BaseModel")
        self.assertEqual(f.getvalue(), str(counter) + '\n')


class Test_console_command_help(TestCase):
    """[Unnitest HBnB console dedicated to help function]
    """

    def test_help_method(self):
        """[Testing help]
        """
        expected = """Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update"""
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(console.HBNBCommand().onecmd("help"))
            self.assertEqual(o.getvalue().strip(), expected)

    def test_help_quit_method(self):
        """[Testing help EOF]
        """
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(console.HBNBCommand().onecmd("help EOF"))
            self.assertEqual(o.getvalue().strip(),
                             "exits the program with a new line printed")

    def test_help_all_method(self):
        """[Testing help all]
        """
        e = """Prints all string representation of all instances based
        or not on the class name. Ex: $ all BaseModel or $ all."""
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(console.HBNBCommand().onecmd("help all"))
            self.assertEqual(o.getvalue().strip(), e)

    def test_help_count_method(self):
        """[Testing help count]
        """
        e = """[ retrieve the number of instances of a class:
        <class name>.count().]"""
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(console.HBNBCommand().onecmd("help count"))
            self.assertEqual(o.getvalue().strip(), e)

    def test_help_create_method(self):
        """[Testing help create]
        """
        e = """Create an instance of given class, prints its id and saves
        it into de json file"""
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(console.HBNBCommand().onecmd("help create"))
            self.assertEqual(o.getvalue().strip(), e.strip())

    def test_help_destroy_method(self):
        """[Testing help destroy]
        """
        e = """Deletes an instance based on its id"""
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(console.HBNBCommand().onecmd("help destroy"))
            self.assertEqual(o.getvalue().strip(), e.strip())

    def test_help_help_method(self):
        """[Testing help help]
        """
        e = """List available commands with "help" """
        e += """or detailed help with "help cmd"."""
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(console.HBNBCommand().onecmd("help help"))
            self.assertEqual(o.getvalue().strip(), e.strip())

    def test_help_quit_method(self):
        """[Testing help quit]
        """
        e = """exits the program"""
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(console.HBNBCommand().onecmd("help quit"))
            self.assertEqual(o.getvalue().strip(), e.strip())

    def test_help_show_method(self):
        """[Testing help show]
        """
        e = """Prints the string representation of an instance
        based on the class name and id"""
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(console.HBNBCommand().onecmd("help show"))
            self.assertEqual(o.getvalue().strip(), e.strip())

    def test_help_update_method(self):
        """[Testing help update]
        """
        e = """Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file)."""
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(console.HBNBCommand().onecmd("help update"))
            self.assertEqual(o.getvalue().strip(), e.strip())

    def test_help_none_implemented_method(self):
        """[Testing help none_implemented]
        """
        e = """*** No help on lkdfdfgjk"""
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(console.HBNBCommand().onecmd("help lkdfdfgjk"))
            self.assertEqual(o.getvalue().strip(), e.strip())


class Test_console_method_all(TestCase):
    """[Unnitest HBnB console dedicated to all function]
    """
    @classmethod
    def setUpClass(cls) -> None:
        try:
            os.rename("file.json", "back_up")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("back_up", "file.json")
        except IOError:
            pass

    def test_all_method(self):
        """[Testing all method]
        """
        with patch("sys.stdout", new=StringIO())as o:
            for value in classes:
                with self.subTest(value=value):
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"create {value}"))
        with patch("sys.stdout", new=StringIO())as o:
            for value in classes:
                with self.subTest(value=value):
                    self.assertFalse(console.HBNBCommand().onecmd("all"))
                    self.assertIn(value, o.getvalue().strip())

    def test_all_method_dot(self):
        """[Testing all method .]
        """
        with patch("sys.stdout", new=StringIO())as o:
            for value in classes:
                with self.subTest(value=value):
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"create {value}"))
        with patch("sys.stdout", new=StringIO())as o:
            for value in classes:
                with self.subTest(value=value):
                    self.assertFalse(console.HBNBCommand().onecmd(".all()"))
                    self.assertIn(value, o.getvalue().strip())

    def test_all_method_by_class(self):
        """[Testing all method by each class]
        """
        with patch("sys.stdout", new=StringIO())as o:
            for value in classes:
                with self.subTest(value=value):
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"create {value}"))
        with patch("sys.stdout", new=StringIO())as o:
            for value in classes:
                with self.subTest(value=value):
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"all {value}"))
                    self.assertIn(value, o.getvalue().strip())
                    self.assertNotIn("Another", o.getvalue().strip())

    def test_all_method_by_class_dot(self):
        """[Testing all method by each class .]
        """
        with patch("sys.stdout", new=StringIO())as o:
            for value in classes:
                with self.subTest(value=value):
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"create {value}"))
        with patch("sys.stdout", new=StringIO())as o:
            for value in classes:
                with self.subTest(value=value):
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"{value}.all()"))
                    self.assertIn(value, o.getvalue().strip())
                    self.assertNotIn("Another", o.getvalue().strip())


class Test_console_method_count(TestCase):
    """[Unnitest HBnB console dedicated to count function]
    """
    @classmethod
    def setUpClass(cls) -> None:
        try:
            os.rename("file.json", "back_up")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("back_up", "file.json")
        except IOError:
            pass

    def test_count_method_valid_class(self):
        """[Testing method count with valid class]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"create {value}"))
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"{value}.count()"))
                    self.assertEqual(o.getvalue().strip(), "1")

    def test_count_method_invalid_class(self):
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(console.HBNBCommand().onecmd("Invalid.count()"))
            self.assertEqual(o.getvalue().strip(), "0")


class Test_console_method_create(TestCase):
    """[Unnitest HBnB console dedicated to create function]
    """
    @classmethod
    def setUpClass(cls) -> None:
        try:
            os.rename("file.json", "back_up")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("back_up", "file.json")
        except IOError:
            pass

    def test_create_method(self):
        """Testing method create with valid classes"""
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"create {value}"))
                    key = f"{value}.{o.getvalue().strip()}"
                    self.assertNotEqual(25, len(o.getvalue().strip()))
                    self.assertIn(key, storage.all().keys())


class Test_console_method_destroy(TestCase):
    """[Unnitest HBnB console dedicated to destroy function]
    """
    @classmethod
    def setUpClass(cls) -> None:
        try:
            os.rename("file.json", "back_up")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("back_up", "file.json")
        except IOError:
            pass

    def test_destroy_method_missing_id(self):
        """[Testing method destroy with valid classes missing id]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"destroy {value}"))
                    self.assertEqual(
                        "** instance id missing **", o.getvalue().strip())

    def test_destroy_method_with_dot_missing_id(self):
        """[Testing method destroy with valid classes missing id with dot]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"{value}.destroy()"))
                    self.assertEqual(
                        "** instance id missing **", o.getvalue().strip())

    def test_destroy_method_with_invalid_id(self):
        """[Testing method destroy with invalid id with dot]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"destroy {value} 5"))
                    self.assertEqual(
                        "** no instance found **", o.getvalue().strip())

    def test_destroy_method_with_invalid_id_with_dot(self):
        """[Testing method destroy with invalid id with dot]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"{value}.destroy(5)"))
                    self.assertEqual(
                        "** no instance found **", o.getvalue().strip())

    def test_destroy_method_with_invalid_class(self):
        """[Testing method destroy with invalid class]
        """
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(
                console.HBNBCommand().onecmd(f"destroy Another 5"))
            self.assertEqual(
                "** class doesn't exist **", o.getvalue().strip())

    def test_destroy_method_with_invalid_class_with_dot(self):
        """[Testing method destroy with invalid class with dot]
        """
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(
                console.HBNBCommand().onecmd(f"Another.destroy(5)"))
            self.assertEqual(
                "** class doesn't exist **", o.getvalue().strip())

    def test_destroy_method_success(self):
        """[Testing method destroy success]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"create {value}"))
                    id = o.getvalue().strip()
                with patch("sys.stdout", new=StringIO())as o:
                    obj = storage.all()[f"{value}.{id}"]
                    self.assertFalse(console.HBNBCommand().onecmd(
                        f"destroy {value} {id}"))
                    self.assertNotIn(obj, storage.all())

    def test_destroy_method_success_with_dot(self):
        """[Testing method destroy success with dot]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"create {value}"))
                    id = o.getvalue().strip()
                with patch("sys.stdout", new=StringIO())as o:
                    obj = storage.all()[f"{value}.{id}"]
                    self.assertFalse(console.HBNBCommand().onecmd(
                        f"{value}.destroy({id})"))
                    self.assertNotIn(obj, storage.all())


class Test_console_method_destroy(TestCase):
    """[Unnitest HBnB console dedicated to show function]
    """
    @classmethod
    def setUpClass(cls) -> None:
        try:
            os.rename("file.json", "back_up")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("back_up", "file.json")
        except IOError:
            pass

    def test_show_method(self):
        """[Testing method show success]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"create {value}"))
                    id = o.getvalue().strip()
                with patch("sys.stdout", new=StringIO())as o:
                    obj = storage.all()[f"{value}.{id}"]
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"show {value} {id}"))
                    self.assertEqual(obj.__str__(), o.getvalue().strip())

    def test_show_method_with_dot(self):
        """[Testing method show success with dot]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"create {value}"))
                    id = o.getvalue().strip()
                with patch("sys.stdout", new=StringIO())as o:
                    obj = storage.all()[f"{value}.{id}"]
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"{value}.show({id})"))
                    self.assertEqual(obj.__str__(), o.getvalue().strip())

    def test_show_method_not_instance_found(self):
        """[Testing method show with not found instance]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"show {value} 5"))
                    self.assertEqual("** no instance found **",
                                     o.getvalue().strip())

    def test_show_method_not_instance_found_with_dot(self):
        """[Testing method show with not found instance with dot]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"{value}.show(5)"))
                    self.assertEqual("** no instance found **",
                                     o.getvalue().strip())

    def test_show_method_missing_id(self):
        """[Testing method show missing id]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"show {value}"))
                    self.assertEqual("** instance id missing **",
                                     o.getvalue().strip())

    def test_show_method_missing_id_with_dot(self):
        """[Testing method show missing id with dot]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"{value}.show()"))
                    self.assertEqual("** instance id missing **",
                                     o.getvalue().strip())

    def test_show_method_missing_class(self):
        """[Testing method show missing class]
        """
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(
                console.HBNBCommand().onecmd(f"show"))
            self.assertEqual("** class name missing **",
                             o.getvalue().strip())
        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(
                console.HBNBCommand().onecmd(f".show()"))
            self.assertEqual("** class name missing **",
                             o.getvalue().strip())


class Test_console_method_update(TestCase):
    """[Unnitest HBnB console dedicated to update function]
    """
    @classmethod
    def setUpClass(cls) -> None:
        try:
            os.rename("file.json", "back_up")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("back_up", "file.json")
        except IOError:
            pass

    def test_update_method(self):
        """[Testing method update]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"create {value}"))
                    id = o.getvalue().strip()
                self.assertFalse(console.HBNBCommand().onecmd(
                    f"update {value} {id} random_key 'random_value'"))
                dictionary = storage.all()[f"{value}.{id}"].__dict__
                self.assertEqual("random_value", dictionary["random_key"])

        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(
                console.HBNBCommand().onecmd(f"create Place"))
            id = o.getvalue().strip()
        self.assertFalse(console.HBNBCommand().onecmd(
            f"update Place {id} max_guest 150"))
        dictionary = storage.all()[f"Place.{id}"].__dict__
        self.assertEqual(150, dictionary["max_guest"])

        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(
                console.HBNBCommand().onecmd(f"create Place"))
            id = o.getvalue().strip()
        self.assertFalse(console.HBNBCommand().onecmd(
            f"update Place {id} latitude 20.5"))
        dictionary = storage.all()[f"Place.{id}"].__dict__
        self.assertEqual(20.5, dictionary["latitude"])

    def test_update_method_with_dot(self):
        """[Testing method update with dot]
        """
        for value in classes:
            with self.subTest(value=value):
                with patch("sys.stdout", new=StringIO())as o:
                    self.assertFalse(
                        console.HBNBCommand().onecmd(f"create {value}"))
                    id = o.getvalue().strip()
                self.assertFalse(console.HBNBCommand().onecmd(
                    f"{value}.update({id}, random_key, 'random_value')"))
                dictionary = storage.all()[f"{value}.{id}"].__dict__
                self.assertEqual("random_value", dictionary["random_key"])

        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(
                console.HBNBCommand().onecmd(f"create Place"))
            id = o.getvalue().strip()
        self.assertFalse(console.HBNBCommand().onecmd(
            f"Place.update({id}, max_guest, 150)"))
        dictionary = storage.all()[f"Place.{id}"].__dict__
        self.assertEqual(150, dictionary["max_guest"])

        with patch("sys.stdout", new=StringIO())as o:
            self.assertFalse(
                console.HBNBCommand().onecmd(f"create Place"))
            id = o.getvalue().strip()
        self.assertFalse(console.HBNBCommand().onecmd(
            f"Place.update({id}, latitude, 20.5)"))
        dictionary = storage.all()[f"Place.{id}"].__dict__
        self.assertEqual(2.0, dictionary["latitude"])
