#!/usr/bin/python3
"""Represents unittests for models/state.py."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        t_sta = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(t_sta))
        self.assertNotIn("name", t_sta.__dict__)

    def test_two_states_unique_ids(self):
        t_sta1 = State()
        t_sta2 = State()
        self.assertNotEqual(t_sta1.id, t_sta2.id)

    def test_two_states_different_created_at(self):
        t_sta1 = State()
        sleep(0.05)
        t_sta2 = State()
        self.assertLess(t_sta1.created_at, t_sta2.created_at)

    def test_two_states_different_updated_at(self):
        t_sta1 = State()
        sleep(0.05)
        t_sta2 = State()
        self.assertLess(t_sta1.updated_at, t_sta2.updated_at)

    def test_str_representation(self):
        tim_d = datetime.today()
        dt_repr = repr(tim_d)
        t_sta = State()
        t_sta.id = "123456"
        t_sta.created_at = t_sta.updated_at = tim_d
        ststr = t_sta.__str__()
        self.assertIn("[State] (123456)", ststr)
        self.assertIn("'id': '123456'", ststr)
        self.assertIn("'created_at': " + dt_repr, ststr)
        self.assertIn("'updated_at': " + dt_repr, ststr)

    def test_args_unused(self):
        t_sta = State(None)
        self.assertNotIn(None, t_sta.__dict__.values())

    def test_instantiation_with_kwargs(self):
        tim_d = datetime.today()
        dt_iso = tim_d.isoformat()
        t_sta = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(t_sta.id, "345")
        self.assertEqual(t_sta.created_at, tim_d)
        self.assertEqual(t_sta.updated_at, tim_d)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittests for testing save method of the State class."""

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
        t_sta = State()
        sleep(0.05)
        first_updated_at = t_sta.updated_at
        t_sta.save()
        self.assertLess(first_updated_at, t_sta.updated_at)

    def test_two_saves(self):
        t_sta = State()
        sleep(0.05)
        first_updated_at = t_sta.updated_at
        t_sta.save()
        second_updated_at = t_sta.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        t_sta.save()
        self.assertLess(second_updated_at, t_sta.updated_at)

    def test_save_with_arg(self):
        t_sta = State()
        with self.assertRaises(TypeError):
            t_sta.save(None)

    def test_save_updates_file(self):
        t_sta = State()
        t_sta.save()
        stid = "State." + t_sta.id
        with open("file.json", "r") as f:
            self.assertIn(stid, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        t_sta = State()
        self.assertIn("id", t_sta.to_dict())
        self.assertIn("created_at", t_sta.to_dict())
        self.assertIn("updated_at", t_sta.to_dict())
        self.assertIn("__class__", t_sta.to_dict())

    def test_to_dict_contains_added_attributes(self):
        t_sta = State()
        t_sta.middle_name = "Holberton"
        t_sta.my_number = 98
        self.assertEqual("Holberton", t_sta.middle_name)
        self.assertIn("my_number", t_sta.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        t_sta = State()
        st_dict = t_sta.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def test_to_dict_output(self):
        tim_d = datetime.today()
        t_sta = State()
        t_sta.id = "123456"
        t_sta.created_at = t_sta.updated_at = tim_d
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': tim_d.isoformat(),
            'updated_at': tim_d.isoformat(),
        }
        self.assertDictEqual(t_sta.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        t_sta = State()
        self.assertNotEqual(t_sta.to_dict(), t_sta.__dict__)

    def test_to_dict_with_arg(self):
        t_sta = State()
        with self.assertRaises(TypeError):
            t_sta.to_dict(None)


if __name__ == "__main__":
    unittest.main()
