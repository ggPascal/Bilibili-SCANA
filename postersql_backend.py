import psycopg2
import getpass
from error_handel import *
def table_exists(con, table_str):
    exists = False
    try:
        con.execute(
            "select exists(select relname from pg_class where relname='" + table_str + "')")
        exists = con.fetchone()[0]
        print(exists)
        con.close()
    except psycopg2.Error as e:
        print(e)
    return exists
def commit_table_create(cur, video_bv_id):
    table_name = str(video_bv_id)+'_commits'
    cur.execute('CREATE TABLE '+table_name+""" { 
        uid int,
        post-time-step int,
        like-number int,
        message BIGSERIAL, 
        has_replies BIGSERIAL, 
        root_rid BIGSERIAL, 
        is_top BIGSERIAL,
        collect-time-step int, 
        };""") # TODO: Change into commit data format
    cur.commit()
    table_exists_flag = table_exists(con=cur, table_str=str(table_name))
    if table_exists_flag == False :
        print("尚未成功创建表格")
        return False
    print(table_name+" 创建成功")
    return True

def video_info_table_create(cur, video_bv_id):
    table_name = str(video_bv_id)+'_video_info'
    cur.execute('CREATE TABLE '+table_name+""" { 
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
    cur.commit()
    table_exists_flag = table_exists(con=cur, table_str=str(table_name))
    if table_exists_flag == False :
        print("尚未成功创建表格")
        return False
    print(table_name+" 创建成功")
    return True

def commit_exit(con, rid, table_name, post_time_step):
    commit_exists = False
    try:
        cur = con.cursor()
        cur.execute(
            "select exists(select rid from "+table_name+" where uid='" + str(rid) + "')")
        uid_exists = cur.fetchone()[0]
        if uid_exists : # TODO: add a post time exists dected
            cur.execute(
            "select exists(select post_time from "+table_name+" where uid='" + str(post_time_step) + "')")
            post_time_exists = cur.fetchone()[0]
            if post_time_exists :
                commit_exit = True
        print(commit_exit)
    except psycopg2.Error as e:
        print(e)
    return commit_exists

# 检测用户是否存在于数据库中
def user_exit(cur, uid_str):
    exists = False
    try:
        cur.execute(
            "select exists(select uid from user_tablet where uid='" + str(uid_str) + "')")
        exists = cur.fetchone()[0]
        print(exists)
        cur.close()
    except psycopg2.Error as e:
        print(e)
    return exists

# 用于检测表格是否存在
# Orinal code from https://www.itranslater.com/qa/details/2583162923480777728



def connect_db(has_con_config):
    # TODO:用户交接数据
    if has_con_config:
        pass  # 读取设置
    else:
        db_name = input("数据库名（留空将使用postgres）: ")
        if db_name == '':
            db_name = 'postgres'
        db_user = input("用户名（留空将使用postgres）:")
        if db_user == '':
            db_user = 'postgres'
        db_host = input('数据库主机（留空将使用localhost）: ')
        if db_host == '':
            db_host = 'localhost'
        db_port = input('数据库端口（留空将使用5432）: ')
        if db_port == '':
            db_port = '5432'
        not_input_password = True
        while not_input_password:
            db_pwd = getpass.getpass("输入密码（输入后不可见）:")
            if db_pwd == None:
                print("你没有输入密码，请重试")
                not_input_password = True
            else:
                not_input_password = False

    conn = psycopg2.connect(database=str(db_name), user=str(
        db_user), password=str(db_pwd), host=str(db_host), port=str(db_port))
    cur = conn.cursor()
    return cur 


def init_db(cur):
    # 初始化数据库布局
    print('本向导会指引你初始化数据库布局')
    has_db = input('您是否有已经有了一个专供本软件使用的数据库？(Y/N): ')
    not_done = True
    while not_done:
        if has_db == 'Y':
            has_db = True
            retry = True
            while retry:
                db_name = input('数据库名称: ')
                cur.execute('/l')
                db_list = cur.fetchall
                db_list = db_list[0]
                if db_name not in db_list:
                    retry = input('我们尚未找到该数据库，是否重新尝试？(Y/N）: ')
                    if retry == 'Y':
                        retry = True
                    else:
                        not_done = input('是否新建一个数据库？(Y/N) : ')
                        if not_done == 'Y':
                            not_done = True
                        else:
                            return
                        break
            cur.execute('\c '+str(db_name))
            print('现在已经切换到 '+str(db_name))
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
                pass
                # error_check_out()
                # 错误码跳转
            print('成功建立数据库 '+str(db_name))
            cur.execute('\c '+str(db_name))
            print('现在已经切换到 '+str(db_name))
            

            # TODO:写入配置

        



def update_data_video_info(cur,video_id): # 视频数据更新
    table_name = str(video_id)+'_info' 
    if table_exists(cur,table_name) == False : 
        cur.execute('CREATE TABLE '+table_name+""" { 
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
        exit_flag=table_exists(cur,str(table_name))# 查询表格是否存在
        if exit_flag :
            pass
            # error_check_out() 
            #TODO:错误码检查

def update_data_commit_info(commit_dire):
    # TODO:数据库数据更新
   for uid in commit_dire.keys() :
       current_data = commit_dire[uid]
       
    # TODO:数据查询
    # pass
