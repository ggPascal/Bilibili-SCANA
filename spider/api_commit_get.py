import json

import requests

import time

# The note will be comment the code at below one line
# Example:
# # SOME note
# The code that note are saying

# Initialize the dictionary that timestep_key_dire will be use
def init():
    print("Initializing sum dicts")
    all_user_dict = {}
    all_commit_direct = {}
    return all_user_dict, all_commit_direct

# Decode json information from video info API from bilibili
def video_info(video_data):  # BV查看页数据工作
    video_basic_data = video_data
    print("Geting video info")
    
    # Basic video info
    video_oid = video_basic_data['aid']
    copyright_type = video_basic_data['copyright']
    picture_add = video_basic_data['pic']
    post_time_step = video_basic_data['pubdate']
    cite_time_step = video_basic_data['ctime']
    desctrion = video_basic_data['desc']

    # Owner info
    owner_data = video_data['owner']
    owner_mid = owner_data['mid']

    # Status info
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

# dectet if the comment has replies
def detect_replies(video_oid, root_rid, root_timestep):
    page_count = 0
    # Get the replies json information
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
    replies_show_size = page_data['size']

    # Dectet the replies
    if replies_number == 0:
        replies_found = False
    else:
        print("Found replies")
        replies_found = True
        
        # Calculatie the total page number
        if replies_number < replies_show_size:
            page_count = 1
        else:
            if replies_number % replies_show_size != 0:
                page_count = (replies_number // replies_show_size) + 1
            else:
                page_count = replies_number // replies_show_size
        print('Total pages : '+str(page_count))
    return replies_found, commit_data, page_count

# Get comments json information and decode to human-readable dictonary(include replies)
def reply_get_online(video_oid, root_rid, root_timestep, all_user_dict, all_commit_direct, commit_data, page_count, continue_mode_enable, timestep_file, timestep_add_mode, timestep_key_dire, all_user_full_timestep_dict, all_commit_full_timestep_dict):
    # example replies address: https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn=1&type=1&oid=841277747&ps=10&root=3168291096&_=1595026441853
    # Example BV： BV1w54y1q7XQ
    replay_page_now = 0

    for replay_page_now in range(0, page_count):
        # 2020/07/18 Special vaule rpid : 3199917477

        # Get the comments data
        print('Collecting on page : '+str(replay_page_now)+'/'+str(page_count))
        replies_full_url = 'https://api.bilibili.com/x/v2/reply/reply?&jsonp=jsonp&pn=' + \
            str(replay_page_now)+'&type=1&oid='+str(video_oid) + \
            '&ps=10&root='+str(root_rid)+'&_='+str(root_timestep)

        replies = requests.get(replies_full_url)
        replies.encoding = 'utf-8'
        replies_json = replies.text
        commit_data = json.loads(replies_json)
        commit_data = commit_data['data']
        replies_data = commit_data['replies']

        # Call decode function
        reply_index = 0
        for reply_index in range(0, len(replies_data)):
            print('collecting '+str(reply_index+1)+'/'+str(len(replies_data)))
            all_commit_direct, all_user_dict = commit_info(continue_mode_enable=continue_mode_enable, commit_all=replies_data, commit_index=reply_index, reply_ana_flag=False, root_rid=root_rid,
                                                           all_user_dict=all_user_dict, all_commit_direct=all_commit_direct, collect_time_step=time.time(), is_top='N', is_list=True, is_hot='N', video_oid=video_oid, timestep_file=timestep_file, timestep_add_mode=timestep_add_mode, timestep_key_dire=timestep_key_dire, all_user_full_timestep_dict=all_user_full_timestep_dict, all_commit_full_timestep_dict=all_commit_full_timestep_dict)

    return all_commit_direct, all_user_dict

# Decode comments json data and get all replies
def commit_info(continue_mode_enable, video_oid, commit_all, commit_index, reply_ana_flag, root_rid, all_user_dict, all_commit_direct, collect_time_step, is_top, is_list, is_hot, timestep_file, timestep_add_mode, timestep_key_dire, all_user_full_timestep_dict, all_commit_full_timestep_dict):
    has_replies = None
    
    # Deal with the case that only have one comments 
    if commit_index == 'N/A':
        current_commit = commit_all
    else:
        if is_list:
            current_commit = commit_all[commit_index]
        else:
            current_commit = commit_all[str(commit_index)]
    current_commit_keys = current_commit.keys()

    # Get reply ID
    # 获取评论ID
    reply_id = int(current_commit['rpid'])  
    # For continue mode pass exit reply
    if continue_mode_enable and reply_id in all_commit_direct.keys():  
        pass
    else:
        if reply_ana_flag == False:
            root_rid = int(current_commit['parent'])
        else:
            root_rid = 'N/A'

        # Pass the root comment when collecting replies
        # 用于回复分析模式下跳过主评论
        if reply_ana_flag and root_rid == reply_id:  
            pass
        # Get the user ID
        member_id = int(current_commit['mid'])  # 获取UID
        like_number = int(current_commit['like'])

        if 'fans_detail' in current_commit.keys():
            fans_detail = current_commit['fans_detail']
            fans_level = int(current_commit['fans_grade'])
        else:
            fans_detail = 'N/A'
            fans_level = 'N/A'

        # Notice that it use UNIX time 
        # 注意使用的是UNIX时，贮存的是秒
        post_time_step = current_commit['ctime']  

        # Get the user data
        member_data = current_commit['member']
        # Get user name
        # 获取用户名
        user_name = member_data['uname']  
        sex = member_data['sex']  
        sign = member_data['sign']  
        # Get the avatar image url
        # 获取头像地址
        avatar_adress = member_data['avatar']  
        member_data_keys = member_data.keys()
        if 'official_verify' in member_data.keys():
            offical_data = member_data['official_verify']
            offical_type = offical_data['type']
            if 'desc' in offical_data.keys():
                offical_desctrion = offical_data['desc']
                if offical_desctrion == '':
                    offical_desctrion = 'N/A'
            else:
                offical_desctrion = 'N/A'
        else:
            offical_type = 'N/A'
            offical_desctrion = 'N/A'

        level_data = member_data['level_info']
        user_level = level_data['current_level']  

        if 'nameplate' in member_data.keys():  
            nameplate_data = member_data['nameplate']
            # Get the nameplate ID 
            # 获取名牌ID
            nameplate_kind = nameplate_data['nid']  
            if nameplate_kind != 0:
                nameplate_name = nameplate_data['name']  
                # Get the full size showing image url
                # 获取此名牌对应的全尺寸展示图片URL
                nameplate_image = nameplate_data['image']  
                # Get the smaller size one url
                # 获取缩小版图片URL
                nameplate_image_small = nameplate_data['image_small']
                nameplate_level = nameplate_data['level']  # 获取等级
                nameplate_condition = nameplate_data['condition']  # 获取对应名牌简介
                has_nameplate = 'Y'
            else:
                has_nameplate = 'N'
                nameplate_kind = 'N/A'
                nameplate_name = 'N/A'
                nameplate_image = 'N/A'
                nameplate_image_small = 'N/A'
                nameplate_level = 'N/A'
                nameplate_condition = 'N/A'
        else:
            has_nameplate = 'N'
            nameplate_kind = 'N/A'
            nameplate_name = 'N/A'
            nameplate_image = 'N/A'
            nameplate_image_small = 'N/A'
            nameplate_level = 'N/A'
            nameplate_condition = 'N/A'

        if 'vip' in member_data.keys():  
            vip_data = member_data['vip']
            vip_type = int(vip_data['vipType']) 
            vip_due_timestep = int(vip_data['vipDueDate'])  
            has_vip = 'Y'
        else:
            has_vip = 'N'
            vip_type = 'N/A'
            vip_due_timestep = 'N/A'

        message_data = current_commit['content']
        message_data_keys = member_data.keys()
        # Get the comments/replies text, meme image will be replace to text(Convert by bilibili API)
        # 获取评论/回复内容，表情包将换为对应字符表达（此部分由Bilibili的API完成）
        message = message_data['message']  

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
                'last-same': 'N'
            }
           
            # Pointer genete for timestep_add_mode
            if timestep_add_mode:
                for key in list(commit_user_info.keys()):

                    # Passed the key of comment collect time
                    if key == 'collect_time':
                        continue
                    last_time_step_found = False

                    # try:
                    # Get the information of time step that exists from exits dictorary 
                    last_user_dire_timestep_list = list(
                        all_user_full_timestep_dict.keys())
                    target_timestep_index = len(
                        last_user_dire_timestep_list) - 1
                    # Get the leaest time step
                    target_timestep = last_user_dire_timestep_list[target_timestep_index]
                    # Jump to target time step
                    last_time_step_user_dire = all_user_full_timestep_dict[target_timestep]

                    # Start to compare data 
                    if str(member_id) in last_time_step_user_dire.keys():
                        test_last_time_step_user_dire = last_time_step_user_dire[str(
                            member_id)]
                        test_last_time_step_user_dire = test_last_time_step_user_dire[key]
                        # Dected the data type to aviod bug of type problem
                        if type(test_last_time_step_user_dire) == dict:
                            if 'last_time_step_pointer' in test_last_time_step_user_dire.keys():
                                # Get the pointer
                                last_time_step = test_last_time_step_user_dire['last_time_step_pointer']
                                last_time_step_found = True
                            else:
                                print('Can not found old data for '+key +
                                      ' data in user_dict, skipping current data')
                        else:
                            print('Can not found old data for '+key +
                                  ' data in user_dict, skipping current data')
                    else:
                        print('Can not found old data for '+key +
                              ' data in user_dict, skipping current data')
                    # except KeyError:
                        #last_time_step_found = False
                        #print('Can not found old data for '+key+' data in user_dict, skipping current data')
                        # pass

                    # Copy the pointer to the timestep data now
                    if last_time_step_found:
                        # Load pointer from old data
                        if timestep_file:
                            last_all_user_dire_file_name = str(
                                last_time_step)+'_all_user_dire.json'
                            last_all_user_dire_file = open(
                                last_all_user_dire_file_name, 'r', encoding='utf-8')
                            last_time_step_user_dire = json.loads(
                                last_all_user_dire_file)
                        
                        if timestep_key_dire:
                            last_time_step_user_dire = all_user_full_timestep_dict[str(
                                last_time_step)]

                        last_time_step_user_dire = last_time_step_user_dire[str(
                            member_id)]
                        found_old_data = True

                    else:
                        # Load old data dictionary
                        if str(member_id) in last_time_step_user_dire.keys():
                            last_time_step_user_dire = last_time_step_user_dire[str(
                                member_id)]
                            found_old_data = True
                        else:
                            print('Can not found old data for '+key +
                                  ' data in user_dict, creating new record')
                            found_old_data = False
                    
                    # Generate pointer or copy the pointer from old data
                    if found_old_data:
                        if last_time_step_user_dire[key] == commit_user_info[key]:
                            print('Find same data for '+key +
                                  ' , wrting pointer to it.')
                            if last_time_step_found == False:
                                last_time_step = target_timestep
                                commit_user_info[key] = {
                                    'last_time_step_pointer': last_time_step}
                            else:
                                commit_user_info[key] = {
                                    'last_time_step_pointer': last_time_step}

            all_user_dict[member_id] = commit_user_info  # uid作为键

        # Get replies data
        if reply_ana_flag == True:
            has_replies, replies_data, page_count = detect_replies(
                video_oid=video_oid, root_rid=reply_id, root_timestep=collect_time_step)

        if has_replies:
            has_replies = 'Y'
        else:
            has_replies = 'N'

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
            # TODO: change the name of vaule and file name
            if timestep_add_mode:
                for key in commit_info.keys():
                    if key == 'collect_time':
                        continue
                    last_time_step_found = False
                    # try:
                    last_comment_dire_timestep_list = list(
                        all_commit_full_timestep_dict.keys())
                    target_timestep = last_comment_dire_timestep_list[len(
                        last_comment_dire_timestep_list) - 1]
                    last_time_step_comment_dire = all_commit_full_timestep_dict[target_timestep]
                    if str(reply_id) in last_time_step_comment_dire.keys():
                        test_last_time_step_comment_dire = last_time_step_comment_dire[str(
                            reply_id)]
                        test_last_time_step_comment_dire = test_last_time_step_comment_dire[key]
                        if type(test_last_time_step_comment_dire) == dict:
                            if 'last_time_step_pointer' in test_last_time_step_comment_dire.keys():
                                last_time_step = test_last_time_step_comment_dire['last_time_step_pointer']
                                last_time_step_found = True
                            else:
                                print('Can not found pointer for '+key +
                                      ' data in comment_dict, Ignore current pointer')
                        else:
                            print('Can not found pointer for '+key +
                                  ' data in comment_dict, skipping current pointer')
                    else:
                        print('Can not found pointer for '+key +
                              ' data in comment_dict, skipping current pointer')
                    # except KeyError:
                        #last_time_step_found = False
                        #print('Can not found old data for '+key+' data in comment_dict, skipping current data')
                        # pass
                    if last_time_step_found:
                        if timestep_file:
                            last_all_dire_file_name = str(last_time_step)
                            last_all_dire_file = open(
                                last_all_dire_file_name, 'r', encoding='utf-8')
                            last_commit_dire = json.loads(last_all_dire_file)
                        if timestep_key_dire:
                            last_commit_dire = all_commit_full_timestep_dict[str(
                                last_time_step)]
                        last_commit_dire = last_commit_dire[str(reply_id)]
                        found_old_data = True
                    else:
                        if str(reply_id) in last_time_step_comment_dire.keys():
                            last_commit_dire = last_time_step_comment_dire[str(
                                reply_id)]
                            found_old_data = True
                        else:
                            found_old_data = False
                            print('Can not found old data for '+key +
                                  ' data in commit_dict, creating new record')
                    if found_old_data:
                        if last_commit_dire[key] == commit_info[key]:
                            print('Find same data for '+key +
                                  ' , wrting pointer to it.')
                            if last_time_step_found == False:
                                last_time_step = target_timestep
                                commit_info[key] = {
                                    'last_time_step_pointer': last_time_step}
                            else:
                                commit_info[key] = {
                                    'last_time_step_pointer': last_time_step}

            all_commit_direct[reply_id] = commit_info

        # This replies get use for hot comments and top comments
        if reply_ana_flag == False:
            pass
        else:
            reply_get_online(continue_mode_enable=continue_mode_enable, video_oid=video_oid, root_rid=reply_id, root_timestep=collect_time_step,
                             all_commit_direct=all_commit_direct, all_user_dict=all_user_dict, commit_data=replies_data, page_count=page_count, timestep_file=timestep_file, timestep_add_mode=timestep_add_mode, timestep_key_dire=timestep_key_dire, all_user_full_timestep_dict=all_user_full_timestep_dict, all_commit_full_timestep_dict=all_commit_full_timestep_dict)

    return all_commit_direct, all_user_dict


