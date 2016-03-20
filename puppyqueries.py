from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from puppy_db_setup import Base, Shelter, Puppy

import datetime


def getPuppyDBSession():
    """Return an interactive session with the puppy adoption database
    """
    engine = create_engine('sqlite:///puppyadoption.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def getPuppiesByName():
    """Return all puppies in ascending alphabetical order
    """
    session = getPuppyDBSession()
    puppiesByName = session.query(Puppy).order_by(name).all()
    session.close()
    return puppiesByName

def getYoungestPuppies():
    """Return all puppies less than 6 months old in ascending order by age
    """
    session = getPuppyDBSession()
    today = datetime.date.today()
    sixMonthsAgo = today - datetime.timedelta(days = 182)
    youngestPuppies = session.query(Puppy).filter(Puppy.dateOfBirth<=sixMonthsAgo).order_by(dateOfBirth).()
    session.close()
    return youngestPuppies

def getPuppiesByWeight():
    """Retrun all puppies in ascending order by weight
    """
    session = getPuppyDBSession()
    puppiesByWeight = session.query(Puppy).order_by(weight).all()
    session.close()
    return puppiesByWeight

def getPuppiesByShelter():
    """Return all puppies grouped by shelter
    """
    session = getPuppyDBSession()
    puppiesBySheler = session.query(Puppy).group_by(shelter_id)
    session.close()
    return
