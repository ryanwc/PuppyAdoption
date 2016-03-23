from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from puppy_db_setup import Base, Shelter, Puppy
from puppyqueries import getPupDBSession, getSheltFullness, getNumPupsByShelt

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
    session = getPupDBSession()

    # prep steps; find best shelter based on fullness
    numPuppiesByShelter = getNumPupsByShelt()
    shelterIDs = [shelter['shelter_id'] for shelter in numPuppiesByShelter]
    shelterFullness = getSheltFullness()

    leastFilledShelter = []

    for shelter in shelterFullness:
        if shelter['percentFull'] < 1:
            if (len(leastFilledShelter) == 0 or
                shelter['percentFull'] < leastFilledShelter['percentFull']):
                leastFilledShelter = shelter

    # fail if all shelters are at capacity
    if len(leastFilledShelter) < 1:
        print "No space in any shelter! Puppy not added."
        return False

    # test/format name
    if 'name' not in PuppyInfo:
        while True:
            print "Puppy name not provided"
            name = raw_input("What is the puppy's name? ")
            if (len(name)>0):
                break
        PuppyInfo['name'] = name

    while True:
        if (not isinstance(PuppyInfo['name'],str) or
            len(PuppyInfo['name']) > 250 or
            len(PuppyInfo['name']) < 1):
            print "Puppy name not in right format"
            PuppyInfo['name'] = raw_input("What is the puppy's name? ")
        else:
            break

    # test/format gender
    if 'gender' not in PuppyInfo:
        while True:
            print "Puppy gender not provided"
            gender = raw_input("What is the puppy's gender? ")
            if (len(gender)>0):
                break
        PuppyInfo['gender'] = gender
        
    while True:
        if (not isinstance(PuppyInfo['gender'],str) or
            len(PuppyInfo['gender']) > 6 or
            len(PuppyInfo['gender']) < 1):
            print "Puppy gender not provided or not in right format"
            PuppyInfo['gender'] = raw_input("What is the puppy's gender? ")
        else:
            break

    # test/format date of birth
    while True:
        if 'dateOfBirth' not in PuppyInfo:
            PuppyInfo['dateOfBirth'] = None
            break
        elif not isinstance(PuppyInfo['dateOfBirth'],datetime):
            print "Puppy date of birth not in right format"
            dateOfBirthStr = raw_input("What is the puppy's DOB (DD MM YY)? ")
            dateOfBirthStruct = time.strptime(dateOfBirthStr, "%d %m %y")
            PuppyInfo['dateOfBirth'] = datetime.\
                                       fromtimestamp(mktime(dateofBirthStruct))
        else:
            break

    # test/format picture
    while True:
        if 'picture' not in PuppyInfo:
            PuppyInfo['picture'] = None
            break
        elif not isinstance(PuppyInfo['picture'], str):
            print "Picture is not in the right format"
            PuppyInfo['picture'] = raw_input("Provide URL to puppy's picture: ")
        else:
            break

    # test/format shelter id (including balancing)
    if 'shelter_id' not in PuppyInfo:
        while True:
            print "Shelter ID not provided"
            shelter_str = raw_input("What is the ID of the shelter should the "\
                                    "puppy should live at? ")
            if (len(shelter_str)>0):
                break
        shelter_id = int(shelter_str)
        PuppyInfo['shelter_id'] = shelter_id

    while True:
        if ( (not isinstance(PuppyInfo['shelter_id'],int)) or
             (len(str(PuppyInfo['shelter_id'])) < 1) ):
            PuppyInfo['shelter_id'] = int(raw_input("Shelter ID is in "\
                                                    "invalid format, please "\
                                                    "re-enter: "))
        elif not PuppyInfo['shelter_id'] in shelterIDs:
            PuppyInfo['shelter_id'] = int(raw_input("Given shelter ID does "\
                                                    "not exist, please "\
                                                    "re-enter: "))
        elif PuppyInfo['shelter_id'] != leastFilledShelter['shelter_id']:
            print "Using shelter ", leastFilledShelter['shelter_id'], \
                  " instead of shelter ", PuppyInfo['shelter_id'], \
                  " because shelter ", leastFilledShelter['shelter_id'], \
                  " has the most remaining capacity"
            PuppyInfo['shelter_id'] = leastFilledShelter['shelter_id']
            break
        else:
            break
            
    # test/format weight
    while True:
        if 'weight' not in PuppyInfo:
            PuppyInfo['weight'] = None
            break
        elif isinstance(PuppyInfo['weight'],str):
            PuppyInfo['weight'] = int(PuppyInfo['weight'])
        elif (not isinstance(PuppyInfo['weight'],int) or
                 len(str(PuppyInfo['weight'])) > 10 or
                 len(str(PuppyInfo['weight'])) < 1):
            print "Weight is not in the right format"
            weightStr = raw_input("What is the puppy's weight? ")
            PuppyInfo['weight'] = int(weightStr)
        else:
            break

    # insert the new puppy
    new_puppy = Puppy(name = PuppyInfo['name'],\
                      gender = PuppyInfo['gender'],\
                      dateOfBirth = PuppyInfo['dateOfBirth'],\
                      picture = PuppyInfo['picture'],\
                      shelter_id = PuppyInfo['shelter_id'],\
                      weight = PuppyInfo['weight'])
    session.add(new_puppy)
    session.commit()
    
    session.close()
        
    return True
