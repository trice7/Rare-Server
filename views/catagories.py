import sqlite3
import json
from models import Catagory

def get_single_catagory(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
      SELECT
          c.id,
          c.label
      FROM Catagories c
      WHERE c.id = ?
      """, ( id, ))

        data = db_cursor.fetchone()

        catagory = Catagory(data['id'], data['label'])

        return json.dumps(catagory.__dict__)

def get_all_catagories():

    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Catagories c
        ORDER BY label COLLATE NOCASE ASC;
        """)

        catagories = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            catagory = Catagory(row['id'], row['label'])

            catagories.append(catagory.__dict__)

    return json.dumps(catagories)

def create_catagory(new_catagory):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Catagories
            ( label )
        VALUES
            ( ? );
        """, (new_catagory['label'], ))

        id = db_cursor.lastrowid

        new_catagory['id'] = id

    return json.dumps(new_catagory)
