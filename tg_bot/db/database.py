import sqlite3


def add_user(msg):
    with sqlite3.connect('traveller.db') as con:
        cursor = con.cursor()
        cursor.execute('INSERT INTO travel (user_id, place_flag) VALUES (?, ?)',
                       (msg.from_user.id, False))
        con.commit()


def get_place(msg):
    with sqlite3.connect('traveller.db') as con:
        cursor = con.cursor()
        cursor.execute(f'SELECT place, place_flag FROM travel WHERE user_id=={msg.from_user.id}')
        data = cursor.fetchall()
    return data


def insert_place(msg, place):
    with sqlite3.connect('traveller.db') as con:
        cursor = con.cursor()
        cursor.execute('INSERT INTO travel (user_id, place, place_flag) VALUES (?, ?, ?)',
                       (msg.from_user.id, place, True))
        con.commit()


def new_day():
    with sqlite3.connect('traveller.db') as con:
        cursor = con.cursor()
        cursor.execute('UPDATE travel SET place_flag = FALSE')
        con.commit()
