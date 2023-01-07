class StudyRecord(object):
    def __init__(self, total_time, cur_date):
        self.__total_time = total_time
        self.__cur_date = cur_date

    @property
    def total_time(self):
        return self.__total_time

    @total_time.setter
    def total_time(self, total_time):
        self.__total_time = total_time

    @property
    def cur_date(self):
        return self.__cur_date

    @cur_date.setter
    def cur_date(self, cur_date):
        self.__cur_date = cur_date
