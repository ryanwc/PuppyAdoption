from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from puppy_db_setup import Base, Shelter, Puppy
import puppyqueries

import time, datetime

def addPuppyToShelter(PuppyInfo):
    """Insert a puppy into the adoption database

    Args:
      PuppyInfo: List of puppy attributes
          Required attributes (cannot be None): name, gender, shelter_id
          Optional attributes (can be None): dateOfBirth, picture, weight
    Return:
      True if puppy was successfully added to the database
      False if puppy was not added to the database
    """
    session = getPuppyDBSession()

    # prep steps; find best shelter based on fullness
    numPuppiesByShelter = puppyqueries.getNumPuppiesByShelter()
    shelterIDs = [shelter.shelter_id for shelter in numPuppiesByShelter]
    shelterFullness = puppyqueries.getShelterFullness()

    leastFilledShelter = []

    for shelter in shelterFullness:
        if shelter[1] < 1:
            if (len(leastFilledShelter) == 0 or
                shelter[1] < leastFilledShelter[1]):
                leastFilledShelter = [{"shelter_id": shelter[0], \
                                       "percentFull": shelter[1]}]

    # fail if all shelters are at capacity
    if len(leastFilledShelter) < 1:
        print "No space in any shelter! Puppy not added."
        return False

    # test/format name
    if PuppyInfo.name is None:
        while True:
            print "Puppy name not provided"
            name = raw_input("What is the puppy's name? ")
            if (len(name)>0):
                break
        PuppyInfo.append(name)

    while True:
        if (not isinstance(PuppyInfo.name,str) or
            len(PuppyInfo.name) > 250 or
            len(PuppyInfo.name) < 1):
            print "Puppy name not in right format"
            PuppyInfo.name = raw_input("What is the puppy's name? ")
        else:
            break

    # test/format gender
    if PuppyInfo.gender is None:
        while True:
            print "Puppy gender not provided"
            gender = raw_input("What is the puppy's gender? ")
            if (len(gender)>0):
                break
        PuppyInfo.append(gender)
        
    while True:
        if (not isinstance(PuppyInfo.gender,str) or
            len(PuppyInfo.gender) > 6 or
            len(PuppyInfo.gender) < 1):
            print "Puppy gender not provided or not in right format"
            PuppyInfo.gender = raw_input("What is the puppy's gender? ")
        else:
            break

    # test/format date of birth
    while True:
        if PuppyInfo.dateOfBirth is None:
            break
        else if not isinstance(PuppyInfo.dateOfBirth,datetime):
            print "Puppy date of birth not in right format"
            dateOfBirthStr = raw_input("What is the puppy's DOB (DD MM YY)? ")
            dateOfBirthStruct = time.strptime(dateOfBirthStr, "%d %m %y")
            PuppyInfo.dateOfBirth = datetime.\
                                    fromtimestamp(mktime(dateofBirthStruct))
        else:
            break

    # test/format picture
    while True:
        if PuppyInfo.picture is None:

            break
        else if not isinstance(picture, str):
            print "Picture is not in the right format"
            PuppyInfo.picture = raw_input("Provide URL to puppy's picture: ")
        else:
            break

    # test/format shelter id (including balancing)
    if PuppyInfo.shelter_id is None:
        while True:
            print "Shelter ID not provided"
            shelter_str = raw_input("What is the ID of the shelter should the "\
                                    "puppy should live at? ")
            if (len(shelter_str)>0):
                break
        shelter_id = int(shelter_str)
        PuppyInfo.append(shelter_id)

    while True:
        if not isinstance(PuppyInfo.shelter_id,int):
            print "Shelter ID is invalid"
        else if not PuppyInfo.shelter_id in shelterIDs:
            PuppyInfo.shelter_id = int(raw_input("Given shelter ID does not "\
                                                 "exist, please re-enter: "))
        else if PuppyInfo.shelter_id != leastFilledShelter[0]:
            print "Using shelter " + leastFilledShelter[0] + " instead of " \
                  "shelter " + PuppyInfo.shelter_id + " because shelter "\
                  + leastFilledShelter[0] + " has the most capacity"
            PuppyInfo.shelter_id = leastFilledShelter[0]
            break
        else:
            break
            
    # test/format weight
    while True:
        if PuppyInfo.weight is None:
            break
        else if isinstance(PuppyInfo.weight,str):
            PuppyInfo.weight = int(PuppyInfo.weight)
        else if (not isinstance(PuppyInfo.weight,int) or
                 len(str(PuppyInfo.weight)) > 10 or
                 len(str(PuppyInfo.weight)) < 1):
            print "Weight is not in the right format"
            weightStr = raw_input("What is the puppy's weight? ")
            PuppyInfo.weight = int(weightStr)
        else:
            break

    # insert the new puppy
    new_puppy = Puppy(PuppyInfo.name,PuppyInfo.gender,\
                      PuppyInfo.dateOfBirth,PuppyInfo.picture,\
                      leastFilledShelter[0],PuppyInfo.weight)
    session.add(new_puppy)
    session.commit()
    
    session.close()
        
    return True
