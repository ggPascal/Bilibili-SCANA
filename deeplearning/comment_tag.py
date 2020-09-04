from dict_dataset_maker import * 
try:

    # root_dir = 'E:\\爬虫\\test-data\\BV1JD4y1U72G'
    root_dir = 'E:\\爬虫\\test-data\\BV1av411v7E1'
    dec_enc_dict_path = 'E:\\爬虫\\test-data\\dec-enc-dict'

    # means the directory is recording all timestep
    timestep_key_dire = True
    # means the directory is use pointer to avoid repeat data
    timestep_add_mode = True
    # means if you want to update the encode dictionary or decode dictionary
    update_dict = True
    # Save data to file (If you use my deeplearning tools, you should set it to True)
    data_save_local = True
    # Coutuine tag the data from last position
    tag_contune = True
    # Coutuine encode data from last position
    encode_contuine = True

    # the keys to collect data
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

    # Collect the data you want
    comment_data_dict = comment_all_time_step_collect(all_timestep_comment_dict=all_time_step_comment_dict,
                                                      timestep_key_add_mode=True, data_collect_keys_list=data_collect_keys_list, comment_data_dict=None)
    # Encode the message data
    # TODO: Change to optional choice based on data collect type
    encode_comment_dict, dec_dict, enc_dict = message_encode_comment_dict(
        comment_data_dict=comment_data_dict, auto_update=True, enc_dict=None, dec_dict=None, encode_comment_dict=None, overwrite_flag=True, encode_contuine=encode_contuine)

    # Tag the comment data
    tag_coment_dict = comment_data_dict_tag(
        comment_data_dict, tag_contune, tag_coment_dict)

    # Wirte comment data to local file.
    tag_coment_dict_file = open('tag_coment_dict.json', 'w', encoding='utf-8')
    encode_commecnt_dict_file = open(
        'encode_comment_dict.json', 'w', encoding='utf-8')
    json.dump(tag_coment_dict, tag_coment_dict_file)
    json.dump(encode_comment_dict, encode_commecnt_dict_file)
    tag_coment_dict_file.close()
    encode_commecnt_dict_file.close()

    # Write decode dictionary and encode dictionary data to file
    os.chdir(dec_enc_dict_path)
    enc_dict_file = open('enc_dict.json', 'w', encoding='utf-8')
    dec_dict_file = open('dec_dict.json', 'w', encoding='utf-8')
    json.dump(enc_dict, enc_dict_file)
    json.dump(dec_dict, dec_dict_file)
    enc_dict_file.close()
    dec_dict_file.close()

    print("Write complete")

# Deal with Keyboard Quit Signal
except KeyboardInterrupt:
    print("Recive a singal to quit, please wait")
    tag_coment_dict_file = open('tag_coment_dict.json', 'w', encoding='utf-8')
    encode_commecnt_dict_file = open(
        'encode_comment_dict.json', 'w', encoding='utf-8')
    json.dump(tag_coment_dict, tag_coment_dict_file)
    json.dump(encode_comment_dict, encode_commecnt_dict_file)
    tag_coment_dict_file.close()
    encode_commecnt_dict_file.close()

    os.chdir(dec_enc_dict_path)
    enc_dict_file = open('enc_dict.json', 'w', encoding='utf-8')
    dec_dict_file = open('dec_dict.json', 'w', encoding='utf-8')
    json.dump(enc_dict, enc_dict_file)
    json.dump(dec_dict, dec_dict_file)
    enc_dict_file.close()
    dec_dict_file.close()

    print("Write complete")

# Deal with unkown errors
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