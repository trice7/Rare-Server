import sqlite3
import json
from models import Reaction, Post_Reaction

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
      
def get_all_post_reactions():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
          a.id,
          a.user_id,
          a.post_id,
          a.reaction_id
        FROM postreactions a
        """)
        
        reactions = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            reaction = Post_Reaction(row['id'], row['user_id'], row['post_id'], row['reaction_id'])
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

def get_single_post_reaction(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor("""
        SELECT
          a.id,
          a.user_id,
          a.post_id,
          a.reaction_id
        """, ( id, ))
        
        data = db_cursor.fetchone()
        reaction = Post_Reaction(data['id'], data['user_id'], data['post_id'], data['reaction_id'])
        return reaction.__dict__


def create_post_reaction(new_post_reaction):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO postreactions
          ( user_id, post_id, reaction_id)
        VALUES
          ( ?, ?, ?)
        """, (new_post_reaction['user_id'], new_post_reaction['post_id'], new_post_reaction['reaction_id']))
        
        id = db_cursor.lastrowid
        new_post_reaction['id'] = id
    return new_post_reaction
  
def update_post_reaction(id, new_reaction):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE postreactions
          SET
            user_id,
            post_id,
            reaction_id
        WHERE id = ?
        """, (new_reaction['user_id'], new_reaction['post_id'], new_reaction['reaction_id']))
        
        rows_affected = db_cursor.rowcount
        
    if rows_affected == 0:
        return False
    else:
        return True
      
def delete_post_reaction(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM postreactions
        WHERE id =?
        """, (id, ))
