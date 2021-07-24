
class User:
    uid = ""
    pwd = ""
    email1 = ""
    email2 = ""
    def __init__(self, uid, pwd, email1, email2):
        self.uid = uid
        self.pwd = pwd
        self.email1 = email1
        self.email2 = email2

daka_time=["07:31","08:32","09:34","10:33","11:32","12:01","13:34","21:31","23:31",
           "14:30","15:32","16:30","17:31","18:31","19:31","20:31","22:31","07:50",
           "08:50","09:50","10:50","11:10","11:50","12:30","13:50","21:50","23:50",
           "14:50","15:52","16:50","17:51","18:51","19:51","20:51","22:51","23:20"]

pd_id = "125686"
pd_key = "jxq9WUgEtEPaBrz2ZQkbhatlZyO2jHvO"
app_id = "325686"
app_key = "DdHdBvwwApGWDThLGNJzdhZr2gJPL31J"
#TWILIO_ACCOUNT_SID = 'AC567327894d0008851a23c0e475b33531'
#TWILIO_AUTH_TOKEN = '4cd5cfb5e37b723f1d878ac1a7b07927'

MAIL_USER = "18766180878@163.com"
MAIL_PWD = "ULGYOBHSNIZVHSOQ" 

UID = "your-id"         
PWD = "your-password"
MAIL_TO = "your-email"

users = list()
#users.append(User("id", "password", "email", "province", "city"))
users.append(User("71600087", "tianTIAN0629", "17860568399@163.com", "18766180878@163.com"))
users.append(User("71609048", "Y3MjEp74!@i7hHG", "17860568399@163.com", "18766180878@163.com"))

for user in users:
    print(user.uid)
