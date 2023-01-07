import redis
import threading
import traceback
import os
from redis import ConnectionPool
from utils.utils import Properties

pool = None
lock = threading.Lock()
config_path = os.path.join(os.getcwd(), "database", "config", "redis.properties")

# 双重检验法保证一个pool
def init_redis_pool():
    # 读取参数
    config = Properties(config_path).getProperties()
    global host, port, username, password
    host = config['host']
    port = config['port']
    username = config['username']
    password = config['password']

    # 创建连接池
    global pool
    if pool is None:
        lock.acquire(blocking=True, timeout=-1)
        if pool is None:
            try:
                pool = ConnectionPool(password=password, host=host, port=port, decode_responses=True)
            except:
                print(traceback.format_exc())
            finally:
                lock.release()
    return pool


def get_redis_connection():
    return redis.Redis(connection_pool=pool)
