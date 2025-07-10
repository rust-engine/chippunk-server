import sqlite3

# A function to connect to the local database, so we don't create a shit ton of connections which would overload our server
def get_db():
    return sqlite3.connect("database/db.sqlite")