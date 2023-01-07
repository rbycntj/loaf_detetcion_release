class User(object):
    def __int__(self):
        pass

    def __init__(self, id: int = None, username: str = None, password: str = None,
                 telephone: str = None, gender: int = None, img: str = None
                 ):
        self.__id = id
        self.__username = username
        self.__password = password
        self.__telephone = telephone
        self.__gender = gender
        self.__img = img

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        self.__id = id

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username: str):
        self.__username = username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password: str):
        self.__password = password

    @property
    def telephone(self):
        return self.__telephone

    @telephone.setter
    def telephone(self, telephone: str):
        self.__telephone = telephone

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, gender: int):
        self.__gender = gender

    @property
    def img(self):
        return self.__img

    @img.setter
    def img(self, img: str):
        self.__img = img
