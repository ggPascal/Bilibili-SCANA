import json

import requests

from dire_manger import *

def video_info(video_data): # 使用评论区数据工作
    video_basic_data = video_data['data']
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

    video_info_dire = {
        'video_av': video_oid,
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
        'dislike_number': dislike_number

    }
    return video_info_dire 
    
def commit_info(commit_all, commit_index, reply_ana_flag, root_rid):
    current_commit = commit_all[str(commit_index)]
    current_commit_keys = current_commit.keys()
    reply_id = int(current_commit['rpid'])  # 获取评论ID

    if reply_ana_flag and root_rid == reply_id:  # 用于回复分析模式下跳过主评论
        pass

    member_id = int(current_commit['mid'])  # 获取UID
    like_number = int(current_commit['like'])  # 获取点赞数
    fans_detail = current_commit['fans_detail']
    fans_level = int(current_commit['fans_grade'])
    post_time_step = current_commit['ctime']  # 注意使用的是UNIX时，贮存的是秒

    member_data = current_commit['member']
    user_name = member_data['uname']  # 获取用户名
    sex = member_data['sex']  # 获取性别
    sign = member_data['sign']  # 获取个人签名
    avatar_adress = member_data['avatar']  # 获取头像地址

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
    message = message_data['message']  # 获取评论/回复内容，表情包将换为对应字符表达
    if reply_ana_flag == False:
        root_rid = 'N/A'
        if message_data['replies'] == 'null':
            has_replies = 'N'
        else:
            has_replies = 'Y'


def reply_get_online(replay_page_now, video_oid, root_rid, root_timestep):
    # example replies address: https://api.bilibili.com/x/v2/reply/reply?&jsonp=jsonp&pn=9&type=1&oid=796031275&ps=10&root=3070784970&_=1592802523767
    replies_full_url = 'https://api.bilibili.com/x/v2/reply/reply?&jsonp=jsonp&pn=' + \
        str(replay_page_now)+'&type=1&oid='+str(video_oid) + \
        '&ps=10&root='+str(root_rid)+'_='+str(root_timestep)

    replies = requests.get(replies_full_url)
    replies.encoding = 'utf-8'
    replies_json = replies.text
    commit_data = json.loads(replies_json)
    reply_index = 0
    reply_ana_flag = True
    while reply_index in commit_data.keys():
        commit_info(commit_data, reply_index, reply_ana_flag, root_rid)
        reply_index = reply_index + 1


def commit_json_ana(f, page_init):
    json_data = json.load(f)
    commit_data = json_data['data']  # 获取评论区数据
    if page_init == True:
        page_data = commit_data['page']  # 获取页数据
        page_now = int(page_data['num'])
        commit_size = int(page_data['size'])
        all_commit = int(page_data['acount'])
    commit_all = commit_data['replies']
    commit_index_list = commit_all.keys()
    commit_index = 0
    while commit_index in commit_index_list:
        commit_info(commit_all, commit_index,
                    reply_ana_flag=False, root_rid=None)
        build_commit_dictory()  # 建立当前评论的字典数据
        commit_index = commit_index + 1
    # 顶置评论获取与标记
    upper_data = commit_data['upper']
    if 'top' in upper_data.keys():
        commit_index = 0
        commit_all = upper_data['top']
        is_top = 'Y'
        commit_info(commit_all, 0, reply_ana_flag=False, root_rid=None)
        build_commit_dictory()
