import sqlite3


# Use this function to connect to the SQLite database.
# Always use this in a variable, never use it on standalone, please.
def get_db():
    return sqlite3.connect("database/db.sqlite")