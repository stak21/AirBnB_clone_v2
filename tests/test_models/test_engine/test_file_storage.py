#!/usr/bin/python3
"""test for file storage"""
import unittest
from unittest.mock import patch
from io import StringIO
import pep8
import json
import os
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    '''this will test the FileStorage'''

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.user = User()
        cls.user.first_name = "Kev"
        cls.user.last_name = "Yo"
        cls.user.email = "1234@yahoo.com"
        cls.storage = FileStorage()
        cls.console = HBNBCommand()

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.user
        del cls.console

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    @staticmethod
    def remove_all():
        """Function to remove all items from storage"""
        storage = FileStorage()
        objects = storage.all()
        objects = list(objects.values())

        for element in objects:
            storage.delete(element)
        objects = storage.all()

    def test_pep8_FileStorage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    @unittest.skipIf('HBNB_TYPE_STORAGE' in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] == 'db', 'These tests\
                     are valid for file storage class only')
    def test_all(self):
        """tests if all works in File Storage"""
        storage = FileStorage()
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage._FileStorage__objects)

    @unittest.skipIf('HBNB_TYPE_STORAGE' in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] == 'db', 'These tests\
                     are valid for file storage class only')
    def test_all_class(self):
        """tests if all will return specified class objects in File Storage"""
        storage = FileStorage()
        obj = storage.all(User)
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIsNot(obj, {})
        self.assertIsNot(obj, storage._FileStorage__objects)

    @unittest.skipIf('HBNB_TYPE_STORAGE' in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] == 'db', 'These tests\
                     are valid for file storage class only')
    def test_all_unknown_class(self):
        """ tests for invalid classes when calling all """
        storage = FileStorage()
        with self.assertRaises(NameError):
            storage.all(dog)

    @unittest.skipIf('HBNB_TYPE_STORAGE' in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] == 'db', 'These tests\
                     are valid for file storage class only')
    def test_new(self):
        """test when new is created"""
        storage = FileStorage()
        obj = storage.all()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    @unittest.skipIf('HBNB_TYPE_STORAGE' in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] == 'db', 'These tests\
                     are valid for file storage class only')
    def test_delete(self):
        """ Tests delete method to delete objects in __object """
        storage = FileStorage()
        obj_dict = storage.all()
        usr = User()
        usr.id = 12345
        storage.new(usr)
        storage.delete(usr)
        key = usr.__class__.__name__ + "." + str(usr.id)
        self.assertFalse(key in obj_dict.keys())

    @unittest.skipIf('HBNB_TYPE_STORAGE' in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] == 'db', 'These tests\
                     are valid for file storage class only')
    def test_reload_filestorage(self):
        """
        tests reload
        """
        self.storage.save()
        Root = os.path.dirname(os.path.abspath("console.py"))
        path = os.path.join(Root, "file.json")
        with open(path, 'r') as f:
            lines = f.readlines()
        try:
            os.remove(path)
        except:
            pass
        self.storage.save()
        with open(path, 'r') as f:
            lines2 = f.readlines()
        self.assertEqual(lines, lines2)
        try:
            os.remove(path)
        except:
            pass
        with open(path, "w") as f:
            f.write("{}")
        with open(path, "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(self.storage.reload(), None)

    @unittest.skipIf('HBNB_TYPE_STORAGE' in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] == 'db', 'These tests\
                     are valid for file storage class only')
    def test_create_valid_str(self):
        """Tests do_create method in console when given valid str input"""
        storage = FileStorage()
        tests = ['new', 'new\\\"', '\\\"', 'My_little_house', '""', '____']
        expected = ['new', 'new"', '"', 'My little house', '', '    ']

        for i in range(len(tests)):
            self.remove_all()
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(
                    'create BaseModel test_var="{}"'.format(tests[i]))
            attributes = list(storage.all().values())
            actual = attributes[0].test_var
            self.assertEqual(expected[i], actual)
            self.assertEqual(str, type(actual))

    @unittest.skipIf('HBNB_TYPE_STORAGE' in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] == 'db', 'These tests\
                     are valid for file storage class only')
    def test_create_invalid_str(self):
        """Tests that variable is not created when given invalid str input"""
        storage = FileStorage()
        tests = ['"', 'Hi "', '"Hi', '\"']

        for test in tests:
            self.remove_all()
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(
                    'create BaseModel test_var={}'.format(test))
            attributes = list(storage.all().values())
            self.assertFalse('test_var' in attributes[0].to_dict())

    @unittest.skipIf('HBNB_TYPE_STORAGE' in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] == 'db', 'These tests\
                     are valid for file storage class only')
    def test_create_valid_int(self):
        """Tests do_create method in console when given valid integer input"""
        storage = FileStorage()
        tests = [9, 12, 10000]
        expected = [9, 12, 10000]

        for i in range(len(tests)):
            self.remove_all()
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(
                    'create BaseModel test_var={}'.format(tests[i]))
            attributes = list(storage.all().values())
            actual = attributes[0].test_var
            self.assertEqual(expected[i], actual)
            self.assertEqual(int, type(actual))

    @unittest.skipIf('HBNB_TYPE_STORAGE' in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] == 'db', 'These tests\
                     are valid for file storage class only')
    def test_create_invalid_int(self):
        """Tests do_create method in console when given invalid integers"""
        storage = FileStorage()
        tests = ['9.a', '90ab10', '90.b1']

        for test in tests:
            self.remove_all()
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(
                    'create BaseModel test_var={}'.format(test))
            attributes = list(storage.all().values())
            self.assertFalse('test_var' in attributes[0].to_dict())

    @unittest.skipIf('HBNB_TYPE_STORAGE' in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] == 'db', 'These tests\
                     are valid for file storage class only')
    def test_create_valid_float(self):
        """Tests do_create method in console when given valid float values"""
        storage = FileStorage()
        tests = [9.124, 90.24, 90.0, 90.]
        expected = [9.124, 90.24, 90.0, 90.0]

        for i in range(len(tests)):
            self.remove_all()
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(
                    'create BaseModel test_var={}'.format(tests[i]))
            attributes = list(storage.all().values())
            actual = attributes[0].test_var
            self.assertEqual(expected[i], actual)
            self.assertEqual(float, type(actual))


if __name__ == "__main__":
    unittest.main()
