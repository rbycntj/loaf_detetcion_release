from database.mysql_connection import *
from modules.result.response_result import *
from modules.user import *
from typing import Type
import traceback

"""
    根据id查询个人信息,用于回显
"""


def query_personal_info(id: str):
    con = None
    cursor = None
    user = None
    try:
        # 获取连接
        con = get_mysql_connect()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        # 根据id查询
        cursor.execute("select * from tb_user where id=%s;", id)
        info = cursor.fetchone()
        if info is None:
            return ResponseResult(flag=False, msg=ResultMessage.user_not_found)
        user = User()
        user.username = info['username']
        user.password = info['password']
        user.id = info['id']
        user.telephone = info['telephone']
        user.gender = info['gender']
        user.img = info['img']
    except:
        print(traceback.format_exc())
        return ResponseResult(flag=False, msg=ResultMessage.query_personal_info_fail)
    finally:
        if con is not None:
            con.close()
        if cursor is not None:
            cursor.close()
    return ResponseResult(flag=True, msg=ResultMessage.query_personal_info_success, obj=user)


"""
    根据id更新个人信息
"""


def update_personal_info(user: Type[User]):
    con = None
    cursor = None
    flag = None
    try:
        con = get_mysql_connect()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        # 根据id更新个人信息
        con.begin()
        flag = cursor.execute("update tb_user set username=%s,password=%s,gender=%s where id=%s",
                              (user.username, user.password, user.gender, user.id))
        con.commit()
    except:
        print(traceback.format_exc())
        con.rollback()
        return ResponseResult(flag=False, msg=ResultMessage.update_personal_info_fail)
    finally:
        if con is not None:
            con.close()
        if cursor is not None:
            cursor.close()
    if flag is False:
        return ResponseResult(flag=False, msg=ResultMessage.update_personal_info_fail)
    else:
        return ResponseResult(flag=True, msg=ResultMessage.update_personal_info_success)


"""
    根据用户id修改头像
"""


def update_personal_img(id, img):
    con = None
    cursor = None
    flag = None
    try:
        con = get_mysql_connect()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        # 根据用户id修改头像
        flag = cursor.execute("update tb_user set img=%s where id=%s", (img, id))
        if not flag:
            con.rollback()
        else:
            con.commit()
    except:
        print(traceback.format_exc())
        con.rollbcak()
        return ResponseResult(flag=False, msg=ResultMessage.update_personal_img_fail)
    finally:
        if con is not None:
            con.close()
        if cursor is not None:
            cursor.close()
    if flag:
        return ResponseResult(flag=True, msg=ResultMessage.update_personal_img_success)
    else:
        return ResponseResult(flag=False, msg=ResultMessage.update_personal_img_fail)
