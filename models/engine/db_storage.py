#!/usr/bin/python3
"""This defines the DBStorage class"""
import sqlalchemy
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from os import environ


class DBStorage():
    """Defines the DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Defines setup for DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                                      environ['HBNB_MYSQL_USER'],
                                      environ['HBNB_MYSQL_PWD'],
                                      environ['HBNB_MYSQL_HOST'],
                                      environ['HBNB_MYSQL_DB'],
                                      pool_pre_ping=True))
        if 'HBNB_ENV' in environ and environ['HBNB_ENV'] == 'test':
            meta = MetaData()
            meta.reflect(bind=self.__engine)
            for table in reversed(meta.sorted_tables):
                self.__engine.execute(table.delete())

    def all(self, cls=None):
        """Performs a query on the current database session
           cls is an object, not a string.
        """
        object_types = {'User': User, 'State': State, 'City': City,
                        'Amenity': Amenity, 'Place': Place, 'Review': Review}
        object_dict = {}

        if cls is None:
            for my_type in object_types.keys():
                for obj in self.__session.query(object_types[my_type]).all():
                    key = obj.__class__.__name__ + '.' + obj.id
                    object_dict[key] = obj
        else:
            if isinstance(cls, str):
                cls = object_types[cls]
            for obj in self.__session.query(cls).all():
                key = obj.__class__.__name__ + '.' + obj.id
                object_dict[key] = obj

        return object_dict

    def close(self):
        self.__session.close()

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes fo the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from current database session if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(bind=self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False, autoflush=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
