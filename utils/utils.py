"""
    读取Properties文件
"""


class Properties:
    def __init__(self, file_name):
        self.file_name = file_name

    def getProperties(self):
        try:
            pro_file = open(self.file_name, 'r', encoding='utf-8')
            properties = {}
            for line in pro_file:
                if line.find('=') > 0:
                    strs = line.replace('\n', '').split('=')
                    properties[strs[0]] = strs[1]
        except Exception as e:
            raise e
        else:
            pro_file.close()
        return properties


from modules import user, friend, rank_info, study_record
from modules.result import response_result

"""
    将obj转为json，手动转变
"""


def obj_to_dict(obj):
    if obj is None:
        return None
    if type(obj) == response_result.ResponseResult:
        res_dict = dict()
        res_dict['flag'] = obj_to_dict(obj.flag)
        res_dict['msg'] = obj_to_dict(obj.msg)
        res_dict['obj'] = obj_to_dict(obj.obj)
        return res_dict
    if type(obj) == user.User:
        res_dict = dict()
        res_dict['id'] = obj_to_dict(obj.id)
        res_dict['username'] = obj_to_dict(obj.username)
        res_dict['password'] = obj_to_dict(obj.password)
        res_dict['telephone'] = obj_to_dict(obj.telephone)
        res_dict['gender'] = obj_to_dict(obj.gender)
        res_dict['img'] = obj_to_dict(obj.img)
        return res_dict
    if type(obj) == int or type(obj) == str or type(obj) == bool or type(obj) == float:
        return obj
    if type(obj) == friend.Friend:
        res_dict = dict()
        res_dict['id'] = obj_to_dict(obj.id)
        res_dict['user_id'] = obj_to_dict(obj.user_id)
        res_dict['friend_id'] = obj_to_dict(obj.friend_id)
        res_dict['friend'] = obj_to_dict(obj.friend)
        return res_dict
    if type(obj) == list:
        res_list = []
        for item in obj:
            res_list.append(obj_to_dict(item))
        return res_list
    if type(obj) == rank_info.RankInfo:
        res_dict = dict()
        res_dict['rank'] = obj_to_dict(obj.rank)
        res_dict['total_time'] = obj_to_dict(obj.total_time)
        res_dict['user'] = obj_to_dict(obj.user)
        return res_dict
    if type(obj) == study_record.StudyRecord:
        res_dict = dict()
        res_dict['total_time'] = obj_to_dict(int(obj.total_time))
        res_dict['cur_date'] = obj_to_dict(str(obj.cur_date))
        return res_dict
