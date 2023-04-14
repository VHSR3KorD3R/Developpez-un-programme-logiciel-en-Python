import os

from tinydb import TinyDB


def connect():
    current_directory = os.getcwd()
    print(current_directory)
    db_path = os.path.join(current_directory, "chess_tournament_db.json")
    db = TinyDB(db_path)
    return db


def players():
    db = connect()
    return db.table("players")


def tournaments():
    db = connect()
    return db.table("tournaments")
