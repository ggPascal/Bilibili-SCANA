import prettytable as pt
import json
import os


def dire_save():
    json.dump(enc, f)

def build_upper_dict(comment_data_dict):
    for reply_id in list(comment_data_dict.keys()):
        upper_tree_list = []
        while str(current_root_rid) != current_reply_id and current_root_rid != 'N/A':
            current_upper_rid = current_root_rid
            upper_message_dict = comment_data_dict[str(
                current_upper_rid)]
            current_reply_id = current_upper_rid
            upper_tree_list.append(
                upper_message_dict['message'])
            current_root_rid = upper_message_dict['root_rid']
        if upper_tree_list == None or upper_tree_list == []:
            upper_message_dict[reply_id] = 'N/A'
        else:
            for message_index in range(0, len(upper_tree_list)):
                result_upper_tree_list[message_index] = upper_tree_list[len(upper_tree_list)-1-message]
                show_index = show_index + 1
            upper_message_dict[reply_id] = result_upper_tree_list
    return upper_message_dict

def build_following_message_dict():
    for reply_id in list(comment_data_dict.keys()):
        for deep_search_rid in list(comment_data_dict.keys()):
            deep_search_dict = comment_data_dict[str(
                deep_search_rid)]
            current_root_rid = deep_search_dict['root_rid']
            if str(current_root_rid) == str(reply_id):
                follow_message_list.append(deep_search_dict['message'])
        if follow_message_list != None or follow_message_list == [] :
            follow_message_dict[reply_id] = follow_message_list
        else:
            follow_message_dict[reply_id] = 'N/A'
    return follow_message_dict

