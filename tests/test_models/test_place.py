#!/usr/bin/python3
"""Represents unittests for models/place.py."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        plac = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(plac))
        self.assertNotIn("city_id", plac.__dict__)

    def test_user_id_is_public_class_attribute(self):
        plac = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(plac))
        self.assertNotIn("user_id", plac.__dict__)

    def test_name_is_public_class_attribute(self):
        plac = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(plac))
        self.assertNotIn("name", plac.__dict__)

    def test_description_is_public_class_attribute(self):
        plac = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(plac))
        self.assertNotIn("desctiption", plac.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        plac = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(plac))
        self.assertNotIn("number_rooms", plac.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        plac = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(plac))
        self.assertNotIn("number_bathrooms", plac.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        plac = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(plac))
        self.assertNotIn("max_guest", plac.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        plac = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(plac))
        self.assertNotIn("price_by_night", plac.__dict__)

    def test_latitude_is_public_class_attribute(self):
        plac = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(plac))
        self.assertNotIn("latitude", plac.__dict__)

    def test_longitude_is_public_class_attribute(self):
        plac = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(plac))
        self.assertNotIn("longitude", plac.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        plac = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(plac))
        self.assertNotIn("amenity_ids", plac.__dict__)

    def test_two_places_unique_ids(self):
        plac1 = Place()
        plac2 = Place()
        self.assertNotEqual(plac1.id, plac2.id)

    def test_two_places_different_created_at(self):
        plac1 = Place()
        sleep(0.05)
        plac2 = Place()
        self.assertLess(plac1.created_at, plac2.created_at)

    def test_two_places_different_updated_at(self):
        plac1 = Place()
        sleep(0.05)
        plac2 = Place()
        self.assertLess(plac1.updated_at, plac2.updated_at)

    def test_str_representation(self):
        tim_d = datetime.today()
        dt_repr = repr(tim_d)
        plac = Place()
        plac.id = "123456"
        plac.created_at = plac.updated_at = tim_d
        plstr = plac.__str__()
        self.assertIn("[Place] (123456)", plstr)
        self.assertIn("'id': '123456'", plstr)
        self.assertIn("'created_at': " + dt_repr, plstr)
        self.assertIn("'updated_at': " + dt_repr, plstr)

    def test_args_unused(self):
        plac = Place(None)
        self.assertNotIn(None, plac.__dict__.values())

    def test_instantiation_with_kwargs(self):
        tim_d = datetime.today()
        dt_iso = tim_d.isoformat()
        plac = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(plac.id, "345")
        self.assertEqual(plac.created_at, tim_d)
        self.assertEqual(plac.updated_at, tim_d)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

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
        plac = Place()
        sleep(0.05)
        first_updated_at = plac.updated_at
        plac.save()
        self.assertLess(first_updated_at, plac.updated_at)

    def test_two_saves(self):
        plac = Place()
        sleep(0.05)
        first_updated_at = plac.updated_at
        plac.save()
        second_updated_at = plac.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        plac.save()
        self.assertLess(second_updated_at, plac.updated_at)

    def test_save_with_arg(self):
        plac = Place()
        with self.assertRaises(TypeError):
            plac.save(None)

    def test_save_updates_file(self):
        plac = Place()
        plac.save()
        plid = "Place." + plac.id
        with open("file.json", "r") as f:
            self.assertIn(plid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        plac = Place()
        self.assertIn("id", plac.to_dict())
        self.assertIn("created_at", plac.to_dict())
        self.assertIn("updated_at", plac.to_dict())
        self.assertIn("__class__", plac.to_dict())

    def test_to_dict_contains_added_attributes(self):
        plac = Place()
        plac.middle_name = "ALX"
        plac.my_number = 24
        self.assertEqual("ALX", plac.middle_name)
        self.assertIn("my_number", plac.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        plac = Place()
        pl_dict = plac.to_dict()
        self.assertEqual(str, type(pl_dict["id"]))
        self.assertEqual(str, type(pl_dict["created_at"]))
        self.assertEqual(str, type(pl_dict["updated_at"]))

    def test_to_dict_output(self):
        tim_d = datetime.today()
        plac = Place()
        plac.id = "123456"
        plac.created_at = plac.updated_at = tim_d
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': tim_d.isoformat(),
            'updated_at': tim_d.isoformat(),
        }
        self.assertDictEqual(plac.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        plac = Place()
        self.assertNotEqual(plac.to_dict(), plac.__dict__)

    def test_to_dict_with_arg(self):
        plac = Place()
        with self.assertRaises(TypeError):
            plac.to_dict(None)


if __name__ == "__main__":
    unittest.main()
