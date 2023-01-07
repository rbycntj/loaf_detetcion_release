from .init import friend_blueprint
from services import friend_service
from utils.utils import *
from modules.result.response_result import *
from flask import request
import json, re, traceback

"""
    根据用户id查询好友
"""


@friend_blueprint.route("/friend/<id>", methods=['GET'])
def query_all_friend(id):
    rr = None
    try:
        rr = friend_service.query_all_friend(id)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.register_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)


"""
    通过好友申请
"""


@friend_blueprint.route("/friend", methods=['PUT'])
def pass_friend():
    uid = request.json.get("uid")
    fid = request.json.get("fid")
    # 判空
    if uid is None or fid is None or str(uid).strip() == "" or str(fid).strip() == "":
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.input_null)),
                          ensure_ascii=False)

    rr = None
    try:
        rr = friend_service.pass_friend(uid, fid)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.friend_pass_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)


"""
    拒绝好友申请
"""


@friend_blueprint.route("/friend", methods=['POST'])
def not_pass_friend():
    uid = request.json.get("uid")
    fid = request.json.get("fid")
    # 判空
    if uid is None or fid is None or str(uid).strip() == "" or str(fid).strip() == "":
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.input_null)),
                          ensure_ascii=False)
    rr = None
    try:
        rr = friend_service.not_pass_friend(uid, fid)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.friend_not_pass_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)


"""
    发送添加好友申请
"""


@friend_blueprint.route("/friend/<uid>", methods=['POST'])
def send_add_friend_msg(uid):
    telephone = request.json.get("telephone")
    telephone = str(telephone)
    # 判空
    if telephone is None or str(telephone).strip() == "":
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.input_null)),
                          ensure_ascii=False)
    # 判断手机号格式
    if not re.match(r"^1[35678]\d{9}$", telephone):
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.telephone_not_match)),
                          ensure_ascii=False)
    # 传递给业务层
    rr = None
    try:
        rr = friend_service.send_add_friend_msg(uid, telephone)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.send_add_friend_msg_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)


"""
    展示添加自己的 好友信息 列表
"""


@friend_blueprint.route("/friends/<uid>", methods=['GET'])
def query_add_friends_msg(uid):
    rr = None
    try:
        rr = friend_service.query_add_friends_msg(uid)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.query_add_friends_msg_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)


"""
    删除好友
"""


@friend_blueprint.route("/friend", methods=['DELETE'])
def delete_friend():
    uid = str(request.json.get("uid"))
    fid = str(request.json.get("fid"))
    # 判断删除自己
    if uid == fid:
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.delete_not_yourself)),
                          ensure_ascii=False)
    # 传递给业务层
    rr = None
    try:
        rr = friend_service.delete_friend(uid, fid)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.delete_friend_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)
