import keras
import json
import os


def dire_save():
    json.dump(enc, f)

def comment_all_time_step_collect(all_timestep_comment_dict, timestep_key_add_mode, data_collect_keys_list,comment_data_dict):
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
                                old_key_commect_data_dict = all_timestep_comment_dict[str(target_timestep)]
                                old_key_commect_data_dict = old_key_commect_data_dict[str(reply_id)]
                                result_key_commect_data_dict[key] = old_key_commect_data_dict[key]
                            else:
                                result_key_commect_data_dict[key] = key_commect_data_dict[key]
                                comment_data_dict[str(reply_id)] = result_key_commect_data_dict
                        else:
                            result_key_commect_data_dict[key] = key_commect_data_dict[key]
                            comment_data_dict[str(reply_id)] = result_key_commect_data_dict
                    else:
                        result_key_commect_data_dict[key] = key_commect_data_dict[key]
                        comment_data_dict[str(reply_id)] = result_key_commect_data_dict
            result_key_commect_data_dict = result_key_commect_data_dict
            
    return comment_data_dict

def init_dec_enc_dict():
    # 0 is for data not found
    dec_dict = {0: 'N/A'}
    enc_dict = {'N/A': 0}
    return dec_dict, enc_dict

def message_encode_comment_dict(comment_data_dict,auto_update, enc_dict, dec_dict, encode_comment_dict):
    # 管理编码字典
    if encode_comment_dict == None:
        encode_comment_dict = {}
    for reply_id in comment_data_dict:
        encode_result = []
        encoding_message = comment_data_dict[reply_id]
        if str(reply_id) not in encode_comment_dict.keys() and overwrite_flag:
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
    return encode_comment_dict     

root_dir = 'E:\\爬虫\\test-data'
timestep_key_dire = True
timestep_add_mode = True
update_dict = True 
data_save_local = True
data_collect_keys_list = ['message', 'root_rid']
os.chdir(root_dir)
if timestep_key_dire:
    all_time_step_comment_dict_file= open('commits_dict_all_timestep.json', encoding='utf-8')
    all_time_step_user_dict_file= open('user_dict_all_timestep.json', encoding='utf-8')
    all_time_step_user_dict = json.load(all_time_step_user_dict_file)
    all_time_step_comment_dict = json.load(all_time_step_comment_dict_file)
    all_time_step_comment_dict_file.close()
    all_time_step_user_dict_file.close()
else:
    comment_dict_file = open('commits_dict.json', encoding='utf-8')
    user_dict_file = open('user_dict.json', encoding='utf-8')
    comment_dict = json.load(comment_dict_file)
comment_all_time_step_collect(all_timestep_comment_dict=all_time_step_comment_dict, timestep_key_add_mode=True, data_collect_keys_list=data_collect_keys_list, comment_data_dict=None)

