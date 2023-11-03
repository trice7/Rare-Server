import sqlite3
import json
from models import Subscription

def get_all_subscriptions():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            a.id,
            a.follower_id,
            a.author_id,
            a.created_on
        FROM Subscription a               
        """)
        
        subscriptions = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            subscription = Subscription(row['id'], row['follower_id'], row['author_id'], row['created_on'])
            
            subscriptions.append(subscription.__dict__)
            
    return subscriptions

def create_subscription(new_subscription):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO Subscription
            ( follower_id, author_id, created_on )
            
        VALUES
            ( ?, ?, ?, ?)
        """, (new_subscription['follower_id'], new_subscription['author_id'], new_subscription['created_on'], ))
        
        id = db_cursor.lastrowid
        new_subscription['id'] = id
    return new_subscription

def delete_subscription(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        DELETE FROM subscription
        WHERE id = ?
        """, (id, ))
        
def update_subscription(id, new_subscription):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Subscription
          SET
            follower_id = ?,
            author_id = ?,
            created_on = ?
        WHERE id = ?    
        """, (new_subscription['follower_id'], new_subscription['author_id'], new_subscription['created_on'], id, ))
        
        rows_affected = db_cursor.rowcount
        
    if rows_affected == 0:
        return False
    else:
        return True

def get_single_subscription():
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
          a.id,
          a.follower_id,
          a.author_id,
          a.created_on
        FROM subscriptions a
        WHERE a.id = ?                
        """, (id, ))
        
        data = db_cursor.fetchone()
        
        subscription = Subscription(data['id'], data['follower_id'], data['author_id'], data['created_on'])
        
        return subscription.__dict__