def comment_data_dict_tag(comment_data_dict, tag_contune, tag_coment_dict):
    try:
        all_count = len(comment_data_dict.keys())
        current_count = 1
        for reply_id in list(comment_data_dict.keys()):
            current_count = current_count + 1
            if tag_contune:
                if reply_id not in tag_coment_dict.keys():
                    os.system('cls')
                    print('Progress : '+str(current_count)+'/'+str(all_count))
                    retry_flag = True
                    while retry_flag:
                        upper_tree_list = []
                        deep_search_dict = {}
                        message_dict = comment_data_dict[str(reply_id)]
                        current_message = message_dict['message']
                        current_reply_id = reply_id
                        current_root_rid = message_dict['root_rid']
                        if current_reply_id != str(current_root_rid) and str(current_root_rid) != 'N/A':
                            while str(current_root_rid) != current_reply_id and current_root_rid != 'N/A':
                                current_upper_rid = current_root_rid
                                upper_message_dict = comment_data_dict[str(
                                    current_upper_rid)]
                                current_reply_id = current_upper_rid
                                upper_tree_list.append(
                                    upper_message_dict['message'])
                                current_root_rid = upper_message_dict['root_rid']
                            print("Root Diaelog of current message:")
                            upper_message_show = pt.PrettyTable()
                            upper_message_show.field_names = [
                                '#', 'message']
                            message_index = 0
                            show_index = 1
                            for message_index in range(0, len(upper_tree_list)):
                                upper_message_show.add_row(
                                    [str(show_index), upper_tree_list[len(upper_tree_list)-1-message_index]])
                                
                                show_index = show_index + 1
                            print(upper_message_show)
                            has_upper_message = True
                        else:
                            print(
                                "This is the root message, does not have any root dialog.")
                            has_upper_message = False
                        print('Current message :')
                        print(current_message)
                        deep_message_show = pt.PrettyTable()
                        deep_message_show.field_names = ['#', 'message']
                        deep_index = 0
                        for deep_search_rid in list(comment_data_dict.keys()):
                            deep_search_dict = comment_data_dict[str(
                                deep_search_rid)]
                            current_root_rid = deep_search_dict['root_rid']
                            if str(current_root_rid) == str(reply_id):
                                deep_index = deep_index + 1
                                deep_message_show.add_row(
                                    [str(deep_index), deep_search_dict['message']])
                        print("Following replies: ")
                        print(deep_message_show)
                        print('Socre feeling:')
                        input_error = True
                        while input_error:
                            postive = input(
                                "Is message positive?(-1/1 , 1 is postive): ")
                            postive = int(postive)
                            if (postive > -1 or postive == -1) and (postive < 1 or postive == 1):
                                input_error = False
                            else:
                                print("Out of range, please check what you type")
                                input_error = True

                        input_error = True
                        while input_error:
                            happiness = input(
                                "How happy is this message? (0/10): ")
                            happiness = int(happiness)
                            if (happiness > 0 or happiness == 0) and (happiness < 10 or happiness == 10):
                                input_error = False
                            else:
                                print("Out of range, please check what you type")
                                input_error = True

                        input_error = True
                        while input_error:
                            admire = input(
                                "How much admire is this message show ? (0/10): ")
                            admire = int(admire)
                            if (admire > 0 or admire == 0) and (admire < 10 or admire == 10):
                                input_error = False
                            else:
                                print("Out of range, please check what you type")
                                input_error = True

                        input_error = True
                        while input_error:
                            sadness = input(
                                "How sad is this message? (0/10): ")
                            sadness = int(sadness)
                            if (sadness > 0 or sadness == 0) and (sadness < 10 or sadness == 10):
                                input_error = False
                            else:
                                print("Out of range, please check what you type")
                                input_error = True

                        input_error = True
                        while input_error:
                            angry = input(
                                "How angry is this message? (0/10): ")
                            angry = int(angry)
                            if (angry > 0 or angry == 0) and (angry < 10 or angry == 10):
                                input_error = False
                            else:
                                print("Out of range, please check what you type")
                                input_error = True

                        input_error = True
                        while input_error:
                            ridicule = input(
                                "How much ridicule is this message show? (0/10): ")
                            ridicule = int(ridicule)
                            if (ridicule > 0 or ridicule == 0) and (ridicule < 10 or ridicule == 10):
                                input_error = False
                            else:
                                print("Out of range, please check what you type")
                                input_error = True

                        input_error = True
                        while input_error:
                            ask = input(
                                "Do you think this message wants ask a question? (0/10, 10 = 100%): ")
                            ask = int(ask)
                            if (ask == 0 or ask > 0) and (ask == 10 or ask < 10):
                                input_error = False
                            else:
                                print("Out of range, please check what you type")
                                input_error = True
                        view_socre_show = pt.PrettyTable()
                        view_socre_show.field_names = [
                            'To socre on', 'Your socre']
                        view_socre_show.add_row(['postive', postive])
                        view_socre_show.add_row(['happiness', happiness])
                        view_socre_show.add_row(['admire', admire])
                        view_socre_show.add_row(['sadness', sadness])
                        view_socre_show.add_row(['angry', angry])
                        view_socre_show.add_row(['ridicule', ridicule])
                        view_socre_show.add_row(['is_ask', ask])
                        print("Please review the socre :")
                        print(view_socre_show)
                        input_retry = True
                        while input_retry:
                            retry_socre_input = input(
                                "Is your socre right? (y/n): ")
                            if retry_socre_input == 'Y' or retry_socre_input == 'N' or retry_socre_input == 'y' or retry_socre_input == 'n':
                                if retry_socre_input.upper() == "N":
                                    retry_flag = True
                                else:
                                    retry_flag = False
                            else:
                                print("Invalid input, Please type in y or n")
                                input_retry = True
                            input_retry = False

                        tag_coment_dict[reply_id] = {
                            'happiness': happiness, 'sadness': sadness, 'angry': angry, 'is_ask':ask, 'admire':admire}

            else:  # For normal mode
                os.system('cls')
                print('Progress : '+str(current_count)+'/'+str(all_count))
                retry_flag = True
                while retry_flag:
                    upper_tree_list = []
                    deep_search_dict = {}
                    message_dict = comment_data_dict[str(reply_id)]
                    current_message = message_dict['message']
                    current_reply_id = reply_id
                    current_root_rid = message_dict['root_rid']
                    if current_reply_id != str(current_root_rid) and str(current_root_rid) != 'N/A':
                        while str(current_root_rid) != current_reply_id and current_root_rid != 'N/A':
                            current_upper_rid = current_root_rid
                            upper_message_dict = comment_data_dict[str(
                                current_upper_rid)]
                            current_reply_id = current_upper_rid
                            upper_tree_list.append(
                                upper_message_dict['message'])
                            current_root_rid = upper_message_dict['root_rid']
                        print("Root Diaelog of current message:")
                        upper_message_show = pt.PrettyTable()
                        upper_message_show.field_names = [
                            '#', 'message']
                        message_index = 0
                        show_index = 1
                        for message_index in range(0, len(upper_tree_list)):
                            upper_message_show.add_row(
                                [str(show_index), upper_tree_list[len(upper_tree_list)-1-message_index]])
                            
                            show_index = show_index + 1
                        print(upper_message_show)
                        has_upper_message = True
                    else:
                        print(
                            "This is the root message, does not have any root dialog.")
                        has_upper_message = False
                    print('Current message :')
                    print(current_message)
                    deep_message_show = pt.PrettyTable()
                    deep_message_show.field_names = ['#', 'message']
                    deep_index = 0
                    for deep_search_rid in list(comment_data_dict.keys()):
                        deep_search_dict = comment_data_dict[str(
                            deep_search_rid)]
                        current_root_rid = deep_search_dict['root_rid']
                        if str(current_root_rid) == str(reply_id):
                            deep_index = deep_index + 1
                            deep_message_show.add_row(
                                [str(deep_index), deep_search_dict['message']])
                    print("Following replies: ")
                    print(deep_message_show)
                    print('Socre feeling:')
                    input_error = True
                    while input_error:
                        postive = input(
                            "Is message positive?(-1/1 , 1 is postive): ")
                        postive = int(postive)
                        if (postive > -1 or postive == -1) and (postive < 1 or postive == 1):
                            input_error = False
                        else:
                            print("Out of range, please check what you type")
                            input_error = True

                    input_error = True
                    while input_error:
                        happiness = input(
                            "How happy is this message? (0/10): ")
                        happiness = int(happiness)
                        if (happiness > 0 or happiness == 0) and (happiness < 10 or happiness == 10):
                            input_error = False
                        else:
                            print("Out of range, please check what you type")
                            input_error = True

                    input_error = True
                    while input_error:
                        admire = input(
                            "How much admire is this message show ? (0/10): ")
                        admire = int(admire)
                        if (admire > 0 or admire == 0) and (admire < 10 or admire == 10):
                            input_error = False
                        else:
                            print("Out of range, please check what you type")
                            input_error = True

                    input_error = True
                    while input_error:
                        sadness = input(
                            "How sad is this message? (0/10): ")
                        sadness = int(sadness)
                        if (sadness > 0 or sadness == 0) and (sadness < 10 or sadness == 10):
                            input_error = False
                        else:
                            print("Out of range, please check what you type")
                            input_error = True

                    input_error = True
                    while input_error:
                        angry = input(
                            "How angry is this message? (0/10): ")
                        angry = int(angry)
                        if (angry > 0 or angry == 0) and (angry < 10 or angry == 10):
                            input_error = False
                        else:
                            print("Out of range, please check what you type")
                            input_error = True

                    input_error = True
                    while input_error:
                        ridicule = input(
                            "How much ridicule is this message show? (0/10): ")
                        ridicule = int(ridicule)
                        if (ridicule > 0 or ridicule == 0) and (ridicule < 10 or ridicule == 10):
                            input_error = False
                        else:
                            print("Out of range, please check what you type")
                            input_error = True

                    input_error = True
                    while input_error:
                        ask = input(
                            "Do you think this message wants ask a question? (0/10, 10 = 100%): ")
                        ask = int(ask)
                        if (ask == 0 or ask > 0) and (ask == 10 or ask < 10):
                            input_error = False
                        else:
                            print("Out of range, please check what you type")
                            input_error = True
                    view_socre_show = pt.PrettyTable()
                    view_socre_show.field_names = [
                        'To socre on', 'Your socre']
                    view_socre_show.add_row(['postive', postive])
                    view_socre_show.add_row(['happiness', happiness])
                    view_socre_show.add_row(['admire', admire])
                    view_socre_show.add_row(['sadness', sadness])
                    view_socre_show.add_row(['angry', angry])
                    view_socre_show.add_row(['ridicule', ridicule])
                    view_socre_show.add_row(['is_ask', ask])
                    print("Please review the socre :")
                    print(view_socre_show)
                    input_retry = True
                    while input_retry:
                        retry_socre_input = input(
                            "Is your socre right? (y/n): ")
                        if retry_socre_input == 'Y' or retry_socre_input == 'N' or retry_socre_input == 'y' or retry_socre_input == 'n':
                            if retry_socre_input.upper() == "N":
                                retry_flag = True
                            else:
                                retry_flag = False
                        else:
                            print("Invalid input, Please type in y or n")
                            input_retry = True
                        input_retry = False

                    tag_coment_dict[reply_id] = {
                        'happiness': happiness, 'sadness': sadness, 'angry': angry, 'is_ask':ask, 'admire':admire}
        return tag_coment_dict
    except KeyboardInterrupt:
        print("Recive siginal to quit, please wait")
        return tag_coment_dict
    except :
        print("Error happened, quiting.")
        return tag_coment_dict



