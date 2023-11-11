class User:
    def __init__(
        self,
        id,
        first_name,
        last_name,
        email,
        password,
        bio,
        username,
        profile_image_url,
        created_on,
        active,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.bio = bio
        self.username = username
        self.profile_image_url = profile_image_url
        self.created_on = created_on
        self.active = active
