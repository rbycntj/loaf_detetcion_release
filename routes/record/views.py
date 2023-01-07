from .init import record_blueprint
from services import record_service
from utils.utils import obj_to_dict
from modules.result.response_result import *
from flask import request
import traceback
import json

"""
    计时开始
"""


@record_blueprint.route("/record/<id>", methods=['POST'])
def start_record(id):
    rr = None
    try:
        rr = record_service.start_record(id)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.add_record_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)


"""
    计时结束
"""


@record_blueprint.route("/record/<id>", methods=['PUT'])
def end_record(id):
    # 获取参数
    record_id = request.json.get("record_id")
    valid = request.json.get("valid")
    score = request.json.get("score")
    if valid is None or score is None or record_id is None or str(valid).strip() == 1 or str(score).strip() == 1 or str(
            record_id).strip() == "":
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.input_null)),
                          ensure_ascii=False)

    # 传递给业务层
    rr = None
    try:
        rr = record_service.end_record(id=id, record_id=record_id, valid=valid, score=score)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.update_record_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)


"""
    根据用户id查询近十天历史学习记录
"""


@record_blueprint.route("/record/<id>", methods=['GET'])
def get_study_record(id):
    rr = None
    try:
        rr = record_service.get_study_record(id=id)
    except:
        print(traceback.format_exc())
        return json.dumps(obj_to_dict(ResponseResult(flag=False, msg=ResultMessage.get_study_record_fail)),
                          ensure_ascii=False)
    return json.dumps(obj_to_dict(rr), ensure_ascii=False)
