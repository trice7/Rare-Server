import sqlite3
import json
from models import Tag, PostTag

def get_all_tags():
    """gets all Tags"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Tags c
        """)

        Tags = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['label'])
            Tags.append(tag.__dict__)

    return Tags

def get_single_tag(id):
    """gets single tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Tags c
        WHERE c.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        tag = Tag(data['id'], data['label'])

        return tag.__dict__
    
def create_tag(new_tag):
    """creates new tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tags
            (label)
        VALUES
            (?)
        """, (new_tag['label'], ))

        id = db_cursor.lastrowid
        new_tag['id'] = id
    return new_tag

def update_tag(id, new_tag):
    """updates tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Tags
            SET
                label = ?
        WHERE id = ?
        """, (new_tag['label'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

def delete_tag(id):
    """deletes Tags"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Tags
        WHERE id = ?
        """, (id, ))
        
# Post Tags


def get_all_post_tags():
    """gets all Tags"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.post_id, 
            c.tag_id
        FROM PostTags c
        """)

        Tags = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = PostTag(row['id'], row['post_id'], row['tag_id'])
            Tags.append(tag.__dict__)
            
    return Tags

def get_single_post_tag(id):
    """gets single post tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.post_id, 
            c.tag_id
        FROM PostTags c
        WHERE c.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        posttag = PostTag(data['id'], data['post_id'], data['tag_id'])

        return posttag.__dict__
    
def create_post_tag(new_tag):
    """creates new tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO PostTags
            ( post_id, tag_id )
        VALUES
            ( ?, ? )
        """, (new_tag['post_id'], new_tag['tag_id'] ))

        id = db_cursor.lastrowid
        new_tag['id'] = id
    return new_tag

def update_post_tag(id, new_tag):
    """updates tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE PostTags
            SET
                post_id = ?,
                tag_id = ?
        WHERE id = ?
        """, (new_tag['post_id'], new_tag['tag_id'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

def delete_post_tag(id):
    """deletes Tags"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM PostTags
        WHERE id = ?
        """, (id, ))