def commit_json_ana(continue_mode_enable, f, page_init, is_file, json_data, all_commit_direct, all_user_dict, video_oid, timestep_file, timestep_add_mode, timestep_key_dire, all_user_full_timestep_dict, all_commit_full_timestep_dict):
    hot_collect_flag = None

    if is_file:
        json_data = json.load(f)
    commit_data = json_data['data']  # 获取评论区数据
    page_data = commit_data['page']  # 获取页数据
    page_now = int(page_data['num'])
    if page_init == True:
        commit_size = int(page_data['size'])
        all_commit = int(page_data['acount'])
        hot_collect_flag = True
    commit_all = commit_data['replies']
    commit_index = 0
    for commit_index in range(0, len(commit_all)):
        print("collecting commit "+str(commit_index)+'/'+str(len(commit_all)-1))
        all_commit_direct, all_user_dict = commit_info(continue_mode_enable=continue_mode_enable, commit_all=commit_all, commit_index=commit_index,
                                                       reply_ana_flag=True, root_rid='N/A', all_commit_direct=all_commit_direct, all_user_dict=all_user_dict, collect_time_step=time.time(), is_top='N', is_list=True, is_hot='N', video_oid=video_oid, timestep_file=timestep_file, timestep_add_mode=timestep_add_mode, timestep_key_dire=timestep_key_dire, all_user_full_timestep_dict=all_user_full_timestep_dict, all_commit_full_timestep_dict=all_commit_full_timestep_dict)
        # 建立当前评论的字典数据
    # 顶置评论获取与标记
    upper_data = commit_data['upper']
    if 'top' in upper_data.keys() and page_init == True:
        print('found upper conment, start collecting')
        commit_all = upper_data['top']
        if commit_all != None:
            is_top = 'Y'
            all_commit_direct, all_user_dict = commit_info(continue_mode_enable=continue_mode_enable, video_oid=video_oid, commit_all=commit_all, commit_index='N/A', reply_ana_flag=True, root_rid='N/A', all_user_dict=all_user_dict,
                                                           all_commit_direct=all_commit_direct, collect_time_step=time.time(), is_top=is_top, is_list=True, is_hot='N', timestep_file=timestep_file, timestep_add_mode=timestep_add_mode, timestep_key_dire=timestep_key_dire, all_user_full_timestep_dict=all_user_full_timestep_dict, all_commit_full_timestep_dict=all_commit_full_timestep_dict)

    if 'hots' in commit_data.keys() and page_init == True :
        commit_index = 0
        commit_all = commit_data['hots']
        if commit_all != None:
            total_number = len(commit_all)
            print("Found hot comments")
            for commit_index in range(0, total_number):
                print('collecting hot comments ' +
                      str(commit_index) + '/' + str(total_number))
                all_commit_direct, all_user_dict = commit_info(continue_mode_enable=continue_mode_enable, video_oid=video_oid, commit_all=commit_all, commit_index=commit_index, reply_ana_flag=True, root_rid='N/A',
                                                               all_user_dict=all_user_dict, all_commit_direct=all_commit_direct, collect_time_step=time.time(), is_top=False, is_list=True, is_hot='Y', timestep_file=timestep_file, timestep_add_mode=timestep_add_mode, timestep_key_dire=timestep_key_dire, all_user_full_timestep_dict=all_user_full_timestep_dict, all_commit_full_timestep_dict=all_commit_full_timestep_dict)
            hot_collect_flag = False

    return all_commit_direct, all_user_dict
