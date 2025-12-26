"""
用户数据库操作（只做数据库操作，不做逻辑处理）
"""
from myutils.MySQLUtil import get_conn, close_conn

# login
def login(username):
    conn = get_conn()
    cur = conn.cursor()
    sql = "SELECT * FROM `user` WHERE `username` = %s;"
    cur.execute(sql, [username])
    result = cur.fetchall()
    close_conn(cur, conn)
    return result





if __name__ == '__main__':
    print(login('admin'))