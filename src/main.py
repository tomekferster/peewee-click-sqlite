import json
import sqlite3
import datetime
import requests
from peewee import *

db = SqliteDatabase('persons.sqlite3')


class BaseModel(Model):
    """
    Every other class inherits the db setting from this 'BaseModel' class
    """
    class Meta:
        database = db


class Person(BaseModel):
    gender = CharField()
    email = CharField()
    phone = CharField()
    cell = CharField()
    nat = CharField()

    def clean_number(self, number):
        return ''.join(char for char in number if char.isalnum())


class Name(BaseModel):
    person = ForeignKeyField(Person, backref="name")
    title = CharField()
    first = CharField()
    last = CharField()


class Location(BaseModel):
    person = ForeignKeyField(Person, backref="location")
    city = CharField()
    state = CharField()
    postcode = CharField()


class Street(BaseModel):
    location = ForeignKeyField(Location, backref="street")
    number = IntegerField()
    name = CharField()


class Coordinates(BaseModel):
    location = ForeignKeyField(Location, backref="coordinates")
    latitude = CharField()
    longitude = CharField()


class Timezone(BaseModel):
    location = ForeignKeyField(Location, backref="timezone")
    offset = CharField()
    description = CharField()


class Login(BaseModel):
    person = ForeignKeyField(Person, backref="login")
    uuid = CharField()
    username = CharField()
    password = CharField()
    salt = CharField()
    md5 = CharField()
    sha1 = CharField()
    sha256 = CharField()


class Dob(BaseModel):
    person = ForeignKeyField(Person, backref="dob")
    date = CharField()
    age = IntegerField()
    count_dob = IntegerField()

    def count_days(self):
        """
        Method for counting how many days has left to the next birthday
        """
        flag = 0
        now = datetime.datetime.now()
        dob = datetime.datetime.strptime(self.date, "%Y-%m-%dT%H:%M:%S.%fZ")
        if now.month > dob.month or (now.month == dob.month and now.day > dob.day):
            flag = 1
        try:
            dob_now = datetime.datetime(now.year + flag, dob.month, dob.day)
        except ValueError:  # leap year
            dob_now = datetime.datetime(now.year + flag, dob.month + 1, 1)  
        return int((dob_now - now).days) + 1


class Registered(BaseModel):
    person = ForeignKeyField(Person, backref="dob")
    date = CharField()
    age = IntegerField()


class Id(BaseModel):
    person = ForeignKeyField(Person, backref="id_")
    name = CharField()
    value = CharField(null=True)
    


def json_or_API():
    """
    Function for loading the data from json file or API
    """
    while True:
        decision = input("Press:\n1 - to load the data from 'persons.json' file\n2 - to load the data from API:\n")
        if decision == '1' or decision == '2':
            break

    # OPEN JSON FILE AND POPULATE THE TABLES
    if decision == '1':
        with open('persons.json', encoding='utf8') as persons_json:
            persons = json.load(persons_json)

    # OPEN API URL AND POPULATE THE TABLES
    elif decision == '2':
        while True:
            try:
                quantity = int(input('How many random people would you like to put in the DB?: '))
                break
            except:
                print("It has to be a number!")
                continue

        url = f'https://randomuser.me/api/?results={quantity}&exc=picture'
        r = requests.get(url)
        persons = json.loads(r.content, encoding='utf8')
    
    return persons


def create_populate_table():
    """
    Function for creating and populating the database
    """

    # CONNECT TO THE SQLITE DB AND CREATE TABLES
    db.connect()
    db.create_tables([Person, Name, Location, Street, Coordinates, Timezone, Login, Dob, Registered, Id])

    # CHOOSE IF YOU WANT TO LOAD THE DATA FROM FILE OR API
    persons = json_or_API()

    print("Wait until you get a notification! This may take a while...")

    # POPULATE THE DB
    for person in persons['results']:
        p = Person(
                    gender=person['gender'],
                    email=person['email'],
                    phone=person['phone'],
                    cell=person['cell'],
                    nat=person['nat']
                    )
        p.phone = p.clean_number(p.phone)
        p.cell = p.clean_number(p.cell)

        n = Name(
                person=p,
                title=person['name']['title'],
                first=person['name']['first'],
                last=person['name']['last']
                )

        l = Location(
                    person=p,
                    city=person['location']['city'],
                    state=person['location']['state'],
                    postcode=person['location']['postcode']
                    )

        s = Street(
                    location=l,
                    number=person['location']['street']['number'],
                    name=person['location']['street']['name']
                    )

        c = Coordinates(
                        location=l,
                        latitude=person['location']['coordinates']['latitude'],
                        longitude=person['location']['coordinates']['longitude']
                        )

        t = Timezone(
                    location=l,
                    offset=person['location']['timezone']['offset'],
                    description=person['location']['timezone']['description']
                    )
        
        log = Login(
                    person=p,
                    uuid=person['login']['uuid'],
                    username=person['login']['username'],
                    password=person['login']['password'],
                    salt=person['login']['salt'],
                    md5=person['login']['md5'],
                    sha1=person['login']['sha1'],
                    sha256=person['login']['sha256']
                    )

        d = Dob(
                person=p,
                date=person['dob']['date'],
                age=person['dob']['age']
                )
        d.count_dob = d.count_days()
        
        r = Registered(
                        person=p,
                        date=person['registered']['date'],
                        age=person['registered']['age']
                        )
        
        i = Id(
                person=p,
                name=person['id']['name'],
                value=person['id']['value']
                )

        # SAVE DATA
        p.save()
        n.save()
        l.save()
        s.save()
        c.save()
        t.save()
        log.save()
        d.save()
        r.save()
        i.save()

    # CLOSE THE DB
    db.close()
    print("DONE!")

if __name__ == "__main__":
    
    create_populate_table()