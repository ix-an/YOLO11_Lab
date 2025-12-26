"""
操作数据库的工具，提供 2个方法：
    1. 获取数据库连接
    2. 关闭连接
"""
import pymysql

# ----------------------------------------
# 获取 db连接
# ----------------------------------------
def get_conn():
    return pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        db='yolo11_lab',
        charset='utf8mb4'
    )

# ----------------------------------------
# 关闭 db连接
# ----------------------------------------
def close_conn(cur, conn):
    # 关闭游标对象：实际上操作db的对象，如执行sql语句
    cur.close()
    # 关闭连接对象
    conn.close()


if __name__ == '__main__':
    print(get_conn())  # 测试是否成功获取连接
