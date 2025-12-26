from myutils.MySQLUtil import get_conn,close_conn


# 保存图片检测结果
def save_result(data):
    conn = get_conn()
    cur = conn.cursor()
    # 向数据库中插入数据
    try:
        sql = "insert into `records` values(null, %s, %s, %s, %s, %s, now())"
        cur.execute(sql, data)
        conn.commit()  # 执行成功就提交事务
        return True
    except Exception as e:
        print(e)
        conn.rollback()  # 执行失败就回滚事务
        return False
    finally:
        close_conn(cur, conn)


# 查询图片检测结果（分页）
def query_records(start, size, username):
    conn = get_conn()
    cur = conn.cursor()
    sql = "select * from `records` where `username`=%s limit %s,%s "
    cur.execute(sql, (username, start, size))
    records = cur.fetchall()
    close_conn(cur, conn)
    return records


# 检测记录总数  -- 分页组件根据total/size计算出来一共多少页
def query_total(username):
    conn = get_conn()
    cur = conn.cursor()
    # count(*) 统计数据多少条
    sql = "select count(*) from `records` where `username`=%s"
    cur.execute(sql, [username])
    counts = cur.fetchall()
    close_conn(cur, conn)
    return counts[0][0]




if __name__ == '__main__':
    result = query_records(0, 5, 'admin')
    for i in result:
        print(i)