"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""

import logging
from peewee import *
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
database_path = '/Users/dahart/git/Sp2018-Online/students/darrell/wk7_assignments/personjob.db'

if os.path.isfile(database_path):
    logger.info('Removing old database file')
    os.remove(database_path)

logger.info('Initializing Database')
database = SqliteDatabase('personjob.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only


class BaseModel(Model):
    class Meta:
        database = database

class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)


class Department(BaseModel):
    """
        This is the department class
    """
    department_name = CharField(max_length=30, null=False)
    department_number = CharField(max_length=4, primary_key=True)
    department_manager = CharField(max_length=30, null=False)
    person_in_department = ForeignKeyField(Person, related_name='in_department', null=False)


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    job_name = CharField(primary_key = True, max_length = 30)
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')
    salary = DecimalField(max_digits = 7, decimal_places = 2)
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null = False)



if __name__ == "__main__":
    logger.info('Creating Tables')
    database.create_tables([
            Job,
            Person,
            Department,
        ])
    logger.info('Closing database')
    database.close()
