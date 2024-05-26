#!/usr/bin/python3
"""Represents unittests for models/engine/file_storage.py."""

import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        base_m = BaseModel()
        usr = User()
        stat = State()
        pla = Place()
        cit = City()
        ameni = Amenity()
        revi = Review()
        models.storage.new(base_m)
        models.storage.new(usr)
        models.storage.new(stat)
        models.storage.new(pla)
        models.storage.new(cit)
        models.storage.new(ameni)
        models.storage.new(revi)
        self.assertIn("BaseModel." + base_m.id, models.storage.all().keys())
        self.assertIn(base_m, models.storage.all().values())
        self.assertIn("User." + usr.id, models.storage.all().keys())
        self.assertIn(usr, models.storage.all().values())
        self.assertIn("State." + stat.id, models.storage.all().keys())
        self.assertIn(stat, models.storage.all().values())
        self.assertIn("Place." + pla.id, models.storage.all().keys())
        self.assertIn(pla, models.storage.all().values())
        self.assertIn("City." + cit.id, models.storage.all().keys())
        self.assertIn(cit, models.storage.all().values())
        self.assertIn("Amenity." + ameni.id, models.storage.all().keys())
        self.assertIn(ameni, models.storage.all().values())
        self.assertIn("Review." + revi.id, models.storage.all().keys())
        self.assertIn(revi, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_with_None(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save(self):
        base_m = BaseModel()
        usr = User()
        stat = State()
        pla = Place()
        cit = City()
        ameni = Amenity()
        revi = Review()
        models.storage.new(base_m)
        models.storage.new(usr)
        models.storage.new(stat)
        models.storage.new(pla)
        models.storage.new(cit)
        models.storage.new(ameni)
        models.storage.new(revi)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + base_m.id, save_text)
            self.assertIn("User." + usr.id, save_text)
            self.assertIn("State." + stat.id, save_text)
            self.assertIn("Place." + pla.id, save_text)
            self.assertIn("City." + cit.id, save_text)
            self.assertIn("Amenity." + ameni.id, save_text)
            self.assertIn("Review." + revi.id, save_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        base_m = BaseModel()
        usr = User()
        stat = State()
        pla = Place()
        cit = City()
        ameni = Amenity()
        revi = Review()
        models.storage.new(base_m)
        models.storage.new(usr)
        models.storage.new(stat)
        models.storage.new(pla)
        models.storage.new(cit)
        models.storage.new(ameni)
        models.storage.new(revi)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + base_m.id, objs)
        self.assertIn("User." + usr.id, objs)
        self.assertIn("State." + stat.id, objs)
        self.assertIn("Place." + pla.id, objs)
        self.assertIn("City." + cit.id, objs)
        self.assertIn("Amenity." + ameni.id, objs)
        self.assertIn("Review." + revi.id, objs)

    def test_reload_no_file(self):
        self.assertRaises(FileNotFoundError, models.storage.reload())

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
