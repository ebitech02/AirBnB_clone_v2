#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
import models
from models import storage_t
from models.city import City

class State(BaseModel):
    """ State class """
       __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="all, delete, delete-orphan")

    @property
    def cities(self):
        '''
        Return list of city with state_id equals to stste.id
        '''
        from models import storage

        city_list = []
        cities = storage.all(City)

        for city in cities.values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
