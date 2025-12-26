from myutils.MySQLUtil import get_conn,close_conn

# 假设账号密码
username = "testUser"
password = "123456"

conn = get_conn()
cur = conn.cursor()
"""
向数据库插入数据
增删改 操作会对 db 产生影响，需要【事务管理】，决定是否执行操作、取消操作
    1. 操作成功，提交事务 try
    2. 操作失败，回滚事务 except
"""
try:
    # 向数据库插入数据
    sql = "insert into `user` values(null, %s, %s)"
    cur.execute(sql, [username, password])
    # 执行成功，提交事务
    conn.commit()
except Exception as e:
    print(e)
    # 执行失败，回滚事务
    conn.rollback()
finally:
    close_conn(cur, conn)





