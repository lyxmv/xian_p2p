import logging
from logging import handlers
import os
import app
import time

import pymysql

BASE_URL="http://user-p2p-test.itheima.net"
BASE_DIR=os.path.dirname(os.path.abspath(__file__)) #获取当前app.py的绝对路径
DB_URL = '121.43.169.97'
DB_USERNAME = 'root'
DB_PASSWORD = 'Itcast_p2p_20191228'
DB_MEMBER = 'czbk_member'
DB_FINANCE = 'czbk_finance'
# 初始化日志配置
def init_log_config():
    # 1.初始化日志对象
    logger = logging.getLogger()
    # 2.设置日志级别
    logger.setLevel(logging.INFO)
    # 3.创建控制台日志处理器和文件日志处理器
    sh = logging.StreamHandler()
    logfile = BASE_DIR + os.sep +"log" + os.sep + "p2p.log"
    #logfile =BASE_DIE+ "log"+os.sep+"log{}.log".format("%Y%m%D %H%M%S")
    fh=logging.handlers.TimedRotatingFileHandler(logfile,when='M',interval=5,backupCount=5,encoding='UTF-8')
    # 4.设置日志格式，创建格式化器
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    fotmatter=logging.Formatter(fmt)
    # 5.将格式化器设置到日志器中
    sh.setFormatter(fotmatter)
    fh.setFormatter(fotmatter)
    # 6.将日志处理器添加到日志对象
    logger.addHandler(sh)
    logger.addHandler(fh)

    class DButils:
        @classmethod
        def get_conn(cls, db_name, ):
            conn = pymysql.connect(app.DB_URL, app.DB_USERNAME, app.DB_PASSWORD, db_name, autocommit=True)
            return conn

        @classmethod
        def close(cls, cursor=None, conn=None):
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        @classmethod
        def delete(cls, db_name, sql):
            try:
                conn = cls.get_conn(db_name)
                cursor = conn.cursor()
                cursor.execute(sql)
            except Exception as e:
                conn.rollback()
            finally:
                cls.close(cursor, conn)
