import prettytable as pt 
import json
import os


def dire_save():
    json.dump(enc, f)

def comment_data_dict_tag(comment_data_dict):
    feeling_dict = {}
    for reply_id in list(comment_data_dict.keys()):
        while retry_flag:
            upper_tree_list = []
            deep_search_dict = {}
            message_dict = comment_data_dict[str(reply_id)]
            current_message = message_dict['message']
            current_reply_id = reply_id
            current_root_rid = message_dict['root_rid']
            if current_reply_id != current_root_rid:
                while current_root_rid != current_reply_id:
                    current_upper_rid = current_root_rid
                    upper_message_dict = comment_data_dict[str(current_upper_rid)]
                    current_reply_id = current_upper_rid
                    upper_tree_list.append(upper_message_dict['message'])
                    current_root_rid = upper_message_dict['root_rid']
                    print("Root Diaelog of current message:")
                    upper_message_show = pt.PrettyTable()
                    upper_message_show.field_names = ['#', 'message']
                    show_index = 0 
                    for message_index in range(len(upper_tree_list), 0):
                        show_index = show_index + 1
                        upper_message_show.add_row([str(show_index), upper_tree_list[message_index]])
                    print(upper_message_show)
                    has_upper_message = True 
            else:
                print("This is the root message, does not have any root dialog.")
                has_upper_message = False
            print('Current message :')
            print(current_message)
            deep_message_show = pt.PrettyTable()
            deep_message_show.field_names[('#', 'message')]
            for deep_search_rid in list(comment_data_dict.keys()):
                deep_search_dict = comment_data_dict[str(deep_search_rid)]
                if current_root_rid == str(reply_id):
                    deep_index = deep_index + 1
                    deep_message_show.add_row([str(deep_index), deep_search_dict['message']])
            print("Following replies: ")
            print(deep_message_show)
            print('Socre feeling:')
            happiness = print("How happy is this message? (0/10): ")
            sadness = print("How sad is this message? (0/10): ")
            angry = print("How angry is this message? (0/10): ")
            view_socre_show = pt.PrettyTable()
            view_socre_show.field_names(['To socre on', 'Your socre'])
            view_socre_show.add_row(['happiness', happiness])
            view_socre_show.add_row(['sadness', sadness])
            view_socre_show.add_row(['angry', angry])
            print("Please review the socre :")
            print(view_socre_show)
            while retry_flag:
                retry_socre_input = input("Is your socre right? (y/n): ")
                if retry_socre_input == 'Y' or retry_socre_input == 'N' or retry_socre_input == 'y' or retry_socre_input == 'n': 
                    if retry_socre_input.upper() == "N" :
                        retry_flag = True
                else:
                    print("Invalid input, Please type in y or n")
                    input_retry = True 
        feeling_dict[str(reply_id)] = {'happiness':happiness, 'sadness':sadness, 'angry':angry}
    return feeling_dict

         



            


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


def message_encode_comment_dict(comment_data_dict, auto_update, enc_dict, dec_dict, encode_comment_dict, overwrite_flag):
    # 管理编码字典
    if encode_comment_dict == None:
        encode_comment_dict = {}
    if enc_dict == None :
        enc_dict = {'N/A': 0}
    if dec_dict == None :
        dec_dict = {0: 'N/A'}

        
    for reply_id in comment_data_dict:
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

    return encode_comment_dict,dec_dict, enc_dict


root_dir = 'E:\\爬虫\\test-data'
timestep_key_dire = True
timestep_add_mode = True
update_dict = True
data_save_local = True
data_collect_keys_list = ['message', 'root_rid']
os.chdir(root_dir)
if timestep_key_dire:
    all_time_step_comment_dict_file = open(
        'commits_dict_all_timestep.json', encoding='utf-8')
    all_time_step_user_dict_file = open(
        'user_dict_all_timestep.json', encoding='utf-8')
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
encode_comment_dict,dec_dict, enc_dict = message_encode_comment_dict(comment_data_dict = comment_data_dict, auto_update = True, enc_dict = None, dec_dict = None, encode_comment_dict = None, overwrite_flag = True)
enc_dict_file=open('enc_dict.json', 'w', encoding='utf-8')
dec_dict_file=open('dec_dict.json', 'w', encoding='utf-8')
json.dump(enc_dict, enc_dict_file)
json.dump(dec_dict, dec_dict_file)
enc_dict_file.close()
dec_dict_file.close()