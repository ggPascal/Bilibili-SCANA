from dict_dataset_maker import message_encode_comment_dict, comment_all_time_step_collect
import re
import os

video_data_rootdir = "E:\\爬虫\\test-data"
floder_walk = os.walk(video_data_rootdir)

for dirpath, current_floder_name, current_filename in floder_walk:
    if re.match('BV', current_floder_name) == None:
        continue
    current_floder = os.path.join(dirpath, floders_list)
    os.chdir(current_floder)

    # Self update the comment_data at first
    try:
        comment_data_dict_file = open(os.path.join(current_floder, comment_data_dict.json))
    except: 
        # Failed to load? create a new one
        try:
            current_all_timestep_comments_file = os.open(os.path.join(current_floder, 'commits_dict_all_timestep.json'))
        except:
            error_list.append(os.path.join(current_floder, 'commits_dict_all_timestep.json'))
    
    try:
        current_encoded_message_file = open(os.path.join(current_floder, 'encode_comment_dict.json'))
    except:
        
        current_all_timestep_comments = json.load(current_all_timestep_comments_file)
        
        comment_all_time_step_collect(all_timestep_comment_dict = current_all_timestep_comments, timestep_key_add_mode, data_collect_keys_list, comment_data_dict)    