import sqlite3
import json
from models import Post, Tag, Category, Reaction

def get_all_posts():
    # Open a connection to the database
     with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_tags = conn.cursor()
        db_reactions = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.category_id,
            a.title,
            a.publication_date,
            a.image_url,
            a.content
        FROM posts a
        """)

        # Initialize an empty list to hold all post representations
        posts = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            db_tags.execute("""
            SELECT
                p.id as pid,
                p.user_id, p.title,
                pt.id as ptid,
                pt.post_id,
                pt.tag_id,
                t.id,
                t.label
            FROM Posts p
            JOIN PostTags pt
                ON p.id = pt.post_id
            JOIN Tags t
                on pt.tag_id = t.id
            WHERE p.id = ?
            
            """, ( row['id'], ))
            
            db_reactions.execute("""
            SELECT p.id as pid, p.title, pr.id as prid, pr.user_id, pr.reaction_id, pr.post_id, r.id, r.label, r.image_url
            from Posts p
            join PostReactions pr
                on p.id = pr.post_id
            JOIN Reactions r
                on pr.reaction_id = r.id
            WHERE pid = ?                     
            """, (row['id'] ,))
            
            tagsdata = db_tags.fetchall()
            reactionsdata = db_reactions.fetchall()
            # Create an post instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # post class above.
            
            
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                            row['publication_date'], row['image_url'],
                            row['content'])
            
            for row in tagsdata:
                tag = Tag(row['id'], row['label'])
                post.tags.append(tag.__dict__)
        
            for row in reactionsdata:
                reaction = Reaction(row['id'], row['label'], row['image_url'])
                reaction_dict = {**reaction.__dict__, 'user_id': row['user_id']}
                post.reactions.append(reaction_dict)

            posts.append(post.__dict__) # see the notes below for an explanation on this line of code.

     return posts
  
def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_tags = conn.cursor()
        db_reactions = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.category_id,
            a.title,
            a.publication_date,
            a.image_url,
            a.content
        FROM posts a
        WHERE a.id = ?
        """, ( id, ))
        
        db_tags.execute("""
        SELECT
            p.id as pid,
            p.user_id, p.title,
            pt.id as ptid,
            pt.post_id,
            pt.tag_id,
            t.id,
            t.label
        FROM Posts p
        JOIN PostTags pt
            ON p.id = pt.post_id
        JOIN Tags t
            on pt.tag_id = t.id
        WHERE p.id = ?
        
        """, ( id, ))
        
        db_reactions.execute("""
        SELECT p.id as pid, p.title, pr.id as prid, pr.user_id, pr.reaction_id, pr.post_id, r.id, r.label, r.image_url
        from Posts p
        join PostReactions pr
            on p.id = pr.post_id
        JOIN Reactions r
            on pr.reaction_id = r.id
        WHERE pid = ?                     
        """, (id ,))

        # Load the single result into memory
        data = db_cursor.fetchone()
        tagsdata = db_tags.fetchall()
        reactionsdata = db_reactions.fetchall()

        # Create an post instance from the current row
        post = Post(data['id'], data['user_id'], data['category_id'], data['title'],
                            data['publication_date'], data['image_url'],
                            data['content'])
        
        for row in tagsdata:
            tag = Tag(row['id'], row['label'])
            post.tags.append(tag.__dict__)
        
        for row in reactionsdata:
            reaction = Reaction(row['id'], row['label'], row['image_url'])
            reaction_dict = {**reaction.__dict__, 'user_id': row['user_id']}
            post.reactions.append(reaction_dict)
            

        return post.__dict__

def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO posts
            ( user_id, category_id, title, publication_date, image_url, content )
        VALUES
            ( ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'],
                new_post['title'], new_post['publication_date'],
                new_post['image_url'], new_post['content'] ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the post dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post['id'] = id


    return new_post

def delete_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (id, ))
        
def update_post(id, new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE posts
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?
        WHERE id = ?
        """, (new_post['user_id'], new_post['category_id'],
            new_post['title'], new_post['publication_date'],
            new_post['image_url'], new_post['content'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    # return value of this function
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
        
