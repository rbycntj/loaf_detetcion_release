from .init import rank_blueprint
from services import rank_service
from modules.result.response_result import *
from utils.utils import obj_to_dict
from flask import request
import traceback
import json

"""
    根据用户id获取该用户排名和总学习时长
"""


@rank_blueprint.route("/rank/<id>", methods=['GET'])
def get_rank(id):
    rr = None
    try:
        rr = rank_service.get_rank(id)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.get_rank_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)


"""
    获取前XX名的排名信息
"""


@rank_blueprint.route("/ranks/<num>", methods=['GET'])
def get_all_rank(num):
    rr = None
    try:
        rr = rank_service.get_all_rank(num)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.get_rank_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)


"""
    根据用户id查看学习圈排名（即自己和好友的排名）
"""


@rank_blueprint.route("/ranks/friend/<id>", methods=['GET'])
def get_self_and_friends_rank(id):
    # 判空
    if id is None or str(id).strip() == "":
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.input_null)),
                          ensure_ascii=False)
    rr = None
    try:
        # 传递给业务层
        rr = rank_service.get_self_and_friends_rank(id)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.get_rank_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)
