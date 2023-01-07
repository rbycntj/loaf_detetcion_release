from database.mysql_connection import *
from database.redis_connection import *
from modules.result.response_result import *
from modules.study_record import *
import datetime
import traceback

"""
    开始计时
"""


def start_record(id):
    # 获取当前时间
    # 要小数点前面的部分
    dt = str(datetime.datetime.today()).split(".")[0]
    d = str(datetime.date.today())

    # 新增记录
    con = None
    cursor = None
    flag = None
    record_id = None
    try:
        # 获取数据库连接
        con = get_mysql_connect()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        # 插入record
        con.begin()  # 必须要加begin，否则获取不到最新的id
        flag = cursor.execute(
            "insert into loaf_detection.tb_study_record(user_id,start_time,cur_date) values(%s,%s,%s)",
            (str(id), dt, d))
        # 获取新插入的id，保证线程安全
        cursor.execute("select last_insert_id() as last_id")
        record_id = cursor.fetchone()['last_id']
        # 提交事务
        con.commit()
    except:
        print(traceback.format_exc())
        con.rollback()
        return ResponseResult(flag=False, msg=ResultMessage.add_record_fail)
    if flag:
        return ResponseResult(flag=True, msg=ResultMessage.add_record_success, obj=record_id)
    else:
        return ResponseResult(flag=False, msg=ResultMessage.add_record_fail)


"""
    结束计时
"""


def end_record(id, record_id, valid, score):
    # 获取结束时间
    end_time = datetime.datetime.today()

    con = None
    cursor = None
    redis_con = None
    try:
        con = get_mysql_connect()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        redis_con = get_redis_connection()
        con.begin()
        # 查询开始时间并计算学习时长
        cursor.execute("select start_time from tb_study_record where id=%s", (record_id))
        start_time = cursor.fetchone()['start_time']
        # 计算时间差
        duration_time = str((end_time - start_time).seconds)
        # 修改字段
        end_time = str(end_time).split(".")[0]
        flag = cursor.execute("update tb_study_record set end_time=%s,duration_time=%s,valid=%s,score=%s where id=%s",
                              (end_time, duration_time, valid, score, record_id))

        if valid == 1:
            # 修改redis中数据
            redis_con.zincrby("time_rank", int(duration_time), id)
        con.commit()
    except:
        print(traceback.format_exc())
        con.rollback()
        return ResponseResult(flag=False, msg=ResultMessage.update_record_fail)
    finally:
        if con is not None:
            con.close()
        if cursor is not None:
            cursor.close()
        if redis_con is not None:
            redis_con.close()
    if flag:
        return ResponseResult(flag=True, msg=ResultMessage.update_record_success)
    else:
        return ResponseResult(flag=False, msg=ResultMessage.update_record_fail)


"""
    根据用户id查询近十天历史学习记录
"""


def get_study_record(id):
    con = None
    cursor = None
    obj = None
    # 今天日期
    cur = datetime.date.today()
    try:
        con = get_mysql_connect()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        con.begin()
        # 十天前日期
        cur_before = cur + datetime.timedelta(days=-9)
        cursor.execute(
            "select sum(duration_time) as total_time,cur_date "
            "from tb_study_record "
            "where user_id=%s and cur_date<=%s and cur_date>=%s "
            "group by cur_date "
            "order by cur_date asc",
            (id, str(cur), str(cur_before)))
        records_info = cursor.fetchall()
        record_list = []
        for info in records_info:
            study_record = StudyRecord(total_time=info['total_time'], cur_date=info['cur_date'])
            record_list.append(study_record)
        obj = record_list
    except:
        print(traceback.format_exc())
        con.rollback()
        return ResponseResult(flag=False, msg=ResultMessage.get_study_record_fail)
    finally:
        if con is not None:
            con.close()
        if cursor is not None:
            cursor.close()
    return ResponseResult(flag=True, msg=ResultMessage.get_study_record_success, obj=obj)
