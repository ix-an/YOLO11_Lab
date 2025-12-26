from myutils.MySQLUtil import get_conn,close_conn

# 假设账号密码
users = [
    ['xiaoming', '123456'],
    ['xiaohong', '123456'],
]


conn = get_conn()
cur = conn.cursor()

try:
    # 向数据库插入数据
    sql = "insert into `user` values(null, %s, %s)"
    # 批量插入
    cur.executemany(sql, users)
    # 执行成功，提交事务
    conn.commit()
except Exception as e:
    print(e)
    # 执行失败，回滚事务
    conn.rollback()
finally:
    close_conn(cur, conn)





