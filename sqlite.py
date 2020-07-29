import aiosqlite
from aiosqlite import Error
import discord


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
            longBoi = []
            slicedList = []
            longString = ''
            async for row in c:
                toAppend = map(str,row)
                toAppend = ' '.join(toAppend)
                summerLen = sum(len(i) for i in longBoi)
                if((len(toAppend))+summerLen <= 1850):
                    longBoi.append(''.join(toAppend))
                else:
                    longString = '\n'.join(longBoi)
                    slicedList.append(longString)
                    longBoi = []
                    longBoi.append(''.join(toAppend))
            remainderStr = '\n'.join(longBoi)
            slicedList.append(remainderStr)#dump last row
            return slicedList 
 
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
