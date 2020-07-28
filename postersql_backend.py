import psycopg2
import getpass
from error_handel import *


def table_exists(con, table_name):
    exists = False
    try:
        con.execute(
            "select exists(select relname from pg_class where relname='" + table_name + "');")
        exists = con.fetchone()[0]
        print(exists)
        con.close()
    except psycopg2.Error as e:
        print(e)
    return exists

def user_table_create(cur):
    table_name = 'user_info'
    cur.execute('CREATE TABLE '+table_name+""" {
        user-name text,
        sign text,
        avatar_image_address text,
        sex text,
        user-level int,
        has-nameplate text,
        nameplate-kind text,
        nameplate-name text,
        nameplate-image text,
        nameplate-image-small text,
        nameplate-level text,
        nameplate-condition text,
        has-vip text,
        vip-type text,
        vip-due-timestep text,
        fans-detail text,
        fans-level text,
        offical-type int,
        offical-desctrion text,
        collect-time-step numeric
    }""")
    cur.commit()
    table_exists_flag = table_exists(con=cur, table_name=str(table_name))
    if table_exists_flag == False:
        print("尚未成功创建表格")
        return False
    print(table_name+" 创建成功")
    return True
def commit_table_create(cur, video_bv_id):
    table_name = str(video_bv_id)+'_commits'
    cur.execute('CREATE TABLE '+table_name+""" { 
        uid int,
        post-time-step int,
        like-number int,
        message text, 
        has_replies text, 
        root_rid text, 
        is_top text,
        collect-time-step numeric
        };""")  # TODO: Change into commit data format
    cur.commit()
    table_exists_flag = table_exists(con=cur, table_name=str(table_name))
    if table_exists_flag == False:
        print("尚未成功创建表格")
        return False
    print(table_name+" 创建成功")
    return True


def video_info_table_create(cur, video_bv_id):
    table_name = str(video_bv_id)+'_video_info'
    cur.execute('CREATE TABLE '+table_name+""" { 
        rid int,
        video-av text , 
        copyright-type int , 
        picture-add text , 
        post-time-step int ,
        cite-time-step int , 
        desctrion text ,
        owner-uid int , 
        view-number int ,
        favorite-number int , 
        coin-number int ,
        share-number int ,
        daily-highest-rank int ,
        like-number int ,
        dislike-number int ,
        collect-time-step numeric
        };""")
    cur.commit()
    table_exists_flag = table_exists(con=cur, table_name=str(table_name))
    if table_exists_flag == False:
        print("尚未成功创建表格")
        return False
    print(table_name+" 创建成功")
    return True


def video_info_exit(cur, video_oid, table_name):
    video_info_exit = False
    try:
        cur.execute("SELECT video-oid from "+table_name +
                    " where video-oid = "+str(video_oid)+");")
        video_info_exit_flag = cur.fetchone()[0]
        if video_info_exit_flag:
            video_info_exit = True
        print(video_info_exit)
    except psycopg2.Error as e:
        print(e)
    return video_info_exit


def commit_exit(con, rid, table_name, post_time_step):
    commit_exists = False
    try:
        cur = con.cursor()
        cur.execute(
            "select exists(select rid from "+table_name+" where rid='" + str(rid) + "')")
        rid_exists = cur.fetchone()[0]
        if rid_exists:  # TODO: add a post time exists dected
            cur.execute(
                "select exists(select post_time from "+table_name+" where post_time_step='" + str(post_time_step) + "');")
            post_time_exists = cur.fetchone()[0]
            if post_time_exists:
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


def update_video_info(cur, video_bv_id, video_info_dire, overwrite_flag):
    table_name = str(video_bv_id)+'_video_info'
    if table_exists(con=cur, table_name=table_name) == False:
        is_create = video_info_table_create(cur, video_bv_id=video_bv_id)
        if is_create == False:
            print("操作失败，正在退出当前函数")
            return False

    if commit_exit(con=cur, rid=rid, table_name=table_name, post_time_step=video_info_dire['post_time_step']):
        if overwrite_flag == True:
            cur.execute('UPDATE '+table_name+' SET video-av = ' + video_info_dire['video_av'] +
                        ', copyright-type = '+video_info_dire['copyright_type'] +
                        ', picture-add = ' + video_info_dire['picture_add'] +
                        ', post-time-step = '+video_info_dire['post_time_step'] +
                        ', cite-time-step = '+video_info_dire['cite_time_step'] +
                        ', desctrion = '+video_info_dire['desctrion'] +
                        ', owner-uid = '+video_info_dire['owner_uid'] +
                        ', view-number = '+video_info_dire['view_number'] +
                        ', comment-number = '+video_info_dire['comment_number'] +
                        ', favorite-number = '+video_info_dire['favorite_number'] +
                        ', coin-number = '+video_info_dire['coin_number'] +
                        ', share-number = '+video_info_dire['share_number'] +
                        ', daily-highest-rank = '+video_info_dire['daily_highest_rank'] +
                        ', like-number = '+video_info_dire['like_number'] +
                        ', dislike-number = '+video_info_dire['dislike_number'] +
                        ', collect-time-step = '+video_info_dire['collect_time_step'] +
                        ' WHERE video-av = '+video_info_dire['video_av']+' AND post-time-step = '+video_info_dire['post_time_step']+';')
            cur.commit()
    else:
        cur.execute('INSERT INTO '+table_name +
                    ' (rid, video-av, copyright-type, post-time-step, cite-time-step, desctrion, owner-uid, view-number, favorite-number, coin-number, share-number, daily-highest-rank, like-number, dislike-number, collect-time-step' +
                    ' VALUES '+'('+rid+', '+video_info_dire['video_av']+', '+video_info_dire['copyright_type']+', '+video_info_dire['post_time_step']+', '+video_info_dire['cite_time_step']+', '+video_info_dire['desctrion']+', '+video_info_dire['owner_uid']+', '+video_info_dire['view_number']+', '+video_info_dire['coin_number']+', '+video_info_dire['share_number']+', '+video_info_dire['daily_highest_rank']+', '+video_info_dire['like_number']+', '+video_info_dire['dislike_number']+', '+video_info_dire['collect_time_step']+');')
        cur.commit()
        if commit_exit(con=cur, rid=rid, table_name=table_name, post_time_step=video_info_dire['post_time_step']) == False:
            print("我们遇到了错误，正在退出此函数")
            cur.rollback()
            return False


