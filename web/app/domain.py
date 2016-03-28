# Simple User Model
class User():

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __init__(self, email, password, authenticated):
        self.email = email
        self.password = password
        self.authenticated = authenticated
