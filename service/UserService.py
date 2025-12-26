"""
用户服务层：获取数据库操作结果，做逻辑处理
"""

from dao import UserDao as ud


# login
def login(username, password):
    # 得到数据库操作结果 -> 用户名查询结果
    result = ud.login(username)
    # 判断账号
    if not result:
        return {
            "status": 500,
            "msg": "账号不存在 🍡",
        }
    # 判断密码
    if result[0][2] != password:
        return {
            "status": 500,
            "msg": "密码错误 🍡",
        }
    # 登录成功
    return {
        "status": 200,
        "msg": "登录成功！🍙",
    }



if __name__ == '__main__':
    print(login('admin', '123456'))