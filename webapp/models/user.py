class User:
    def __init__(self, email):
        self.email = email
        self.username = None
        self.family_name = None
        self.nickname = None
        self.preferred_username = None

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    @staticmethod
    def find_or_create_by_email(email):
        return User(email)

    @staticmethod
    def find_by_id(id):
        return User(id)

