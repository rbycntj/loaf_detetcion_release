import traceback

from modules.user import User
from modules.result.response_result import ResponseResult, ResultMessage
from services import user_service
from flask import request
from .init import user_blueprint
from utils.utils import obj_to_dict
import json
import re

"""
    登录
"""


@user_blueprint.route("/user", methods=['POST'])
def login():
    # 请求体参数
    telephone = request.json.get('telephone')
    password = request.json.get('password')
    # 转换类型
    if type(telephone) != str:
        telephone = str(telephone)
    # 判空
    if telephone is None or password is None or str(telephone).strip() == "" or str(password).strip() == "":
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.telephone_or_password_null)),
                          ensure_ascii=False)
    # 判断格式
    if not re.match(r"^1[35678]\d{9}$", telephone):
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.telephone_not_match)),
                          ensure_ascii=False)
    # 封装
    user = User(telephone=telephone, password=password)
    # 传递参数给业务层
    rr = None
    try:
        rr = user_service.login(user)
    except:
        print(traceback)
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.login_fail)), ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)


"""
    发送验证码
"""


@user_blueprint.route("/val", methods=['POST'])
def send_validate():
    telephone = request.json.get('telephone')
    # 格式转化
    if type(telephone) != str:
        telephone = str(telephone)
    # 判空
    if telephone is None or telephone.strip() == "":
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.telephone_null)),
                          ensure_ascii=False)
    # 格式判断
    if not re.match(r"^1[35678]\d{9}$", telephone):
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.telephone_not_match)),
                          ensure_ascii=False)
    # 传递参数给业务层
    rr = None
    try:
        rr = user_service.send_validate(telephone)
    except:
        print(traceback)
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.send_message_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)


"""
    注册
"""


@user_blueprint.route("/user", methods=['PUT'])
def register():
    telephone = request.json.get('telephone')
    validate_code = request.json.get('validate_code')
    password = request.json.get('password')
    reconfirm_password = request.json.get('reconfirm_password')
    # 格式校验
    if type(telephone) != str:
        telephone = str(telephone)
    # 判空
    if telephone is None or validate_code is None or password is None or reconfirm_password is None or str(telephone).strip() == "" or str(validate_code).strip() == "" or str(password).strip() == "" or str(reconfirm_password).strip() == "":
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.input_null)),
                          ensure_ascii=False)
    # 判断格式
    if not re.match(r"^1[35678]\d{9}$", telephone):
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.telephone_not_match)),
                          ensure_ascii=False)

    rr = None
    try:
        # 传递给业务层
        rr = user_service.register(telephone, validate_code, password, reconfirm_password)
    except:
        print(traceback)
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.register_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)

"""
    查询所有用户
"""
@user_blueprint.route("/users",methods=['GET'])
def query_all_users():
    rr = None
    try:
        rr = user_service.query_all_users()
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.query_friend_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)
