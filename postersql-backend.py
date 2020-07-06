import psycopg2
import getpass

passwd=getpass.getpass("输入密码")

def connect_db():
    # TODO:用户交接数据
    if has_con_config :
        pass # 读取设置
    else:
        db_name = input("数据库名（留空将使用postgres）: ")
        if db_name == None :
            db_name = 'postgres'
        db_user = input("用户名（留空将使用postgres）:")
        if db_user == None :
            db_user = 'postgres'
        db_host = input('数据库主机（留空将使用localhost）: ')
        if db_host == None :
            db_host = 'localhost'
        db_port = input('数据库端口（留空将使用5432）: ')
        if db_port == None :
            db_port = '5432'
    
        while not_input_password :
            db_pwd = getpass.getpass("输入密码（输入后不可见）:")
            if db_pwd == None :
                print("你没有输入密码，请重试")

    conn = psycopg2.connect(database=str(db_name), user=str(db_user), password=str(db_pwd), host=str(db_host), port=str(db_port))
    cur = conn.cursor()

def init_db():
    # 初始化数据库布局
    print('本向导会指引你初始化数据库布局')
    has_db = input('您是否有已经有了一个专供本软件使用的数据库？(Y/N): ')
    while not_done:
        if has_db == 'Y':
            has_db = True
            while retry:
                db_name = input('数据库名称: ')
                cur.execute('/l')
                db_list = cur.fetchall
                db_list = db_list[0]
                if db_name not in db_list :
                    retry=input('我们尚未找到该数据库，是否重新尝试？(Y/N）: ')
                    if retry == 'Y' :
                        retry = True
                    else:
                        not_done=input('是否新建一个数据库？(Y/N) : ')
                        if not_done == 'Y':
                            not_done = True
                        else:
                            return
                        break
             cur.execute('\c '+str(db_name))
            print('现在已经切换到 '+str(db_name))
            sheet_name = input('输入表名称（留空将使用默认名 bilcs ）: ')
            if sheet == None :
                sheet_name = 'bilcs'
            cur.execute('CREATE TABLE '+sheet_name+""" { 
                video-av BIGSERIAL , 
                copyright-type int , 
                picture-add BIGSERIAL , 
                post-time-step int ,
                cite-time-step int , 
                desctrion BIGSERIAL ,
                owner-uid int , 
                view-number int ,
                favorite-number int , 
                coin-number int ,
                share-number int ,
                daily-highest-rank int ,
                like-number int
                dilike-number int
                };""")
            # TODO:创建表格
            cur.commit()
            cur.execute('\d')
            list_all = cur.fetchall()
            list_all = list_all[1]
            if sheet_name not in list_all :
                pass
                error_check_out() #TODO:错误码检查

            
        else:
            print('我们将会创建一个全新的数据库')
            while retry:
                db_name = input('请输入名称：')
                if db_name == None :
                    print('你尚未输入名称！')
                    retry = True
                    continue
            cur.execute('CREATE DATABASE '+str(db_name)+';')
            cur.commit()
            db_list = cur.fetchall
            db_list = db_list[0]
            if db_name not in db_list :
                error_check_out()# 错误码跳转
            print('成功建立数据库 '+str(db_name))
            cur.execute('\c '+str(db_name))
            print('现在已经切换到 '+str(db_name))
            

            # TODO:写入配置

        



def update_data_video_info(): # 视频数据更新
    sheet_name = input('输入表名称（留空将使用默认名 bilcs ）: ')
            
    cur.execute('CREATE TABLE '+sheet_name+""" { 
        video-av BIGSERIAL , 
        copyright-type int , 
        picture-add BIGSERIAL , 
        post-time-step int ,
        cite-time-step int , 
        desctrion BIGSERIAL ,
        owner-uid int , 
        view-number int ,
        favorite-number int , 
        coin-number int ,
        share-number int ,
        daily-highest-rank int ,
        like-number int ,
        dilike-number int ,
        collect-time-step int
        };""")
    # TODO:创建表格
    cur.commit()
    cur.execute('\d')
    list_all = cur.fetchall()
    list_all = list_all[1]
    if sheet_name not in list_all :
        pass
        error_check_out() #TODO:错误码检查

def update_data_commit_info():
    # TODO:数据库数据更新
   
    # TODO:数据查询
    pass
