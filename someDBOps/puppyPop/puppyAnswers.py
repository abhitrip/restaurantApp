from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base,Shelter,Puppy
import datetime
from sqlalchemy.sql import func

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def queryPupsByAscending():
    listOfPups = session.query(Puppy).order_by(Puppy.name.asc()).all()
    for pup in listOfPups:
        print pup.name,

def queryPupsLessThan6MonthsOld():
    # Ignoring the leap year constraint
    today = datetime.datetime.now()
    # Assuming 182 days = 6 Months
    dayDiff = 182 #6 Months
    prevDate = today-datetime.timedelta(days=dayDiff)
    print prevDate # To Debug
    convertTime = prevDate.strftime("%Y-%m-%d")
    listOfPups = session.query(Puppy).filter(Puppy.dateOfBirth>=convertTime).all()
    for pup in listOfPups:
        print pup.name,pup.dateOfBirth
    

    for pup in listOfPups:
        print pup.name,pup.dateOfBirth

def queryPupsByAscendingWeight():
    for name,weight in session.query(Puppy.name,Puppy.weight).order_by(Puppy.weight.asc()):
        print name,weight



def queryPupsByShelter():
    pupAndShelterList = session.query(Shelter,func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
    for pns in pupAndShelterList:
        print pns[0].id,pns[0].name,pns[1]  


if __name__ == '__main__':
    # Task 1
    #queryPupsByAscending()
    # Task 2
    queryPupsLessThan6MonthsOld()
    # Task 3
    #queryPupsByAscendingWeight()
    # Task 4
    #queryPupsByShelter()