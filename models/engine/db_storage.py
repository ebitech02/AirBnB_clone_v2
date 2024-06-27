#!/usr/bin/python3
"""
module: db_storage
"""
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """New database engine"""
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the value and links to database
        """
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine('mysql + mysqldb://{}:{}@{}/{}'.format(
            user, password, host, db), pull_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """query on the current db session & return a dict"""

        my_classes = (Amenity, City, Place, Review, State, User)
        objects = dict()

        if cls is None:
            for item in my_classes:
                query = self.__session.query(item)
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.name__, obj.id)
                    objects[obj_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[obj_key] = obj
        print(objects)
        return objects

    def new(self, obj):
        """Adds an object to the current database"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the current database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()
