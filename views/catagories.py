import sqlite3
import json
from models import Catagory

def get_all_catagory():
    """gets all catagories"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Catagories c
        """)

        catagories = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            catagory = Catagory(row['id'], row['label'])
            catagories.append(catagory.__dict__)

    return catagories

def get_single_catagory(id):
    """gets single catagory"""
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

        return catagory.__dict__

def create_catagory(new_catagory):
    """creates new catagory"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Catagories
            (label)
        VALUES
            (?);
        """, (new_catagory['label'],))

        id = db_cursor.lastrowid
        new_catagory['id'] = id

def update_catagory(id, new_catagory):
    """updates catagory"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Catagories
            SET
                label = ?
        WHERE id = ?
        """, (new_catagory['label'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True
