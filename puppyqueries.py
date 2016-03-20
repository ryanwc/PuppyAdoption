from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from puppy_db_setup import Base, Shelter, Puppy


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
    
    return

def getYoungestPuppies():
    """Return all puppies less than 6 months old in ascending order by age
    """
    session = getPuppyDBSession()
    
    return

def getPuppiesByWeight():
    """Retrun all puppies in ascending order by weight
    """
    session = getPuppyDBSession()
    
    return

def getPuppiesByShelter():
    """Return all puppies grouped by shelter
    """
    session = getPuppyDBSession()
    
    return
