from sqlalchemy import create_engine, select, func, distinct
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
    """Return a list all puppies in ascending alphabetical order
    """
    session = getPuppyDBSession()
    
    puppiesByName = session.query(Puppy).order_by(Puppy.name)
    
    session.close()
    return puppiesByName

def getYoungestPuppies():
    """Return a list of all puppies less than 6 months old in ascending
        order by age
    """
    session = getPuppyDBSession()
    
    today = datetime.date.today()
    sixMonthsAgo = today - datetime.timedelta(days = 182)
    youngestPuppies = session.query(Puppy).\
                      filter(Puppy.dateOfBirth>=sixMonthsAgo).\
                      order_by(Puppy.dateOfBirth)

    session.close()
    return youngestPuppies

def getPuppiesByWeight():
    """Retrun a list of all puppies in ascending order by weight
    """
    session = getPuppyDBSession()

    puppiesByWeight = session.query(Puppy).order_by(Puppy.weight)

    session.close()
    return puppiesByWeight

def getPuppiesByShelter():
    """Return a list of all puppies ordered by shelter
    """
    session = getPuppyDBSession()

    puppiesByShelter = session.query(Puppy).order_by(Puppy.shelter_id)

    session.close()
    return puppiesByShelter

def getNumPuppiesByShelter():
    """Return a list with number of puppies in each shelter
    """
    session getPuppyDBSession()

    numPuppiesByShelter = session.query(func.count(Puppy.name)).\
                          group_by(Puppy.shelter_id)

    session.close()
    return numPuppiesByShelter

