import json

import requests

import time
import numba as nb


def init():
    print("Initializing sum dicts")
    all_user_dict = {}
    all_commit_direct = {}
    return all_user_dict, all_commit_direct


def video_info(video_data):  # BV查看页数据工作
    video_basic_data = video_data
    print("Geting video info")
    video_oid = video_basic_data['aid']
    copyright_type = video_basic_data['copyright']
    picture_add = video_basic_data['pic']
    post_time_step = video_basic_data['pubdate']
    cite_time_step = video_basic_data['ctime']
    desctrion = video_basic_data['desc']

    owner_data = video_data['owner']
    owner_mid = owner_data['mid']

    state_data = video_data['stat']
    view_number = state_data['view']
    commit_number = state_data['reply']
    favorite_number = state_data['favorite']
    coin_number = state_data['coin']
    share_number = state_data['share']
    daily_highest_rank = state_data['his_rank']
    like_number = state_data['like']
    dislike_number = state_data['dislike']

    print("building video_info")
    video_info_dire = {
        'video_oid': video_oid,
        'copyright_type': copyright_type,
        'picture_add': picture_add,
        'post_time_step': post_time_step,
        'cite_time_step': cite_time_step,
        'desctrion': desctrion,
        'owner_uid': owner_mid,
        'view_number': view_number,
        'favorite_number': favorite_number,
        'coin_number': coin_number,
        'share_number': share_number,
        'daily_highest_rank': daily_highest_rank,
        'like_number': like_number,
        'dislike_number': dislike_number,
        'commit_number': commit_number

    }
    return video_info_dire


