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
    session = getPuppyDBSession()

    shelterIDs = session.query(distinct(Puppy.shelter_id))
    numPuppiesByShelter = []

    for shelterID in shelterIDs:
        tupleToAdd = {"shelter_id": shelterID[0],
                      "numOfPups": session.query(Puppy.id).\
                      filter(Puppy.shelter_id==shelterID[0]).count()}
        numPuppiesByShelter.append(tupleToAdd)

    session.close()
    return numPuppiesByShelter

def getShelterFullness():
    """Return the id of the shelter with the most free space for puppies
    """
    session = getPuppyDBSession()

    numPuppiesByShelter = getNumPuppiesByShelter()
    shelterFullness = []
    
    for shelter in numPuppiesByShelter:
        shelterCapacity = session.query(Shelter.capacity).\
                          filter(Shelter.id==shelter['shelter_id']).first()[0]
        tupleToAdd = {'shelter_id': shelter['shelter_id'],
                      'fullness': (shelter['numOfPups'] / float(shelterCapacity))}
        shelterFullness.append(tupleToAdd)
    
    session.close()
    return shelterFullness
