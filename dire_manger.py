import keras
import json


def dire_save():
    json.dump(enc, f)


def update_dire(text):
    # 管理编码字典
    for charater in text:
        if charater not in enc.keys():
            new_index = len(enc)
            enc[str(charater)] = new_index
            dec[str(new_index)] = charater


def build_commit_dictory():
    # 使用RID作为主键
    if member_uid not in all_user_dict.keys():
        commit_user_info = {
            'user_name': user_name,
            'sign': sign,
            'avatar_image_address': avatar_adress,
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
            'vip_due_timestep': vip_due_timestep,
        }
        all_user_dict[member_id] = commit_user_info  # uid作为键
    if reply_id not in all_commit_direct.keys():
        commit_info = {
            'uid': member_id,
            'time': post_time_step,
            'like_number': like_number,
            'message': message,
            'has_replies': has_replies,
            'root_rid': root_rid,
            'is_top': is_top,
            'collect_time': collect_time_step
        }
        all_commit_direct[reply_id] = commit_info
    return all_commit_direct ,all_user_dict
