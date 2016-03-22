from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from puppy_db_setup import Base, Shelter, Puppy
import puppyqueries

import datetime

def addPuppyToShelter(name, gender, dateOfBirth, picture, shelter_id, weight):
    """Insert a puppy into the adoption database

    Args:
      name: the puppy's name
      gender: the puppy's gender
      dateOfBirth: puppy's birthday
      picture: a web address of a picture of the puppy
      shelter_id: the id of the shelter where the function caller wants the
          puppy to live
      weight: the puppy's weight
    """
    session = getPuppyDBSession()
        
    if (name is None or not isinstance(name,str) or len(name) > 250):
        print "Puppy name is not in the right format"
        
    if (gender is None or not isinstance(gender,str) or len(gender) > 6):
        print "Gender of puppy is not in right format"
        
    if (dateOfBirth is None or not isinstance(dateOfBirth,datetime)):
        print "Puppy date of birth is not in right format"
        
    if (picture is None or not isinstance(picture, str)):
        print "Picture is not in the right format"
        
    if (shelter_id is None or not isinstance(shelter_id,Integer)):
        print "Shelter ID is not in the right format"
        
    if (weight is None or
        not (isinstance(weight,str) or isinstance(weight,Integer)) or
        len(str(weight)) > 10):
        print "Weight is not in the right format"
        

    numPuppiesByShelter = puppyqueries.getNumPuppiesByShelter()
    shelterIDs = [shelter.shelter_id for shelter in numPuppiesByShelter]
    leastFilledShelter = puppyqueries.getLeastFilledShelter()

    if shelter_id in shelterIDs:
        print "Given shelter ID does not exist, using this ID instead: "\
              + leastFilledShelter
    else if shelter_id != leastFilledShelter:
        print "Using shelter " + leastFilledShelter + " instead of shelter "\
              + shelter_id + " because shelter " + leastFilledShelter\
              + "has the most capacity"
    
    new_puppy = Puppy(name,gender,dateOfBirth,picture,leastFilledShelter,weight)
        
    session.add(new_puppy)
    session.commit()
    
    session.close()
