#import sqlite3
#from sqlite3 import Error
import aiosqlite
from aiosqlite import Error


async def insert_table(name, ideas):
    conn = None
    try:
        conn = await aiosqlite.connect('idea.db')
    except Error as e:
        print("unexppected error has occured while attempting to connect to the db: ", e)

    if conn is not None:
        try:
            await conn.execute("INSERT INTO IDEAS (ID, NAME, IDEA) VALUES (?, ?, ?)", (None, name, ideas))
            await conn.commit()
            print("Idea recorded")
        except Error as e:
            print("error at insert: ", e)
    else:
        await print("Connection creation failed, try again later or whatever zzzz")
    await conn.close()

async def read_table():
    conn = None
    try:
        conn = await aiosqlite.connect('idea.db')
    except Error as e:
        print("unexppected error has occured while attempting to connect to the db: ", e)

    if conn is not None:
        try:
            c = await conn.execute("""SELECT * FROM IDEAS""")
            async for row in c: #temp printout until desired output format is debated
                print("ID = ", row[0])
                print("NAME = ", row[1])
                print("IDEA = ", row[2], "\n")
                print('forrowtest')
            print('test')
        except Error as e:
            print("error at read table: ", e)
    else:
        print("Connection creation failed, try again later or whatever zzzz")
    await conn.close()

async def wipe_table():
    conn = None
    try:
        conn = await aiosqlite.connect('idea.db')
    except Error as e:
        print("unexppected error has occured while attempting to connect to the db: ", e)
        
    if conn is not None:
        try:
            c = await conn.execute("""DELETE FROM IDEAS""")
            await conn.commit()
        except Error as e:
            print("error at read table: ", e)
    else:
        print("Connection creation failed, try again later or whatever zzzz")
    await conn.close()
