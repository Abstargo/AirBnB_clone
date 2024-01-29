#!/usr/bin/python3
"""[Module that contains the FileStorage class]"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """[Class Engine to serialize to json and deserialize to instances]"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """[returns the dictionary __objects]"""
        return self.__objects

    def new(self, obj):
        """[sets  in __objects the obj with key <obj class name>.id]"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """[serializes __objects to the JSON file (path: __file_path)]"""
        dict_data = self.__objects
        transformed = {key: dict_data[key].to_dict()
                       for key, _ in dict_data.items()}
        with open(self.__file_path, mode="w") as f:
            json.dump(transformed, f)

    def reload(self):
        """[deserializes the JSON file to __objects if this exists]"""
        try:
            with open(self.__file_path, mode="r") as f:
                readed = json.load(f)
            for _, dict_readed in readed.items():
                class_name = dict_readed.__getitem__('__class__')
                self.new(eval(class_name)(**dict_readed))
        except FileNotFoundError:
            return
