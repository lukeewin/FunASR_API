import os
import threading
import pymysql
from dbutils.pooled_db import PooledDB


class SQLHelper:
    def __init__(self):
        db_host = os.getenv('DB_HOST')
        db_port = int(os.getenv('DB_PORT'))
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')

        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=0,
            mincached=1,
            maxcached=8,
            blocking=True,
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name,
            charset='utf8mb4',
            connect_timeout=15
        )
        self.local = threading.local()

    def open(self):
        conn = self.pool.connection()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cur

    def close(self, conn, cur):
        cur.close()
        conn.close()

    def get_list(self, sql, args=None):
        """
        获取所有数据
        :param sql: SQL语句
        :param args: SQL语句的占位参数
        :return: 查询结果
        """
        conn, cur = self.open()
        cur.execute(sql, args)
        result = cur.fetchall()
        self.close(conn, cur)
        return result

    def get_one(self, sql, args=None):
        """
        获取单条数据
        :return: 查询结果
        """
        conn, cur = self.open()
        cur.execute(sql, args)
        result = cur.fetchone()
        self.close(conn, cur)
        return result

    def modify(self, sql, args=None):
        """
        修改、增加、删除操作
        :return: 受影响的行数
        """
        conn, cur = self.open()
        try:
            result = cur.execute(sql, args)
            conn.commit()
            return result
        except Exception as e:
            raise e
        finally:
            self.close(conn, cur)


    def bulk_modify(self, sql, args=None):
        """
        批量修改、增加、删除操作
        :return: 受影响的行数
        """
        conn, cur = self.open()
        try:
            result = cur.executemany(sql, args)
            conn.commit()
            return result
        except Exception as e:
            raise e
        finally:
            self.close(conn, cur)

    def create(self, sql, args=None):
        """
        增加数据
        :return: 新增数据行的ID
        """
        conn, cur = self.open()
        try:
            cur.execute(sql, args)
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            raise e
        finally:
            self.close(conn, cur)

    def __enter__(self):
        conn, cur = self.open()
        rv = getattr(self.local, 'stack', None)
        if not rv:
            self.local.stack = [(conn, cur), ]
        else:
            self.local.stack.append((conn, cur))
        return conn, cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        rv = getattr(self.local, 'stack', None)
        if not rv:
            return
        conn, cur = self.local.stack.pop()
        cur.close()
        conn.close()
