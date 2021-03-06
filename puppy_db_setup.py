import sys

# import functionality from sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, Boolean
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


# create an object that holds the database's data
Base = declarative_base()


# define tables for the database in Python classes
class Shelter(Base):
        __tablename__ = 'shelter'

        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)
        address = Column(String(250), nullable=False)
        city = Column(String(80), nullable=False)
        state = Column(String(30), nullable=False)
        zipCode = Column(String(10), nullable=False)
        capacity = Column(Integer, nullable=False)
        website = Column(String)


class Puppy(Base):
        __tablename__ = 'puppy'

        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)
        dateOfBirth = Column(Date)
        gender = Column(String(6), nullable = False)
        weight = Column(Integer)
        picture = Column(String)
        shelter_id = Column(Integer,ForeignKey('shelter.id'),nullable=False)
        adopted = Column(Boolean, nullable = False)


class Adopter(Base):
        __tablename__ = 'adopter'
        __table_args__ = (
                PrimaryKeyConstraint('person_id', 'puppy_id'),
        )

        person_id = Column(Integer, ForeignKey('person.id'), nullable=False)
        puppy_id = Column(Integer, ForeignKey('puppy.id'), nullable=False)


class Person(Base):
        __tablename__ = 'person'

        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)
        household_id = Column(Integer,ForeignKey('household.id'),nullable=False)
        #headOfHousehold = Column(Boolean, nullable=False)


class Household(Base):
        __tablename__ = 'household'

        id = Column(Integer, primary_key=True)
        #headOfHousehould = Column(Integer, ForeignKey('person.id'))
        address = Column(String(250), nullable=False)
        city = Column(String(80), nullable=False)
        state = Column(String(30), nullable=False)
        zipCode = Column(String(10), nullable=False)


# connect to database engine
engine = create_engine('sqlite:///puppyadoption.db')

# creates the database as new tables with the given engine/name
Base.metadata.create_all(engine)
