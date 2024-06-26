#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from datetime import datetime
from sqlaclchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if kwargs:
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())

            for key, value in kwards.item():
                if key == 'created_at' or key =='updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__':
                    setattr(self, key, value)

            if 'created_at' not in kwargs:
                self.created_at = self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        '''Delete current instance from the storage'''
        models.storage.delete(self)
        
    def to_dict(self):
        """Convert instance into dict format and update new dictionary"""
        new_dictionary = self.__dict__.copy()
        # update the created and updated at attributes
        if "created_at" in new_dictionary:
            new_dictionary["created_at"] = new_dictionary["created_at"].strftime(time)
        if "updated_at" in new_dictionary:
            new_dictionary["updated_at"] = new_dictionary["updated_at"].strftime(time)
        new_dictionary["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dictionary:
            del new_dictionary["_sa_instance_state"]
        return new_dictionary
