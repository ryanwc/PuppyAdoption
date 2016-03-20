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
    puppiesByName = session.query(Puppy).order_by(name)
    session.close()
    return puppiesByName

def getYoungestPuppies():
    """Return all puppies less than 6 months old in ascending order by age
    """
    session = getPuppyDBSession()
    today = datetime.date.today()
    youngestPuppies = session.query(Puppy).filter(Puppy.dateOfBirth-today<=182).order_by(dateOfBirth)
    session.close()
    return youngestPuppies

def getPuppiesByWeight():
    """Retrun all puppies in ascending order by weight
    """
    session = getPuppyDBSession()
    puppiesByWeight = session.query(Puppy).order_by(weight)
    session.close()
    return puppiesByWeight

def getPuppiesByShelter():
    """Return all puppies grouped by shelter
    """
    session = getPuppyDBSession()
    
    session.close()
    return