def update_comment_info(current_commit, cur, overwrite_flag, rid, video_bv_id):
    # TODO:数据库数据更新
    table_name = str(video_bv_id)+'_comments'
    if table_exists(con=cur, table_name=table_name) == False:
        is_create = commit_table_create(cur, video_bv_id=video_bv_id)
        if is_create == False:
            print("操作失败，正在退出当前函数")
            return False
    if commit_exit(con=cur, rid=rid, table_name=table_name, post_time_step=current_commit['post_time_step']):
        if overwrite_flag == True:
            cur.execute('UPDATE '+table_name+' SET uid = '+current_commit['uid']+
                        ', post-time-step = '+current_commit['post_time_step']+
                        ', like-number = '+current_commit['like_number']+
                        ', message = '+current_commit['message']+
                        ', has-replies = '+current_commit['has_replies']+
                        ', root-rid = '+current_commit['root_rid']+
                        ', is-top = '+current_commit['is_top']+
                        ', is-hot = '+current_commit['is_hot']+
                        ', collect-time-step = '+current_commit['collect_time_step'])
            cur.commit()
    else:
        cur.execute('INSERT INTO '+table_name+
        ' (uid, post-time-step, like-number, message, has-replies, root-rid, is-top, is-hot, collect-time-step)'+
        ' VALUES ('+current_commit['uid']+', '+current_commit['post_time_step']+', '+current_commit['like_number']+', '+current_commit['message']+', '+current_commit['has_replies']+', '+current_commit['root_rid']+', '+current_commit['is_top']+', '+current_commit['is_hot']+', '+current_commit['collect_time_step']+');')
        cur.commit()
    if commit_exit(con=cur, rid=rid, table_name=table_name, post_time_step=current_commit['post_time_step']) == False:
            print("我们遇到了错误，正在退出此函数")
            cur.rollback()
            return False
    # TODO:数据查询
    pass

def update_user_info(current_user_data, uid, user_info, cur, overwrite_flag):
    table_name = 'user_info'
    if table_exists(con=cur, table_name=table_name) == False:
        is_create = user_table_create(cur)
        if is_create == False:
            print("操作失败，正在退出当前函数")
            return False
    if overwrite_flag == True:
        cur.execute('UPDATE '+table_name+' SET uid ='+uid+
                    ', user-name = '+current_user_data['user_name']+
                    ', sign = '+current_user_data['sign']+
                    ', avatar-image-address = '+current_user_data['avatar_image_address']+
                    ', sex = '+current_user_data['sex']+
                    ', user-level = '+current_user_data['user_level']+
                    ', has-nameplate = '+current_user_data['has_nameplate']+
                    ', nameplate-kind = '+current_user_data['nameplate_kind']+
                    ', nameplate-name = '+current_user_data['nameplate_name']+
                    ', nameplate-image-address = '+current_user_data['nameplate_image_address']+
                    ', nameplate-image-small-address = '+current_user_data['nameplate-image-small-address']+
                    ', nameplate-level = '+current_user_data['nameplate_level']+
                    ', nameplate-conditiion = '+current_user_data['nameplate_conditiion']+
                    ', has-vip = '+current_user_data['has_vip']+
                    ', vip-type = '+current_user_data['vip_type']+
                    ', vip-due-timestep = '+current_user_data['vip_due_timestep']+
                    ', fans-detail = '+current_user_data['fans_detail']+
                    ', fans-level = '+current_user_data['fans_level']+
                    ', offical-type = '+current_user_data['offical_type']+
                    ', offical-desctrion = '+current_user_data['offical_desctrion']+
                    ',collect-timestep = '+current_user_data['collect-timestep']+
                    'WHERE uid = '+ uid+';')
        cur.commit()
        if user_exit(cur=cur, uid_str=uid) == False:
            print("我们遇到了错误，正在退出此函数")
            cur.rollback()
            return False

                
        

