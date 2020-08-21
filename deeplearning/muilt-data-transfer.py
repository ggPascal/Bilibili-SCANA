from dict_dataset_maker import message_encode_comment_dict, comment_all_time_step_collect
import re
import os
import json

timestep_key_add_mode = True
use_bvid_key = True
data_collect_keys_list = ['message', 'root_rid']
video_data_rootdir = "E:\\爬虫\\test-data"
enc_dec_dict_root_path = "E:\\爬虫\\test-data\\dec-enc-dict"
merged_data_root_path = "E:\\爬虫\\test-data\\merged-data"
error_list = []
merged_comment_data_dict = {}
merged_encode_comment_dict = {}

floder_walk = os.walk(video_data_rootdir, topdown=False)
if use_bvid_key == False :
    index = 1

for dirpath, floder_names, current_filename in floder_walk:
    for current_floder_name in floder_names:
        if re.match('BV', current_floder_name) == None:
            continue
        current_floder = os.path.join(dirpath, current_floder_name)
        os.chdir(current_floder)

        # Self update the comment_data at first
        try:
            current_comment_data_dict_file = open(os.path.join(
                current_floder, "comment_data_dict.json"))
            current_comment_data_dict = json.load(current_comment_data_dict_file)
            current_comment_data_dict_file.close()
        except:
            # Failed to load? create a new comment_data_dict
            try:
                current_all_timestep_comments_file = open(
                    os.path.join(current_floder, 'commits_dict_all_timestep.json'))
                current_all_timestep_comments_dict = json.load(current_all_timestep_comments_file)
                
            except:
                # Skip this file
                error_list.append(os.path.join(
                    current_floder, 'commits_dict_all_timestep.json'))
                continue
            
            current_comment_data_dict = comment_all_time_step_collect(all_timestep_comment_dict=current_all_timestep_comments_dict,
                                                                    timestep_key_add_mode=True, data_collect_keys_list=data_collect_keys_list, comment_data_dict=None)
        if use_bvid_key:
            merged_comment_data_dict[str(current_floder_name)] =current_comment_data_dict
        else:
            merged_comment_data_dict[str(index)] = current_comment_data_dict

        # Self up encode comment and encode
        try:
            current_encode_comment_dict_file = open(os.path.join(
                current_floder, 'encode_comment_dict.json'))
            current_encode_comment_dict = json.load(
                current_encode_comment_dict_file)

            current_encode_comment_dict_file.close()
        except:
            current_encode_comment_dict = {}

        try:
            enc_dict_file = open(os.path.join(
                enc_dec_dict_root_path, 'enc_dict.json'))
            dec_dict_file = open(os.path.join(
                enc_dec_dict_root_path, 'dec_dict.json'))
            enc_dict = json.load(enc_dict_file)
            dec_dict = json.load(dec_dict_file)
        except:
            enc_dict = {}
            dec_dict = {}

        
        current_encode_comment_dict, dec_dict, enc_dict = message_encode_comment_dict(
            comment_data_dict=current_comment_data_dict, auto_update=True, enc_dict=enc_dict, dec_dict=dec_dict, encode_comment_dict=current_encode_comment_dict, overwrite_flag=False, encode_contuine=True)
        if use_bvid_key:
            merged_encode_comment_dict[str(current_floder_name)] = current_encode_comment_dict
        else:
            merged_encode_comment_dict[str(index)] = current_encode_comment_dict
        if use_bvid_key == False:
            index += 1

merged_encode_comment_dict_file = open(os.path.join(merged_data_root_path, 'merged_encode_comment_dict.json'), 'w', encoding='utf-8')
merged_comment_data_dict_file = open(os.path.join(merged_data_root_path, 'merged_comment_data_dict.json'), 'w', encoding='utf-8')

json.dump(merged_encode_comment_dict, merged_encode_comment_dict_file)
json.dump(merged_comment_data_dict, merged_comment_data_dict_file)

if error_list != [] :
    print('During merge, we found theses errors')
    print(error_list)