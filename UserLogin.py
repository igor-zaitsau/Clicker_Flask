class UserLogin():
    def fromDB(self, userID, connect):
        self.__user = connect.getUser(userID)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return int(self.__user['id'])
