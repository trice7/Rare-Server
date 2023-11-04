class Subscription():
    def __init__(self, id, follower_id, author_id, created_on):
        self.id = id
        self.author_id = author_id
        self.created_on = created_on
        self.follower_id = follower_id
