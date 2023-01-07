from .init import personal_info_blueprint
from flask import request
from services import personal_info_service
from utils.utils import *
from modules.result.response_result import *
from modules.user import User
import traceback
import json

"""
    根据id查询个人信息
"""


@personal_info_blueprint.route("/info/<id>", methods=['GET'])
def query_personal_info(id):
    if id is None or str(id).strip() == "":
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.id_null)),
                          ensure_ascii=False)
    rr = None
    try:
        rr = personal_info_service.query_personal_info(id)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.query_personal_info_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr),
                      ensure_ascii=False)


"""
    根据id更新个人信息,不更新手机信息
"""


@personal_info_blueprint.route("/info", methods=['PUT'])
def update_personal_info():
    id = request.json.get("id")
    username = request.json.get("username")
    password = request.json.get("password")
    gender = request.json.get("gender")

    # 判空
    if id is None or username is None or password is None or gender is None or str(id).strip() == "" or str(
            username).strip() == "" or str(password).strip() == "" or str(gender).strip() == "":
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.input_null)),
                          ensure_ascii=False)
    # 封装
    user = User(id=id, username=username, password=password, gender=gender)
    # 传递给业务层
    rr = None
    try:
        rr = personal_info_service.update_personal_info(user)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.update_personal_info_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)


"""
    根据用户id修改头像
"""


@personal_info_blueprint.route("/info", methods=['POST'])
def update_personal_img():
    id = request.json.get("id")
    img = request.json.get("img")
    # 判空
    if id is None or img is None or str(id).strip() == "" or str(img).strip() == "":
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.input_null)),
                          ensure_ascii=False)
    # 传递给业务层
    rr = None
    try:
        rr = personal_info_service.update_personal_img(id, img)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.update_personal_img_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)
