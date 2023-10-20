import sqlite3


def create_table():
    conn = sqlite3.connect('traveller.db')

    cursor = conn.cursor()
    try:
        query = ('CREATE TABLE IF NOT EXISTS "travel"'
                 ' ("ID" INTEGER UNIQUE, "user_id" INTEGER, "place" TEXT,'
                 ' "place_flag" INTEGER DEFAULT 0, PRIMARY KEY ("ID"))')
        cursor.execute(query)
    except:
        pass
