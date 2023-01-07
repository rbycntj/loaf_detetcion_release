from typing import Type
from .user import *


class Friend(object):
    def __init__(self, id=None, user_id=None, friend_id=None, friend: Type[User] = None):
        self.__id = id
        self.__user_id = user_id
        self.__friend_id = friend_id
        self.__friend = friend

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def friend_id(self):
        return self.__friend_id

    @friend_id.setter
    def friend_id(self, friend_id):
        self.__friend_id = friend_id

    @property
    def friend(self):
        return self.__friend

    @friend.setter
    def friend(self, friend: Type[User]):
        self.__friend = friend
