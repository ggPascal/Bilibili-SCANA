import json
import requests

def commit_info(commit_all,commit_index,reply_ana_flag,root_rid):
    current_commit = commit_all[str(commit_index)]
    current_commit_keys = current_commit.keys()
    reply_id = int(current_commit['rpid'])

    if reply_ana_flag and root_rid == reply_id:
        pass

    member_id = int(current_commit['mid'])
    like_number = int(current_commit['like'])
    fans_detail = current_commit['']
    if fans_detail == 'null':
        fans_level = 'N/A'
    else:
        fans_level = int(current_commit['fans_grade'])
    post_time_step = current_commit['ctime']  # 注意使用的是UNIX时，贮存的是秒

    member_data = current_commit['member']
    user_name = member_data['uname']
    sex = member_data['sex']
    sign = member_data['sign']
    avatar_adress = member_data['avatar']

    level_data = member_data['level_info']
    user_level = level_data['current_level']

    if 'nameplate' in current_commit_keys:
        nameplate_data = member_data['nameplate']
        nameplate_kind = nameplate_data['nid']
        nameplate_name = nameplate_data['name']
        nameplate_image = nameplate_data['image']
        nameplate_image_small = nameplate_data['image_small']
        nameplate_level = nameplate_data['level']
        nameplate_condition = nameplate_data['condition']
        has_nameplate = 'Y'
    else:
        # 处理没有徽章的情况
        has_nameplate = 'N'
        nameplate_kind = 'N/A'
        nameplate_name = 'N/A'
        nameplate_image = 'N/A'
        nameplate_image_small = 'N/A'
        nameplate_level = 'N/A'
        nameplate_condition = 'N/A'
    if 'vip' in current_commit_keys:
        vip_data = member_data['vip']
        vip_type = int(vip_data['vipType'])
        vip_due_timestep = int(vip_data['vipDueDate'])
        has_vip = 'Y'
    else :
        has_vip = 'N'
        vip_type = 'N/A'
        vip_due_timestep = 'N/A'

    message_data = current_commit['content']
    message = message_data['message']
    if reply_ana_flag == False :
        root_rid = 'N/A'
        if message_data['replies'] == 'null':
            has_replies = 'N'
        else:
            has_replies = 'Y'




def reply_get_online():
    # example replies address: https://api.bilibili.com/x/v2/reply/reply?&jsonp=jsonp&pn=9&type=1&oid=796031275&ps=10&root=3070784970&_=1592802523767
    replies_full_url = 'https://api.bilibili.com/x/v2/reply/reply?&jsonp=jsonp&pn=' + \
        str(replay_page_now)+'&type=1&oid='+str(video_oid) + \
        '&ps=10&root='+str(root_rid)+'_='+str(root_timestep)

    replies = requests.get(replies_full_url)
    replies.encoding = 'utf-8'
    replies_json = replies.text
    commit_data = json.loads(replies_data)
    reply_index = 0
    reply_ana_flag = True
    root_rid = reply_id 
    root_timestep = post_time_step
    while reply_index in commit_data.keys() :
        commit_info()
        reply_index = reply_index + 1
    


def commit_json_ana(f):
    json_data = json.load(f)
    commit_data = json_data['data']  # 获取评论区数据
    if page_init == True:
        page_data = commit_data['page']  # 获取页数据
        page_now = int(page_data['num'])
        commit_size = int(page_data['size'])
        all_commit = int(page_data['acount'])
    commit_all = commit_data['replies']
    commit_index_list = commit_all.keys()
    while commit_index in commit_index_list :
        commit_info(commit_all,commit_index,reply_ana_flag=False,None)
        build_commit_dictory() # 建立当前评论的字典数据
        all_commit_direct[reply_id] = commit_info
        all_user_dict[member_id] = commit_user_info # 保存当前数据
        commit_index = commit_index + 1
    # 顶置评论获取与标记
    upper_data = commit_data['upper']
    if 'top' in upper_data.keys():
        commit_index = 0
        commit_all = upper_data['top']
        is_top = 'Y'
        commit_info()
        build_commit_dictory()


   