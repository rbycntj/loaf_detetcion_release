from dbutils.pooled_db import PooledDB
from utils.utils import Properties
import pymysql
import threading
import os
import traceback

pool = None
lock = threading.Lock()
config_path = os.path.join(os.getcwd(), "database", "config", "mysql.properties")


# 双重检验法保证一个pool
def init_mysql_pool():
    global pool
    if pool is None:
        lock.acquire(blocking=True, timeout=-1)
        if pool is None:
            # 读取properties文件
            try:
                config = Properties(config_path).getProperties()
                # 创建连接池
                pool = PooledDB(creator=pymysql,
                                maxconnections=0,  # 连接池允许的最大连接数，0和None表示不限制连接数
                                mincached=10,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                                maxcached=10,  # 链接池中最多闲置的链接，0和None不限制
                                maxusage=1,  # 一个链接最多被重复使用的次数，None表示无限制
                                blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                                host=config['host'],  # 此处必须是是127.0.0.1
                                port=int(config['port']),
                                user=config['username'],
                                passwd=config['password'],
                                db=config['db'],
                                use_unicode=True,
                                charset='utf8mb4')
            except Exception as e:
                print(traceback.format_exc())
            finally:
                lock.release()
    return pool


def get_mysql_connect():
    return pool.connection()
