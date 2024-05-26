#!/usr/bin/python3
"""Represents unittests for models/city.py."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        cit = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cit))
        self.assertNotIn("state_id", cit.__dict__)

    def test_name_is_public_class_attribute(self):
        cit = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(cit))
        self.assertNotIn("name", cit.__dict__)

    def test_two_cities_unique_ids(self):
        cit1 = City()
        cit2 = City()
        self.assertNotEqual(cit1.id, cit2.id)

    def test_two_cities_different_created_at(self):
        cit1 = City()
        sleep(0.05)
        cit2 = City()
        self.assertLess(cit1.created_at, cit2.created_at)

    def test_two_cities_different_updated_at(self):
        cit1 = City()
        sleep(0.05)
        cit2 = City()
        self.assertLess(cit1.updated_at, cit2.updated_at)

    def test_str_representation(self):
        tim_d = datetime.today()
        dt_repr = repr(tim_d)
        cit = City()
        cit.id = "123456"
        cit.created_at = cit.updated_at = tim_d
        cystr = cit.__str__()
        self.assertIn("[City] (123456)", cystr)
        self.assertIn("'id': '123456'", cystr)
        self.assertIn("'created_at': " + dt_repr, cystr)
        self.assertIn("'updated_at': " + dt_repr, cystr)

    def test_args_unused(self):
        cit = City(None)
        self.assertNotIn(None, cit.__dict__.values())

    def test_instantiation_with_kwargs(self):
        tim_d = datetime.today()
        dt_iso = tim_d.isoformat()
        cit = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cit.id, "345")
        self.assertEqual(cit.created_at, tim_d)
        self.assertEqual(cit.updated_at, tim_d)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        cit = City()
        sleep(0.05)
        first_updated_at = cit.updated_at
        cit.save()
        self.assertLess(first_updated_at, cit.updated_at)

    def test_two_saves(self):
        cit = City()
        sleep(0.05)
        first_updated_at = cit.updated_at
        cit.save()
        second_updated_at = cit.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cit.save()
        self.assertLess(second_updated_at, cit.updated_at)

    def test_save_with_arg(self):
        cit = City()
        with self.assertRaises(TypeError):
            cit.save(None)

    def test_save_updates_file(self):
        cit = City()
        cit.save()
        cyid = "City." + cit.id
        with open("file.json", "r") as f:
            self.assertIn(cyid, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        cit = City()
        self.assertIn("id", cit.to_dict())
        self.assertIn("created_at", cit.to_dict())
        self.assertIn("updated_at", cit.to_dict())
        self.assertIn("__class__", cit.to_dict())

    def test_to_dict_contains_added_attributes(self):
        cit = City()
        cit.middle_name = "ALX"
        cit.my_number = 24
        self.assertEqual("ALX", cit.middle_name)
        self.assertIn("my_number", cit.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        cit = City()
        cy_dict = cit.to_dict()
        self.assertEqual(str, type(cy_dict["id"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["updated_at"]))

    def test_to_dict_output(self):
        tim_d = datetime.today()
        cit = City()
        cit.id = "123456"
        cit.created_at = cit.updated_at = tim_d
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': tim_d.isoformat(),
            'updated_at': tim_d.isoformat(),
        }
        self.assertDictEqual(cit.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        cit = City()
        self.assertNotEqual(cit.to_dict(), cit.__dict__)

    def test_to_dict_with_arg(self):
        cit = City()
        with self.assertRaises(TypeError):
            cit.to_dict(None)


if __name__ == "__main__":
    unittest.main()
