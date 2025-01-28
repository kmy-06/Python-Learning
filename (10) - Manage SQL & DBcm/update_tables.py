import DBcm

db_details = "CoachDB.sqlite3"

import os

FOLDER = "swimdata/"

files = os.listdir(FOLDER) # grab list of filenames
files.remove(".DS_Store")


# A collection of SQL statements 

SQL_SELECT_SWIMMERS = """
    select * from swimmers
    where name = ? and age = ?
"""

SQL_INSERT_SWIMMERS = """
    insert into swimmers
    (name, age)
    values
    (?, ?)
"""

SQL_SELECT_EVENTS = """
    select * from events
    where distance = ? and stroke = ?
"""

SQL_INSERT_EVENTS = """
    insert into events
    (distance, stroke)
    values
    (?, ?)
"""

SQL_GET_SWIMMER = """
    select id from swimmers
    where name = ? and age = ?
"""

SQL_GET_EVENT = """
    select id from events
    where distance = ? and stroke = ?
"""

SQL_INSERT_TIMES = """
    insert into times
    (swimmer_id, event_id, time)
    values
    (?, ?, ?)
"""


with DBcm.UseDatabase(db_details) as db:
    for fn in files:
        name, age, distance, stroke = fn.removesuffix(".txt").split("-")

        # Add 'name' and 'age' to the "swimmers" table
        db.execute(SQL_SELECT_SWIMMERS,(name,age,),)
        if not db.fetchall(): # subsitute the "continue" statement with "if not"
            db.execute(SQL_INSERT_SWIMMERS,(name,age,),)

        # Add 'distance' and 'stroke' to the "events" table
        db.execute(SQL_SELECT_EVENTS,(distance,stroke,),)
        if not db.fetchall():
            db.execute(SQL_INSERT_EVENTS,(distance,stroke,),)

        # Add everything including 'time' to the "times" table
        db.execute(SQL_GET_SWIMMER,(name,age,),)
        s_id = db.fetchone()[0]

        db.execute(SQL_GET_EVENT,(distance,stroke,),)
        e_id = db.fetchone()[0]

        with open(FOLDER + fn) as sf:
            times = sf.read().strip().split(",")
            for t in times:
                db.execute(SQL_INSERT_TIMES,(s_id,e_id,t,),)