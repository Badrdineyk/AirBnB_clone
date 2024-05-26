#!/usr/bin/python3
"""Reprents unittests for models/amenity.py."""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        ameni = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", ameni.__dict__)

    def test_two_amenities_unique_ids(self):
        ameni1 = Amenity()
        ameni2 = Amenity()
        self.assertNotEqual(ameni1.id, ameni2.id)

    def test_two_amenities_different_created_at(self):
        ameni1 = Amenity()
        sleep(0.05)
        ameni2 = Amenity()
        self.assertLess(ameni1.created_at, ameni2.created_at)

    def test_two_amenities_different_updated_at(self):
        ameni1 = Amenity()
        sleep(0.05)
        ameni2 = Amenity()
        self.assertLess(ameni1.updated_at, ameni2.updated_at)

    def test_str_representation(self):
        tim_d = datetime.today()
        dt_repr = repr(tim_d)
        ameni = Amenity()
        ameni.id = "123456"
        ameni.created_at = ameni.updated_at = tim_d
        amstr = ameni.__str__()
        self.assertIn("[Amenity] (123456)", amstr)
        self.assertIn("'id': '123456'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def test_args_unused(self):
        ameni = Amenity(None)
        self.assertNotIn(None, ameni.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """instantiation with kwargs test method"""
        tim_d = datetime.today()
        dt_iso = tim_d.isoformat()
        ameni = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(ameni.id, "345")
        self.assertEqual(ameni.created_at, tim_d)
        self.assertEqual(ameni.updated_at, tim_d)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

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
        ameni = Amenity()
        sleep(0.05)
        first_updated_at = ameni.updated_at
        ameni.save()
        self.assertLess(first_updated_at, ameni.updated_at)

    def test_two_saves(self):
        ameni = Amenity()
        sleep(0.05)
        first_updated_at = ameni.updated_at
        ameni.save()
        second_updated_at = ameni.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        ameni.save()
        self.assertLess(second_updated_at, ameni.updated_at)

    def test_save_with_arg(self):
        ameni = Amenity()
        with self.assertRaises(TypeError):
            ameni.save(None)

    def test_save_updates_file(self):
        ameni = Amenity()
        ameni.save()
        amid = "Amenity." + ameni.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        ameni = Amenity()
        self.assertIn("id", ameni.to_dict())
        self.assertIn("created_at", ameni.to_dict())
        self.assertIn("updated_at", ameni.to_dict())
        self.assertIn("__class__", ameni.to_dict())

    def test_to_dict_contains_added_attributes(self):
        ameni = Amenity()
        ameni.middle_name = "ALX"
        ameni.my_number = 24
        self.assertEqual("ALX", ameni.middle_name)
        self.assertIn("my_number", ameni.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        ameni = Amenity()
        am_dict = ameni.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_to_dict_output(self):
        tim_d = datetime.today()
        ameni = Amenity()
        ameni.id = "123456"
        ameni.created_at = ameni.updated_at = tim_d
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': tim_d.isoformat(),
            'updated_at': tim_d.isoformat(),
        }
        self.assertDictEqual(ameni.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        ameni = Amenity()
        self.assertNotEqual(ameni.to_dict(), ameni.__dict__)

    def test_to_dict_with_arg(self):
        ameni = Amenity()
        with self.assertRaises(TypeError):
            ameni.to_dict(None)


if __name__ == "__main__":
    unittest.main()
