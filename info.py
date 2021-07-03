class User:
    uid = ""
    pwd = ""
    email = ""
    province = ""
    city = ""
    def __init__(self, uid, pwd, email, province, city):
        self.uid = uid
        self.pwd = pwd
        self.email = email
        self.province = province
        self.city = city

daka_time="08:25"

pd_id = "125686"     #用户中心页可以查询到pd信息
pd_key = "jxq9WUgEtEPaBrz2ZQkbhatlZyO2jHvO"
app_id = "325686"     #开发者分成用的账号，在开发者中心可以查询到
app_key = "DdHdBvwwApGWDThLGNJzdhZr2gJPL31J"

MAIL_USER = "18766180878@163.com"        # 用于发送通知的邮箱
MAIL_PWD = ""    # 该邮箱的授权码
# 单用户
UID = "your-id"         # 学号
PWD = "your-password"   # 密码
MAIL_TO = "your-email"  # 接受通知的邮箱
# 多用户
users = list()
#users.append(User("id", "password", "email", "province", "city"))
users.append(User("71609048", "Y3MjEp74!@i7hHG", "18766180878@163.com", "山东省", "济南市"))

for user in users:
    print(user.uid)
