import psycopg2 as psq # 连接PostgreSQL所需的连接器 
import getpass # 隐藏密码用的函数

def connect-server() : # TODO: 完成连接函数
    print("警告！")
    print("除非你启用本工具的自动连接配置，否则本工具不记录你的登录信息，但是不代表你所处的连接是安全的！")
    print("如果你的数据库遭到攻击，本工具均不负责！")
    a = input("同意？（Y/N）>")
    if a = "Y" or a = "y" :
        while error_flag :
            ip_add = input("远程服务器IP（没有请打NULL）:")
            port = str(input("请输入端口号（默认为5432）："))
            if port = None :
                port = "5432"
            while err_user_name_none :
                err_user_name_none = False
                user_name = str(input("用户名："))
                if user_name = None :
                    print("请输入用户名！")
                    err_user_name_none = True
            while err_passw_none :
                err_passw_none = False
                password = getpass.getpass("密码（已被隐藏）：")
                if password = None :
                    print("密码为空！")
                    err_passw_none = True
            if ip_add = "NULL" :
                ip_add = "127.0.0.1"
            try:
                opdatabase = psycopg2.connect(database="testdb", user="postgres", password="pass123", host="127.0.0.1", port="5432")
            except :
                print("连接错误，请检查相关配置") # TODO: 完善异常引导处理程序

def insert_data() #TODO：完成


        