import sqlite3
import json
from models import Reaction

def get_all_reactions():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
          a.id,
          a.label,
          a.image_url
        FROM Reactions a
        """)
        
        reactions = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            reaction = Reaction(row['id'], row['label'], row['image_url'])
            
            reactions.append(reaction.__dict__)
        return reactions

def get_single_reaction(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
          a.id,
          a.label,
          a.image_url
        FROM Reactions a
        WHERE a.id = ?
        """, (id, ))
        
        data = db_cursor.fetchone()
        
        reaction = Reaction(data['id'], data['label'], data['image_url'])
        
        return reaction.__dict__
