from database.mysql_connection import *
from modules.result.response_result import *
from modules.friend import Friend
from modules.user import User
import traceback

"""
    根据用户id查找好友
"""


def query_all_friend(id: int):
    con = None
    cursor = None
    obj = None
    try:
        # 获取连接
        con = get_mysql_connect()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        friend_list = []
        # 查询 relation=2 relation=2说明已经成为好友
        cursor.execute(
            "select distinct * "
            "from tb_user "
            "where "
            "id in(select friend_id from tb_friend where user_id=%s and relation=2) or "
            "id in(select user_id from tb_friend where friend_id=%s and relation=2)",
            (id, id))
        friend_msg = cursor.fetchall()
        for msg in friend_msg:
            user = User(id=msg['id'], username=msg['username'], password=msg['password'], telephone=msg['telephone'],
                        gender=msg['gender'], img=msg['img'])
            friend_list.append(user)

        obj = friend_list
    except:
        print(traceback.format_exc())
        return ResponseResult(flag=False, msg=ResultMessage.query_friend_fail)
    finally:
        if con is not None:
            con.close()
        if cursor is not None:
            cursor.close()
    return ResponseResult(flag=True, msg=ResultMessage.query_friend_success, obj=obj)


"""
    通过好友申请
"""


def pass_friend(uid, fid):
    con = None
    cursor = None
    flag = None
    try:
        # 获取连接
        con = get_mysql_connect()
        cursor = con.cursor()
        # 更新relation值
        flag = cursor.execute(
            "update tb_friend set relation=2 "
            "where "
            "(user_id=%s and friend_id=%s and relation=1) "
            "or(friend_id=%s and user_id=%s and relation=1)",
            (fid, uid, fid, uid))
        if flag:
            con.commit()
        else:
            con.rollback()
    except:
        print(traceback.format_exc())
        con.rollback()
        return ResponseResult(flag=False, msg=ResultMessage.friend_pass_fail)
    finally:
        if con is not None:
            con.close()
        if cursor is not None:
            cursor.close()
    if flag:
        return ResponseResult(flag=True, msg=ResultMessage.friend_pass_success)
    else:
        return ResponseResult(flag=False, msg=ResultMessage.friend_pass_fail)


"""
    拒绝好友申请
"""


def not_pass_friend(uid, fid):
    con = None
    cursor = None
    flag = None
    try:
        # 获取连接
        con = get_mysql_connect()
        cursor = con.cursor()
        # 更新pass值
        flag = cursor.execute("update tb_friend set relation=0 where user_id=%s and friend_id=%s", (fid, uid))
        if flag:
            con.commit()
        else:
            con.rollback()
    except:
        print(traceback.format_exc())
        con.rollback()
        return ResponseResult(flag=False, msg=ResultMessage.friend_not_pass_fail)
    finally:
        if con is not None:
            con.close()
        if cursor is not None:
            cursor.close()
    if flag:
        return ResponseResult(flag=True, msg=ResultMessage.friend_not_pass_success)
    else:
        return ResponseResult(flag=False, msg=ResultMessage.friend_not_pass_fail)


"""
    发送添加好友信息
"""


def send_add_friend_msg(uid, telephone):
    con = None
    cursor = None
    flag = None
    try:
        # 获取连接
        con = get_mysql_connect()
        cursor = con.cursor()
        # 通过手机号查询用户id
        cursor.execute("select id from tb_user where telephone = %s", (telephone))
        fid = cursor.fetchone()
        if fid is None:
            # 该用户不存在
            return ResponseResult(flag=False, msg=ResultMessage.friend_not_exist)
        # 查看是否是自己
        if str(fid[0]) == str(uid):
            return ResponseResult(flag=False, msg=ResultMessage.add_not_yourself)
        # 查看是否已经是好友了
        cursor.execute(
            "select id from tb_friend where (user_id=%s and friend_id=%s and relation=2) or (friend_id=%s and user_id=%s and relation=2)",
            (uid, fid, uid, fid))
        id = cursor.fetchone()
        if id is not None:
            return ResponseResult(flag=False, msg=ResultMessage.already_friend)
        # 查找是否已经申请过且对方没有处理
        cursor.execute("select id from tb_friend where user_id=%s and friend_id=%s and relation=%s", (uid, fid, 1))
        id = cursor.fetchone()
        if id is not None:
            return ResponseResult(flag=False, msg=ResultMessage.already_send_add_friend)
        # 添加好友列表
        flag = cursor.execute("insert into tb_friend(user_id,friend_id,relation) values(%s,%s,%s)", (uid, fid, 1))
        if flag:
            con.commit()
        else:
            con.rollback()
    except:
        print(traceback.format_exc())
        con.rollback()
        return ResponseResult(flag=False, msg=ResultMessage.send_add_friend_msg_fail)
    finally:
        if con is not None:
            con.close()
        if cursor is not None:
            cursor.close()
    if flag:
        return ResponseResult(flag=True, msg=ResultMessage.send_add_friend_msg_success)
    else:
        return ResponseResult(flag=False, msg=ResultMessage.send_add_friend_msg_fail)


"""
    展示添加自己的 好友信息 列表
"""


def query_add_friends_msg(uid):
    con = None
    cursor = None
    user_msg_list = []
    try:
        # 获取连接
        con = get_mysql_connect()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        # 通过uid查询添加好友信息列表
        cursor.execute(
            "select * from tb_user where id in(select user_id from tb_friend where friend_id=%s and relation=1)",
            (uid))
        msg_list = cursor.fetchall()
        for msg in msg_list:
            user = User(id=msg['id'], username=msg['username'], telephone=msg['telephone'], gender=msg['gender'],
                        img=msg['img'])
            user_msg_list.append(user)

    except:
        print(traceback.format_exc())
        con.rollback()
        return ResponseResult(flag=False, msg=ResultMessage.query_add_friends_msg_fail)
    finally:
        if con is not None:
            con.close()
        if cursor is not None:
            cursor.close()
    return ResponseResult(flag=True, msg=ResultMessage.query_add_friends_msg_success, obj=user_msg_list)


"""
    删除好友
"""


def delete_friend(uid, fid):
    con = None
    cursor = None
    flag = None
    try:
        con = get_mysql_connect()
        cursor = con.cursor()
        con.begin()
        # 删除
        flag = cursor.execute(
            "delete from tb_friend where (user_id=%s and friend_id=%s) or (user_id=%s and friend_id=%s)",
            (uid, fid, fid, uid))
        con.commit()
    except:
        print(traceback.format_exc())
        return ResponseResult(flag=False, msg=ResultMessage.delete_friend_fail)
    finally:
        if con is not None:
            con.close()
        if cursor is not None:
            cursor.close()
    if flag:
        return ResponseResult(flag=True, msg=ResultMessage.delete_friend_success)
    else:
        return ResponseResult(flag=False, msg=ResultMessage.delete_friend_fail)
