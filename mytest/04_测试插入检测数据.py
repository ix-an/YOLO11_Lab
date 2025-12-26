from myutils.MySQLUtil import get_conn,close_conn


conn = get_conn()
cur = conn.cursor()

try:
    # 向数据库插入数据
    sql = "insert into `records` values(null, %s, %s, %s, %s, %s, now())"
    cur.execute(sql, ["1", "1", 1.0, "1", "1"])
    # 执行成功，提交事务
    conn.commit()
except Exception as e:
    print(e)
    # 执行失败，回滚事务
    conn.rollback()
finally:
    close_conn(cur, conn)





