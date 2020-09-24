def load_arry_data(load_arry_data_container):
    import numpy as np
    import os
    try:
        os.chdir(load_arry_data_container.data_root_dir)
        all_in_one_data = np.load(load_arry_data_container.all_in_one_data_filename)
    except:
        load_arry_data_container.error_while_loading_data = True
        exit(),
    
    if load_arry_data_container.make_new_data_flag == False:
        train_up_arry = all_in_one_data['train_up_arry']
        train_down_arry = all_in_one_data['train_down_arry']
        train_target_arry = all_in_one_data['train_target_arry']

        load_arry_data_container.train_up_arry = train_up_arry
        load_arry_data_container.train_down_arry = train_down_arry
        load_arry_data_container.train_target_arry = train_target_arry

        if load_arry_data_container.test_accuray_flag:
            test_up_arry = all_in_one_data['test_up_arry']
            test_down_arry = all_in_one_data['test_down_arry']
            test_target_arry = all_in_one_data['test_target_arry']
            test_target_orinal_arry = all_in_one_data['test_target_orianl_arry']
            maxium_legth = all_in_one_data['maxium_legth']
            maxium_legth = maxium_legth.tolist()
            max_enc_index = all_in_one_data['max_enc_index']
            max_enc_index = max_enc_index.tolist()

            load_arry_data_container.test_up_arry = test_up_arry
            load_arry_data_container.test_down_arry = test_down_arry
            load_arry_data_container.test_target_arry = test_target_arry
            load_arry_data_container.test_target_orinal_arry = test_target_orinal_arry
            load_arry_data_container.maxium_legth = maxium_legth
            load_arry_data_container.max_enc_index = max_enc_index
        
        if load_arry_data_container.make_new_model_flag:
            maxium_legth = all_in_one_data['maxium_legth']
            max_enc_index = all_in_one_data['max_enc_index']
            maxium_legth = maxium_legth.tolist()
            max_enc_index = max_enc_index.tolist()

            load_arry_data_container.maxium_legth = maxium_legth
            load_arry_data_container.max_enc_index = max_enc_index
    return load_arry_data_container

def load_tagged_data(load_tagged_data_container):
    import os
    import numpy as np
    os.chdir(load_tagged_data_container.data_root_dir)
    try:
        tagged_data_all_in_one = np.load(load_tagged_data_container.tagged_data_all_in_one_filename, allow_pickle=True)
    except:
        load_tagged_data_container.error_while_loading_data = True
        exit()
    maxium_legth = tagged_data_all_in_one['maxium_legth']
    maxium_legth = maxium_legth.tolist()
    max_enc_index = tagged_data_all_in_one['max_enc_index']
    max_enc_index = max_enc_index.tolist()

    train_up_list = tagged_data_all_in_one['tagged_data_train_up_arry']
    train_down_list = tagged_data_all_in_one['tagged_data_train_down_arry']
    train_target_list = tagged_data_all_in_one['tagged_data_train_target_arry']

    train_up_list = train_up_list.tolist()
    train_down_list = train_down_list.tolist()
    train_target_list = train_target_list.tolist()

    val_up_list = tagged_data_all_in_one['tagged_data_val_up_arry']
    val_down_list = tagged_data_all_in_one['tagged_data_val_down_arry']
    val_target_list = tagged_data_all_in_one['tagged_data_val_target_arry']

    val_up_list = val_up_list.tolist()
    val_down_list = val_down_list.tolist()
    val_target_list = val_target_list.tolist()

    load_tagged_data_container.maxium_legth = maxium_legth
    load_tagged_data_container.max_enc_index = max_enc_index
    load_tagged_data_container.train_up_list = train_up_list
    load_tagged_data.train_target_list = train_target_list
    load_tagged_data.train_down_list = train_down_list
    load_tagged_data_container.val_up_list = val_up_list
    load_tagged_data_container.val_down_list = val_down_list
    load_tagged_data_container.val_target_list = val_target_list

    if load_tagged_data_container.test_tagged_data_accuray_flag or load_tagged_data_container.show_tagged_data_predict_output_flag:
        test_up_list = tagged_data_all_in_one['tagged_data_test_up_arry']
        test_down_list = tagged_data_all_in_one['tagged_data_test_down_arry']
        test_target_list = tagged_data_all_in_one['tagged_data_test_target_arry']

        test_up_list = test_up_list.tolist()
        test_down_list = test_down_list.tolist()
        test_target_list = test_target_list.tolist()

        load_tagged_data_container.test_up_list = test_up_list
        load_tagged_data_container.test_down_list = test_down_list
        load_tagged_data_container.test_target_list = test_target_list

    return load_tagged_data_container

def load_model_data(load_model_data_container):
    import os
    from keras.models import load_model

    try:
        os.chdir(load_model_data_container.model_root_path)
        model_file_name = os.path.join(load_model_data_container.model_root_path, load_tagged_data_container.model_file_name)
        model = load_model(model_file_name, custom_objects={'r2': r2})
        load_model_data_container.model = model
    except:
        load_model_data_container.worng_while_loading = True
        exit()
    return load_model_data_container

def make_new_data(make_new_data_data_container):
    if make_new_data_data_container.merged_data_flag == False:
        try:
            encode_comment_dict_file = open(make_new_data_data_container.encode_comment_dict_file_name, 'r', encoding='utf-8')
        except:
            make_new_data_data_container.error_while_loading_data = True
            exit()
    else:
        try:
            merged_encode_comment_dict_file = open(make_new_data_data_container.merged_encode_comment_dict_filename, 'r', encoding='uft-8')
        except:
            make_new_data_data_container.error_while_loading_data = True
            
