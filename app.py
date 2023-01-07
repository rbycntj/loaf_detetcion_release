from flask import Flask
from database.mysql_connection import init_mysql_pool
from database.redis_connection import init_redis_pool
from services.rank_service import load_mysql_data_to_redis
from flask_cors import *

# 初始化
app = Flask(__name__)
# 解决跨域请求资源被拦截问题
CORS(app, supports_credentials=True, resources=r"/*")
# 初始化数据库连接池
init_mysql_pool()
init_redis_pool()
# 装载mysql数据进入redis ==> 利用redis实现排行榜业务
if not load_mysql_data_to_redis():
    # 装载失败
    exit(-1)

# 导入蓝图
from routes.user.init import user_blueprint
from routes.personal_info.init import personal_info_blueprint
from routes.friend.init import friend_blueprint
from routes.record.init import record_blueprint
from routes.rank.init import rank_blueprint

# 注册蓝图
app.register_blueprint(user_blueprint)
app.register_blueprint(personal_info_blueprint)
app.register_blueprint(friend_blueprint)
app.register_blueprint(record_blueprint)
app.register_blueprint(rank_blueprint)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