def comment_all_time_step_collect(all_timestep_comment_dict, timestep_key_add_mode, data_collect_keys_list, comment_data_dict):
    for timestep in all_timestep_comment_dict.keys():
        current_timestep_dict = all_timestep_comment_dict[str(timestep)]
        if comment_data_dict == None:
            comment_data_dict = {}
            result_key_commect_data_dict = {}
        for reply_id in current_timestep_dict.keys():
            if str(reply_id) not in comment_data_dict.keys():
                key_commect_data_dict = current_timestep_dict[str(reply_id)]
                comment_data_dict[str(reply_id)] = {}
                result_key_commect_data_dict = {}
                for key in data_collect_keys_list:
                    if timestep_key_add_mode:
                        time_pointer_dict = key_commect_data_dict[key]
                        if type(time_pointer_dict) == dict:
                            if 'last_time_step_pointer' in time_pointer_dict.keys():
                                target_timestep = time_pointer_dict['last_time_step_pointer']
                                old_key_commect_data_dict = all_timestep_comment_dict[str(
                                    target_timestep)]
                                old_key_commect_data_dict = old_key_commect_data_dict[str(
                                    reply_id)]
                                result_key_commect_data_dict[key] = old_key_commect_data_dict[key]
                            else:
                                result_key_commect_data_dict[key] = key_commect_data_dict[key]
                                comment_data_dict[str(
                                    reply_id)] = result_key_commect_data_dict
                        else:
                            result_key_commect_data_dict[key] = key_commect_data_dict[key]
                            comment_data_dict[str(
                                reply_id)] = result_key_commect_data_dict
                    else:
                        result_key_commect_data_dict[key] = key_commect_data_dict[key]
                        comment_data_dict[str(
                            reply_id)] = result_key_commect_data_dict
            result_key_commect_data_dict = result_key_commect_data_dict

    return comment_data_dict


