from typing import Type
from .user import User


class RankInfo(object):
    def __init__(self, rank=None, total_time=None, user: Type[User] = None):
        self.__rank = rank
        self.__total_time = total_time
        self.__user = user

    @property
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, rank):
        self.__rank = rank

    @property
    def total_time(self):
        return self.__total_time

    @total_time.setter
    def total_time(self, total_time):
        self.__total_time = total_time

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user: Type[User]):
        self.__user = user
