import sqlite3

def init_db():
    connection = sqlite3.connect('database.db')

    with open('schema.sql') as f:
        connection.executescript(f.read())

    # Create a cursor object
    cur = connection.cursor()

    connection.commit()
    connection.close()

if __name__ == '__main__':
    init_db()