def init_dec_enc_dict():
    # 0 is for data not found
    dec_dict = {0: 'N/A'}
    enc_dict = {'N/A': 0}
    return dec_dict, enc_dict


def message_encode_comment_dict(comment_data_dict, auto_update, enc_dict, dec_dict, encode_comment_dict, overwrite_flag, encode_contuine):
    # 管理编码字典
    if encode_comment_dict == None:
        encode_comment_dict = {}
    if enc_dict == None:
        enc_dict = {'N/A': 0}
    if dec_dict == None:
        dec_dict = {0: 'N/A'}

    for reply_id in comment_data_dict:
        if encode_contuine:
            if reply_id not in enc_dict.keys():
                encode_result = []
                encoding_message_dict = comment_data_dict[reply_id]
                encoding_message = encoding_message_dict['message']
                if str(reply_id) not in encode_comment_dict.keys():
                    for charater in encoding_message:
                        if str(charater) not in enc_dict.keys():
                            if auto_update:
                                new_index = len(enc_dict)
                                enc_dict[str(charater)] = new_index
                                dec_dict[str(new_index)] = charater
                                encode_result.append(new_index)
                            else:
                                encode_result.append(0)
                        else:
                            encode_result.append(enc_dict[str(charater)])
                    encode_comment_dict[str(reply_id)] = encode_result
                else:
                    if overwrite_flag:
                        if str(reply_id) not in encode_comment_dict.keys():
                            for charater in encoding_message:
                                if str(charater) not in enc_dict.keys():
                                    if auto_update:
                                        new_index = len(enc_dict)
                                        enc_dict[str(charater)] = new_index
                                        dec_dict[str(new_index)] = charater
                                    else:
                                        encode_result.append(0)
                                else:
                                    encode_result.append(
                                        enc_dict[str(charater)])
                        encode_comment_dict[str(reply_id)] = encode_result
        else:
            encode_result = []
            encoding_message_dict = comment_data_dict[reply_id]
            encoding_message = encoding_message_dict['message']
            if str(reply_id) not in encode_comment_dict.keys():
                for charater in encoding_message:
                    if str(charater) not in enc_dict.keys():
                        if auto_update:
                            new_index = len(enc_dict)
                            enc_dict[str(charater)] = new_index
                            dec_dict[str(new_index)] = charater
                            encode_result.append(new_index)
                        else:
                            encode_result.append(0)
                    else:
                        encode_result.append(enc_dict[str(charater)])
                encode_comment_dict[str(reply_id)] = encode_result
            else:
                if overwrite_flag:
                    if str(reply_id) not in encode_comment_dict.keys():
                        for charater in encoding_message:
                            if str(charater) not in enc_dict.keys():
                                if auto_update:
                                    new_index = len(enc_dict)
                                    enc_dict[str(charater)] = new_index
                                    dec_dict[str(new_index)] = charater
                                else:
                                    encode_result.append(0)
                            else:
                                encode_result.append(enc_dict[str(charater)])
                    encode_comment_dict[str(reply_id)] = encode_result

    return encode_comment_dict, dec_dict, enc_dict


