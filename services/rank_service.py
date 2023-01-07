from database.mysql_connection import get_mysql_connect
from database.redis_connection import get_redis_connection
from modules.result.response_result import *
from services import personal_info_service
from modules.rank_info import *
import traceback
import pymysql

"""
    将mysql时间数据载入到redis中
"""


def load_mysql_data_to_redis():
    mysql_con = None
    mysql_cursor = None
    redis_con = None

    try:
        # 获取mysql数据库连接
        mysql_con = get_mysql_connect()
        mysql_cursor = mysql_con.cursor(cursor=pymysql.cursors.DictCursor)
        # 获取redis连接
        redis_con = get_redis_connection()
        redis_con.flushall()
        # 查询duration_time
        mysql_cursor.execute("select sum(duration_time) as total_time,user_id from tb_study_record where valid=1 group by user_id ")
        fetch_infos = mysql_cursor.fetchall()
        # 转换结果
        for info in fetch_infos:
            data_dict = dict()
            data_dict[info['user_id']] = info['total_time']
            # 将数据载入redis
            redis_con.zadd("time_rank", data_dict)
    except:
        print(traceback.format_exc())
        return False
    finally:
        if mysql_con is not None:
            mysql_con.close()
        if mysql_cursor is not None:
            mysql_cursor.close()
        if redis_con is not None:
            redis_con.close()
    return True


"""
    根据用户id获取排名和总学习时长
"""


def get_rank(id):
    con = None
    rank = None
    try:
        # 获取redis连接
        con = get_redis_connection()
        # 获取排名
        rank = con.zrevrank("time_rank", id)
        score = con.zscore("time_rank",id)
        if rank is not None:
            rank = rank + 1
        else:
            rank = 99999
            score = 0
    except:
        print(traceback.format_exc())
        return ResponseResult(flag=False, msg=ResultMessage.get_rank_fail)
    finally:
        if con is not None:
            con.close()
    print(1)
    return ResponseResult(flag=True, msg=ResultMessage.get_rank_success, obj=[rank,score])


"""
    获取前XX名的排名信息
"""


def get_all_rank(num):
    mysql_con = None
    mysql_cursor = None
    redis_con = None
    rank_list = []

    try:
        # 获取mysql数据库连接
        mysql_con = get_mysql_connect()
        mysql_cursor = mysql_con.cursor(cursor=pymysql.cursors.DictCursor)
        # 获取redis连接
        redis_con = get_redis_connection()
        # 获取前XX名的排名
        tops = redis_con.zrevrange("time_rank", 0, num, withscores=True)
        # 获取用户信息
        for index, top in enumerate(tops):
            rr = personal_info_service.query_personal_info(int(top[0]))
            if rr.flag == False:
                return ResponseResult(flag=False, msg=ResultMessage.get_rank_fail)
            # 获取用户
            user = rr.obj
            # 封装
            rank_info = RankInfo(rank=index + 1, total_time=int(top[1]), user=user)
            # 加入list
            rank_list.append(rank_info)
    except:
        print(traceback.format_exc())
        return ResponseResult(flag=False, msg=ResultMessage.get_rank_fail)
    finally:
        if mysql_con is not None:
            mysql_con.close()
        if mysql_cursor is not None:
            mysql_cursor.close()
        if redis_con is not None:
            redis_con.close()
    print(2)
    return ResponseResult(flag=True, msg=ResultMessage.get_rank_success, obj=rank_list)


"""
    根据用户id查看学习圈排名（即自己和好友的排名）
"""


def get_self_and_friends_rank(id):
    mysql_con = None
    mysql_cursor = None
    redis_con = None
    obj = None
    try:
        # 获取mysql数据库连接
        mysql_con = get_mysql_connect()
        mysql_cursor = mysql_con.cursor(cursor=pymysql.cursors.DictCursor)
        # 获取redis连接
        redis_con = get_redis_connection()
        # 根据id获取好友
        mysql_cursor.execute(
            "select distinct * "
            "from tb_user "
            "where "
            "id in(select friend_id from tb_friend where user_id=%s and relation=2) or "
            "id in(select user_id from tb_friend where friend_id=%s and relation=2)",
            (id, id))
        friend_msg = mysql_cursor.fetchall()
        friend_list = []
        for msg in friend_msg:
            user = User(id=msg['id'], username=msg['username'], telephone=msg['telephone'],
                        gender=msg['gender'], img=msg['img'])
            friend_list.append(user)
        # 获取排名信息
        rank_list = []
        for friend in friend_list:
            rank = redis_con.zrevrank("time_rank", friend.id)
            score = redis_con.zscore("time_rank", friend.id)
            if rank is not None:
                rank = rank + 1
            rank_info = RankInfo(rank=rank, total_time=round(score, 1), user=friend)
            rank_list.append(rank_info)
        # 获取自己的信息与排名
        mysql_cursor.execute("select * from tb_user where id=%s", (id))
        self_info = mysql_cursor.fetchone()
        self_user = User(id=id, username=self_info['username'], telephone=self_info['telephone'],
                         gender=self_info['gender'], img=self_info['img'])
        rank = redis_con.zrevrank("time_rank", id)
        score = redis_con.zscore("time_rank", id)
        if rank is not None:
            rank = rank + 1
            rank_info = RankInfo(rank=rank, total_time=round(score, 1), user=self_user)
            rank_list.append(rank_info)
        obj = rank_list
    except:
        print(traceback.format_exc())
        return ResponseResult(flag=False, msg=ResultMessage.get_rank_fail)
    finally:
        if mysql_con is not None:
            mysql_con.close()
        if mysql_cursor is not None:
            mysql_cursor.close()
        if redis_con is not None:
            redis_con.close()
    print(3)
    return ResponseResult(flag=True, msg=ResultMessage.get_rank_success, obj=obj)
