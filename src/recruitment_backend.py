import json
import sqlite3
from pprint import pprint
from peewee import *
import datetime
import base64
import ast

from playhouse.sqlite_ext import JSONField
from playhouse.shortcuts import model_to_dict



db = SqliteDatabase('persons.sqlite3')

class Person(Model):
    gender = CharField()
    name = CharField()
    location = CharField()
    email = CharField()
    login = CharField()
    dob = CharField()
    registered = CharField()
    phone = CharField()
    cell = CharField()
    id_ = CharField()
    picture = CharField(null=True)
    nat = CharField()
    count_dob = IntegerField()


    class Meta:
        database = db

    def dob_to_dict(self):
        return model_to_dict(self.dob)


    def clean_number(self, number):
        return ''.join(char for char in number if char.isalnum())

    def clean_date(self):
        return datetime.datetime.strptime(self.dob['date'], "%Y-%m-%dT%H:%M:%S.%fZ")



    def count_days(self):
        flag = 0
        now = datetime.datetime.now()
        dob = self.clean_date()
        if now.month > dob.month or (now.month == dob.month and now.day > dob.day):
            flag = 1
        try:
            dob_now = datetime.datetime(now.year + flag, dob.month, dob.day)
        except ValueError:  # leap year
            dob_now = datetime.datetime(now.year + flag, dob.month + 1, 1)  
        return int((dob_now - now).days) + 1


if __name__ == "__main__":
    
    db.connect()

    db.create_tables([Person])



    # TASK 1
    with open('persons.json', encoding='utf8') as persons:
        persons_data = json.load(persons)
        

    # for person in persons_data['results'][:2]:
    #     p = Person(gender=person['gender'], name=person['name'], location=person['location'], email=person['email'], 
    #                 login=person['login'], dob=person['dob'], registered=person['registered'], phone=person['phone'],
    #                 cell=person['cell'], id_=person['id'], picture=person['picture'], nat=person['nat'])


    #     p.count_dob = p.count_days()
    #     p.phone = p.clean_number(p.phone)
    #     p.cell = p.clean_number(p.cell)
    #     p.picture = None
    #     # p.login['password'] = base64.b64encode(p.login['password'].encode('utf-8'))
    #     p.save()