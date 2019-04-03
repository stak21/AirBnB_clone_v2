#!/usr/bin/python3
"""test for review"""
import unittest
import os
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.base_model import BaseModel
import pep8


class TestReview(unittest.TestCase):
    """this will test the place class"""

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        from models import storage

        cls.state = State(name="California")
        cls.city = City(name="Los Angeles", state_id=cls.state.id)
        cls.user = User(email="john@snow.com", password="johnpwd")
        cls.place = Place(city_id=cls.city.id, state_id=cls.state.id,
                          name='Death Star', user_id=cls.user.id,
                          description='Unlimited power', number_rooms=12,
                          number_bathrooms=12, max_guest=12, price_by_night=12,
                          latitude=10, longitude=12,
                          )
        cls.rev = Review(place_id=cls.place.id, user_id=cls.user.id,
                         text="The strongest in the galaxy")
        storage.new(cls.state)
        storage.new(cls.city)
        storage.new(cls.user)
        storage.new(cls.place)
        storage.new(cls.rev)

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.rev

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_Review(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/review.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_Review(self):
        """checking for docstrings"""
        self.assertIsNotNone(Review.__doc__)

    def test_attributes_review(self):
        """chekcing if review have attributes"""
        self.assertTrue('id' in self.rev.__dict__)
        self.assertTrue('created_at' in self.rev.__dict__)
        self.assertTrue('updated_at' in self.rev.__dict__)
        self.assertTrue('place_id' in self.rev.__dict__)
        self.assertTrue('text' in self.rev.__dict__)
        self.assertTrue('user_id' in self.rev.__dict__)

    def test_is_subclass_Review(self):
        """test if review is subclass of BaseModel"""
        self.assertTrue(issubclass(self.rev.__class__, BaseModel), True)

    def test_attribute_types_Review(self):
        """test attribute type for Review"""
        self.assertEqual(type(self.rev.text), str)
        self.assertEqual(type(self.rev.place_id), str)
        self.assertEqual(type(self.rev.user_id), str)

    def test_save_Review(self):
        """test if the save works"""
        self.rev.save()
        self.assertNotEqual(self.rev.created_at, self.rev.updated_at)

    def test_to_dict_Review(self):
        """test if dictionary works"""
        self.assertEqual('to_dict' in dir(self.rev), True)


if __name__ == "__main__":
    unittest.main()
