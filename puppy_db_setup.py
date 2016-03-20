import sys
import psycopg2

# import functionality from sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
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
	city = Column(String(30), nullable=False)
	state = Column(String(30), nullable=False)
	zipCode = Column(String(10), nullable=False)
	website = Column(String)

class Puppy(Base):
	__tablename__ = 'puppy'

	id = Column(Integer, primary_key=True)
	name = Column(String(30), nullable=False)
	dateOfBirth = Column(Date)
	gender = Column(String(1), nullable = False)
	weight = Column(Numeric(10))
	picture = Column(String)
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)


# connect to database engine
engine = create_engine('sqlite:///puppyadoption.db')

# creates the database as new tables with the given engine/name
Base.metadata.create_all(engine)