try:
    
    # root_dir = 'E:\\爬虫\\test-data\\BV1JD4y1U72G'
    root_dir = 'E:\\爬虫\\test-data\\BV1UC4y1b7eG'
    dec_enc_dict_path = 'E:\\爬虫\\test-data\\dec-enc-dict'
    timestep_key_dire = True
    timestep_add_mode = True
    update_dict = True
    data_save_local = True
    tag_contune = True
    encode_contuine = True
    data_collect_keys_list = ['message', 'root_rid']
    
    os.chdir(dec_enc_dict_path)
    try:
        enc_dict_file = open('enc_dict.json', 'r', encoding='utf-8')
        dec_dict_file = open('dec_dict.json', 'r', encoding='utf-8')
        enc_dict = json.load(enc_dict_file)
        dec_dict = json.load(dec_dict_file)
    except:
        print("Could not read decode/encode dictionary")
        print("Create a new one")
    os.chdir(root_dir)
    try:
        encode_comment_dict_file = open(
            'encode_comment_dict.json', 'r', encoding='utf-8')
    except:
        print("Could not read encoded comment")
    tag_coment_dict = {}
    try:
        tag_coment_dict_file = open(
            'tag_coment_dict.json', 'r', encoding='utf-8')
        tag_coment_dict = json.load(tag_coment_dict_file)
        tag_coment_dict_file.close()
    except:
        tag_coment_dict = {}
        print("Could not read tag_coment_dict")
    if timestep_key_dire:
        all_time_step_comment_dict_file = open(
            'commits_dict_all_timestep.json', 'r', encoding='utf-8')
        all_time_step_user_dict_file = open(
            'user_dict_all_timestep.json', 'r', encoding='utf-8')
        all_time_step_user_dict = json.load(all_time_step_user_dict_file)
        all_time_step_comment_dict = json.load(all_time_step_comment_dict_file)
        all_time_step_comment_dict_file.close()
        all_time_step_user_dict_file.close()
    else:
        comment_dict_file = open('commits_dict.json', encoding='utf-8')
        user_dict_file = open('user_dict.json', encoding='utf-8')
        comment_dict = json.load(comment_dict_file)
    comment_data_dict = comment_all_time_step_collect(all_timestep_comment_dict=all_time_step_comment_dict,
                                                      timestep_key_add_mode=True, data_collect_keys_list=data_collect_keys_list, comment_data_dict=None)
    encode_comment_dict, dec_dict, enc_dict = message_encode_comment_dict(
        comment_data_dict=comment_data_dict, auto_update=True, enc_dict=None, dec_dict=None, encode_comment_dict=None, overwrite_flag=True, encode_contuine=encode_contuine)

    tag_coment_dict = comment_data_dict_tag(
        comment_data_dict, tag_contune, tag_coment_dict)
    tag_coment_dict_file = open('tag_coment_dict.json', 'w', encoding='utf-8')
    enc_dict_file = open('enc_dict.json', 'w', encoding='utf-8')
    dec_dict_file = open('dec_dict.json', 'w', encoding='utf-8')
    json.dump(enc_dict, enc_dict_file)
    json.dump(dec_dict, dec_dict_file)
    json.dump(tag_coment_dict, tag_coment_dict_file)
    enc_dict_file.close()
    dec_dict_file.close()
    tag_coment_dict_file.close()
    print("Write complete")
except KeyboardInterrupt:
    print("Recive a singal to quit, please wait")
    tag_coment_dict_file = open('tag_coment_dict.json', 'w', encoding='utf-8')
    enc_dict_file = open('enc_dict.json', 'w', encoding='utf-8')
    dec_dict_file = open('dec_dict.json', 'w', encoding='utf-8')
    json.dump(enc_dict, enc_dict_file)
    json.dump(dec_dict, dec_dict_file)
    json.dump(tag_coment_dict, tag_coment_dict_file)
    enc_dict_file.close()
    dec_dict_file.close()
    tag_coment_dict_file.close()
    print("Write complete")
except:
    print("Unkown Error")
    tag_coment_dict_file = open('tag_coment_dict.json', 'w', encoding='utf-8')
    enc_dict_file = open('enc_dict.json', 'w', encoding='utf-8')
    dec_dict_file = open('dec_dict.json', 'w', encoding='utf-8')
    json.dump(enc_dict, enc_dict_file)
    json.dump(dec_dict, dec_dict_file)
    json.dump(tag_coment_dict, tag_coment_dict_file)
    enc_dict_file.close()
    dec_dict_file.close()
    tag_coment_dict_file.close()
    print("Write complete")
