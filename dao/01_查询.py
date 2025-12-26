"""
无参数查询：不用在定义sql语句时，使用 %s 进行参数占位
e.g. 查询全部数据： -- select * from 表名
     查询username为admin的数据： -- select * from 表名 where `username` = %s;
     %s 表示一个变量，执行sql时赋值
步骤固定：
    1）获取连接对象
    2）获取游标对象
    3）定义 sql语句
    4）执行 sql语句
    5）获取查询结果  -> 元组，元素是数据，每个数据也是一个元组。内容顺序和表的类名一致。
    6）关闭连接
    7）返回查询结果【service中处理，dao中不处理】
"""
from myutils.MySQLUtil import get_conn, close_conn

# ----------------------------------------
# 无参数查询（没有 %s）
# ----------------------------------------
def query_all():
    conn = get_conn()  # 获取连接对象
    cur = conn.cursor()  # 获取游标对象
    try:
        # 定义 sql语句
        sql = "SELECT * FROM `user`;"
        cur.execute(sql)  # 执行 sql语句
        result = cur.fetchall()  # 获取查询结果
        return result
    except Exception as e:
        print(e)
        return None
    finally:
        close_conn(cur, conn)  # 关闭连接


# ----------------------------------------
# 参数查询（有 %s）
# ----------------------------------------
def login(username, password):
    conn = get_conn()
    cur = conn.cursor()
    try:
        # %s 是变量占位符，多个变量时，需按顺序传入
        sql = "SELECT * FROM `user` WHERE `username` = %s and `password` = %s;"
        # 列表里的元素按顺序传给 %s
        cur.execute(sql, [username, password])
        result = cur.fetchall()
        return result
    except Exception as e:
        print(e)
        return None
    finally:
        close_conn(cur, conn)


if __name__ == '__main__':
    # res = query_all()
    res = login('admin', '123456')
    if not res:  # 或 if len(res) == 0
        print('用户名或密码错误')
    else:
        print('登录成功')
        print(res)