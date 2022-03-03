import json


def load_db():
    with open("flashcards_db.json") as f:
        return json.load(f)


def save_db():
    with open("flashcards_db.json", "w") as db_file:
        json.dump(db, db_file)


db = load_db()
