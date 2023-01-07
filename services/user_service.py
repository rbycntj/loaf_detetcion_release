import uuid
from typing import Type
from modules.user import User
from database.mysql_connection import get_mysql_connect
from database.redis_connection import get_redis_connection
from modules.result.response_result import ResponseResult, ResultMessage
from utils.tencent import send_message
import pymysql
import random
import traceback

"""
登录功能
"""


def login(user: Type[User]):
    con = None
    cursor = None
    try:
        # 获取连接
        con = get_mysql_connect()
        cursor = con.cursor()
        # 查询
        cursor.execute("select id from tb_user where telephone=%s and password=%s;", (user.telephone, user.password))
        id = cursor.fetchone()
        if id is None or id[0] is None:
            return ResponseResult(flag=False, msg=ResultMessage.telephone_or_password_wrong)
        else:
            return ResponseResult(flag=True, msg=ResultMessage.login_success, obj=id[0])
    except:
        print(traceback.format_exc())
        return ResponseResult(flag=False, msg=ResultMessage.login_fail)
    finally:
        if con is not None:
            con.close()
        if cursor is not None:
            cursor.close()


"""
发送验证码
"""


def send_validate(telephone: str):
    # 生成六位验证码
    validate_code = random.randrange(100000, 999999, 1)
    # 存入redis数据库中
    con = None
    try:
        con = get_redis_connection()
        con.setex(name=str(telephone + "/val"), value=validate_code, time=300)
    except:
        print(traceback.format_exc())
        return ResponseResult(flag=False, msg=ResultMessage.send_message_fail)
    finally:
        if con is not None:
            con.close()
    # 发送短信
    try:
        send_message(validate_code=str(validate_code), telephone=telephone)
    except:
        print(traceback.format_exc())
        return ResponseResult(flag=False, msg=ResultMessage.send_message_fail)
    return ResponseResult(flag=True, msg=ResultMessage.send_message_success)


"""
注册
"""


def register(telephone: str, validate_code: str, password: str, reconfirm_password: str):
    mysql_con = None
    cursor = None
    redis_con = None
    try:
        mysql_con = get_mysql_connect()
        cursor = mysql_con.cursor()
        mysql_con.begin()
        # 检查手机号是否注册过
        cursor.execute("select id from tb_user where telephone=%s", (telephone))
        id = cursor.fetchone()
        if id is not None:
            return ResponseResult(flag=False, msg=ResultMessage.telephone_used)
        # 检查验证码是否正确
        redis_con = get_redis_connection()
        redis_validate_code = redis_con.get(str(telephone + "/val"))
        if validate_code is None:
            return ResponseResult(flag=False, msg=ResultMessage.validate_code_timeout)
        if str(redis_validate_code) != str(validate_code):
            # 验证码不相等
            return ResponseResult(flag=False, msg=ResultMessage.validate_code_wrong)
        # 验证密码是否一致
        if password != reconfirm_password:
            return ResponseResult(flag=False, msg=ResultMessage.password_not_equal)
        # 添加新用户
        cursor.execute("insert into tb_user(username,telephone,password) values(%s,%s,%s)",
                       (uuid.uuid4(), telephone, password))
        mysql_con.commit()
    except:
        print(traceback.format_exc())
        mysql_con.rollback()
        return ResponseResult(flag=False, msg=ResultMessage.register_fail)
    finally:
        if mysql_con is not None:
            mysql_con.close()
        if cursor is not None:
            cursor.close()
        if redis_con is not None:
            redis_con.close()
    return ResponseResult(flag=True, msg=ResultMessage.register_success)


"""
    查询所有用户
"""


def query_all_users():
    obj = None
    con = None
    cursor = None
    try:
        # 获取数据库连接
        con = get_mysql_connect()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        # 查询全部用户
        cursor.execute("select * from tb_user")
        query_users = cursor.fetchall()
        user_list = []
        for qu in query_users:
            user = User(id=qu['id'], username=qu['username'], password=qu['password'], telephone=qu['telephone'],
                        gender=qu['gender'], img=qu['img'])
            user_list.append(user)
        obj = user_list
    except:
        print(traceback)
        return ResponseResult(flag=False, msg=ResultMessage.query_all_users_fail)
    finally:
        if con is not None:
            con.close()
        if cursor is not None:
            cursor.close()
    return ResponseResult(flag=True, msg=ResultMessage.query_all_users_success, obj=obj)