def reply_get_online(video_oid, root_rid, root_timestep, all_user_dict, all_commit_direct):
    # example replies address: https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn=1&type=1&oid=841277747&ps=10&root=3168291096&_=1595026441853
    # Example BV： BV1w54y1q7XQ
    replies_get_not_done = True
    replay_page_now = 0
    replies_full_url = 'https://api.bilibili.com/x/v2/reply/reply?&jsonp=jsonp&pn=' + \
        str(1)+'&type=1&oid='+str(video_oid) + \
        '&ps=10&root='+str(root_rid)+'&_='+str(root_timestep)

    replies = requests.get(replies_full_url)
    replies.encoding = 'utf-8'
    replies_json = replies.text
    commit_data = json.loads(replies_json)
    commit_data = commit_data['data']
    page_data = commit_data['page']
    replies_number = page_data['count']
    # Get the data that calculates count of pages
    replies_show_size = page_data['size']
    if replies_number == 0:
        return False
    else:
        print("Found replies")
        if replies_number < replies_show_size:
            page_count = 1
        else:
            if replies_number % replies_show_size != 0:
                page_count = (replies_number // replies_show_size) + 1
            else:
                page_count = replies_number // replies_show_size
    print('Total pages : '+str(page_count))
    for replay_page_now in range(1, page_count):
        replay_page_now = replay_page_now + 1
        print('Collecting on : '+str(replay_page_now)+'/'+str(page_count))
        replies_full_url = 'https://api.bilibili.com/x/v2/reply/reply?&jsonp=jsonp&pn=' + \
            str(replay_page_now)+'&type=1&oid='+str(video_oid) + \
            '&ps=10&root='+str(root_rid)+'&_='+str(root_timestep)

        replies = requests.get(replies_full_url)
        replies.encoding = 'utf-8'
        replies_json = replies.text
        commit_data = json.loads(replies_json)
        replies_data = commit_data['replies']

        reply_index = 0
        reply_ana_flag = True
        for reply_index in range(0, len(replies_data)):
            print('collecting '+str(reply_index)+'/'+str(len(replies_data)+1))
            commit_info(commit_all=commit_data, commit_index=reply_index, reply_ana_flag=reply_ana_flag, root_rid=root_rid,
                        all_user_dict=all_user_dict, all_commit_direct=all_commit_direct, collect_time_step=time.time(), is_top='N', is_list=True, is_hot='N', video_oid=None)
            reply_index = reply_index + 1
        replies_get_not_done = True


def commit_info(video_oid, commit_all, commit_index, reply_ana_flag, root_rid, all_user_dict, all_commit_direct, collect_time_step, is_top, is_list, is_hot):
    if is_list:
        current_commit = commit_all[commit_index]
    else:
        current_commit = commit_all[str(commit_index)]
    current_commit_keys = current_commit.keys()
    reply_id = int(current_commit['rpid'])  # 获取评论ID

    if reply_ana_flag and root_rid == reply_id:  # 用于回复分析模式下跳过主评论
        pass

    member_id = int(current_commit['mid'])  # 获取UID
    like_number = int(current_commit['like'])  # 获取点赞数
    if 'fans_detail' in current_commit_keys:
        fans_detail = current_commit['fans_detail']
        fans_level = int(current_commit['fans_grade'])
    else:
        fans_detail = 'N/A'
        fans_level = 'N/A'
    post_time_step = current_commit['ctime']  # 注意使用的是UNIX时，贮存的是秒

    member_data = current_commit['member']
    user_name = member_data['uname']  # 获取用户名
    sex = member_data['sex']  # 获取性别
    sign = member_data['sign']  # 获取个人签名
    avatar_adress = member_data['avatar']  # 获取头像地址
    if 'offcial_verify' in member_data.keys():
        offical_data = member_data['offcial_verify']
        offical_type = member_data['type']
        if 'desc' in offical_data.keys():
            offical_desctrion = offical_data['desc']
            if offical_desctrion == None:
                offical_desctrion = 'N/A'
        else:
            offical_desctrion = 'N/A'
    else:
        offical_type = 'N/A'
        offical_desctrion = 'N/A'

    level_data = member_data['level_info']
    user_level = level_data['current_level']  # 获取等级

    if 'nameplate' in current_commit_keys:  # 判断是否有名牌
        nameplate_data = member_data['nameplate']
        nameplate_kind = nameplate_data['nid']  # 获取名牌ID
        nameplate_name = nameplate_data['name']  # 获取名称
        nameplate_image = nameplate_data['image']  # 获取此名牌对应的图片
        nameplate_image_small = nameplate_data['image_small']  # 获取缩小版图片
        nameplate_level = nameplate_data['level']  # 获取等级
        nameplate_condition = nameplate_data['condition']  # 获取对应名牌简介
        has_nameplate = 'Y'
    else:
        # 处理没有徽章的情况，全部替换为N/A
        has_nameplate = 'N'
        nameplate_kind = 'N/A'
        nameplate_name = 'N/A'
        nameplate_image = 'N/A'
        nameplate_image_small = 'N/A'
        nameplate_level = 'N/A'
        nameplate_condition = 'N/A'
    if 'vip' in current_commit_keys:  # 检测是否有VIP
        vip_data = member_data['vip']
        vip_type = int(vip_data['vipType'])  # 获取VIP种类
        vip_due_timestep = int(vip_data['vipDueDate'])  # 获取该VIP的截止时间
        has_vip = 'Y'
    else:
        # 处理没有VIP的情况，全部替换为N/A
        has_vip = 'N'
        vip_type = 'N/A'
        vip_due_timestep = 'N/A'

    message_data = current_commit['content']
    message_data_keys = member_data.keys()
    message = message_data['message']  # 获取评论/回复内容，表情包将换为对应字符表达
    if reply_ana_flag == False:
        root_rid = 'N/A'
        if 'replies' not in message_data_keys:
            has_replies = 'N'
        else:
            has_replies = 'Y'
    if member_id not in all_user_dict.keys():
        commit_user_info = {
            'user_name': user_name,
            'sign': sign,
            'avatar_image_address': avatar_adress,
            'sex': sex,
            'user_level': user_level,
            'has_nameplate': has_nameplate,
            'nameplate_kind': nameplate_kind,
            'nameplate_name': nameplate_name,
            'nameplate_image': nameplate_image,
            'nameplate_image_small': nameplate_image_small,
            'nameplate_level': nameplate_level,
            'nameplate_condition': nameplate_condition,
            'has_vip': has_vip,
            'vip_type': vip_type,
            'fans_detail': fans_detail,
            'fans_level': fans_level,
            'offical_type': offical_type,
            'offical_desctrion': offical_desctrion,
            'vip_due_timestep': vip_due_timestep,
        }
        all_user_dict[member_id] = commit_user_info  # uid作为键

    if reply_ana_flag == False and video_oid == None:
        pass
    else:
        reply_get_online(video_oid=video_oid, root_rid=reply_id, root_timestep=collect_time_step,
                         all_commit_direct=all_commit_direct, all_user_dict=all_user_dict)
    if reply_id not in all_commit_direct.keys():
        commit_info = {
            'uid': member_id,
            'time': post_time_step,
            'like_number': like_number,
            'message': message,
            'has_replies': has_replies,
            'root_rid': root_rid,
            'is_top': is_top,
            'is_hot': is_hot,
            'collect_time': collect_time_step
        }
        all_commit_direct[reply_id] = commit_info

    return all_commit_direct, all_user_dict


def commit_json_ana(f, page_init, is_file, json_data, all_commit_direct, all_user_dict, video_oid):
    if is_file:
        json_data = json.load(f)
    commit_data = json_data['data']  # 获取评论区数据
    page_data = commit_data['page']  # 获取页数据
    page_now = int(page_data['num'])
    if page_init == True:
        commit_size = int(page_data['size'])
        all_commit = int(page_data['acount'])
    commit_all = commit_data['replies']
    commit_index = 0
    for commit_index in range(0, len(commit_all)-1):
        all_commit_direct, all_user_dict = commit_info(commit_all=commit_all, commit_index=commit_index,
                                                       reply_ana_flag=False, root_rid=None, all_commit_direct=all_commit_direct, all_user_dict=all_user_dict, collect_time_step=time.time(), is_top='N', is_list=True, is_hot='N', video_oid=video_oid)
        # 建立当前评论的字典数据
    # 顶置评论获取与标记
    upper_data = commit_data['upper']
    if 'top' in upper_data.keys():
        print('found upper conment, start collecting')
        commit_index = 0
        commit_all = upper_data['top']
        if commit_all != None:
            is_top = 'Y'
            all_commit_direct, all_user_dict = commit_info(video_oid=None, commit_all=commit_all, commit_index=0, reply_ana_flag=False, root_rid=None, all_user_dict=all_user_dict,
                                                           all_commit_direct=all_commit_direct, collect_time_step=time.time(), is_top=is_top, is_list=False, is_hot='N')

    if 'hots' in commit_data.keys():
        commit_index = 0
        commit_all = commit_data['hots']
        if commit_all != None:
            total_number = len(commit_all)
            for commit_index in range(0, total_number):
                print('collecting '+str(commit_index) +'/' + str(total_number))
                all_commit_direct, all_user_dict = commit_info(video_oid=None, commit_all=commit_all, commit_index=commit_index, reply_ana_flag=False, root_rid=None,
                                                               all_user_dict=all_user_dict, all_commit_direct=all_commit_direct, collect_time_step=time.time(), is_top=False, is_list=True, is_hot='Y')

    return all_commit_direct, all_user_dict
