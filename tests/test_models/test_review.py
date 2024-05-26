#!/usr/bin/python3
"""Represents unittests for models/review.py."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        revi = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(revi))
        self.assertNotIn("place_id", revi.__dict__)

    def test_user_id_is_public_class_attribute(self):
        revi = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(revi))
        self.assertNotIn("user_id", revi.__dict__)

    def test_text_is_public_class_attribute(self):
        revi = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(revi))
        self.assertNotIn("text", revi.__dict__)

    def test_two_reviews_unique_ids(self):
        revi1 = Review()
        revi2 = Review()
        self.assertNotEqual(revi1.id, revi2.id)

    def test_two_reviews_different_created_at(self):
        revi1 = Review()
        sleep(0.05)
        revi2 = Review()
        self.assertLess(revi1.created_at, revi2.created_at)

    def test_two_reviews_different_updated_at(self):
        revi1 = Review()
        sleep(0.05)
        revi2 = Review()
        self.assertLess(revi1.updated_at, revi2.updated_at)

    def test_str_representation(self):
        tim_d = datetime.today()
        dt_repr = repr(tim_d)
        revi = Review()
        revi.id = "123456"
        revi.created_at = revi.updated_at = tim_d
        rvstr = revi.__str__()
        self.assertIn("[Review] (123456)", rvstr)
        self.assertIn("'id': '123456'", rvstr)
        self.assertIn("'created_at': " + dt_repr, rvstr)
        self.assertIn("'updated_at': " + dt_repr, rvstr)

    def test_args_unused(self):
        revi = Review(None)
        self.assertNotIn(None, revi.__dict__.values())

    def test_instantiation_with_kwargs(self):
        tim_d = datetime.today()
        dt_iso = tim_d.isoformat()
        revi = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(revi.id, "345")
        self.assertEqual(revi.created_at, tim_d)
        self.assertEqual(revi.updated_at, tim_d)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

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
        revi = Review()
        sleep(0.05)
        first_updated_at = revi.updated_at
        revi.save()
        self.assertLess(first_updated_at, revi.updated_at)

    def test_two_saves(self):
        revi = Review()
        sleep(0.05)
        first_updated_at = revi.updated_at
        revi.save()
        second_updated_at = revi.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        revi.save()
        self.assertLess(second_updated_at, revi.updated_at)

    def test_save_with_arg(self):
        revi = Review()
        with self.assertRaises(TypeError):
            revi.save(None)

    def test_save_updates_file(self):
        revi = Review()
        revi.save()
        rvid = "Review." + revi.id
        with open("file.json", "r") as f:
            self.assertIn(rvid, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        revi = Review()
        self.assertIn("id", revi.to_dict())
        self.assertIn("created_at", revi.to_dict())
        self.assertIn("updated_at", revi.to_dict())
        self.assertIn("__class__", revi.to_dict())

    def test_to_dict_contains_added_attributes(self):
        revi = Review()
        revi.middle_name = "ALX"
        revi.my_number = 24
        self.assertEqual("ALX", revi.middle_name)
        self.assertIn("my_number", revi.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        revi = Review()
        rv_dict = revi.to_dict()
        self.assertEqual(str, type(rv_dict["id"]))
        self.assertEqual(str, type(rv_dict["created_at"]))
        self.assertEqual(str, type(rv_dict["updated_at"]))

    def test_to_dict_output(self):
        tim_d = datetime.today()
        revi = Review()
        revi.id = "123456"
        revi.created_at = revi.updated_at = tim_d
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': tim_d.isoformat(),
            'updated_at': tim_d.isoformat(),
        }
        self.assertDictEqual(revi.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        revi = Review()
        self.assertNotEqual(revi.to_dict(), revi.__dict__)

    def test_to_dict_with_arg(self):
        revi = Review()
        with self.assertRaises(TypeError):
            revi.to_dict(None)


if __name__ == "__main__":
    unittest.main()
