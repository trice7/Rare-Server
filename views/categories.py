import sqlite3
import json
from models import Category

def get_all_category():
    """gets all categories"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        """)

        categories = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            category = Category(row['id'], row['label'])
            categories.append(category.__dict__)

    return categories

def get_single_category(id):
    """gets single category"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        WHERE c.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        category = Category(data['id'], data['label'])

        return category.__dict__

def create_category(new_category):
    """creates new category"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Categories
            (label)
        VALUES
            (?)
        """, (new_category['label'], ))

        id = db_cursor.lastrowid
        new_category['id'] = id
    return new_category

def update_category(id, new_category):
    """updates category"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Categories
            SET
                label = ?
        WHERE id = ?
        """, (new_category['label'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

def delete_category(id):
    """deletes categories"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Categories
        WHERE id = ?
        """, (id, ))
