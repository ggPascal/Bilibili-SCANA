
# PYCMS开发
# 本人初次开发爬虫工具，如果您有更好的建议，可以提出（当然语气请不要太激烈）
from api_commit_get import *

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import queue
import os
import re
import numba as nb
import traceback as tb

# Time step file is waiting for develoap done.
timestep_file = True
timestep_add_mode = False
timestep_key_dire = True
root_dir = "E:/爬虫/test-data/"
bvid_list = ['BV1JD4y1U72G', 'BV1ri4y1u7JR',
             'BV1av411v7E1', 'BV1UC4y1b7eG', 'BV1DC4y1b7UA']

if bvid_list == None:
    bvid_list.append(input("输入需要获取评论的BV号： "))

all_in_one = True
write_copy = False
write_copy_dict = True
continue_mode_enable = True

max_page_xpath = '//*[@id="comment"]/div[@class="common"]/div[@class="comment"]/div[@class="bb-comment "]/div[@class="bottom-page paging-box-big"]/div[@class="page-jump"]/span'
page_input = '//*[@id="comment"]/div[@class="common"]/div[@class="comment"]/div[@class="bb-comment "]/div[@class="bottom-page paging-box-big"]/div[@class="page-jump"]/input'
js = "window.scrollTo(0, document.body.scrollHeight)"
flag_upper_done_element = '/html/body/div[3]/div/div[1]/div[3]/div[1]/span[4]/i'
flag_upper_not_done_str = '--'
broswer_profile = "C:\\Users\\20363\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\jpuqy65r.default-release"

proxy_enable = True
requests = requests.session()
if proxy_enable:
    requests.verify = True
    proxies = {'http': 'socks5://127.0.0.1:9150',
               'https': 'socks5://127.0.0.1:9150'}

tor_proxy = False
if tor_proxy:
    import socket
    import socks
    import requests

    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
    socket.socket = socks.socksocket

for video_id in bvid_list:
    print('Now we are collecting information from '+video_id)
    try:
        os.chdir(root_dir + "/" + video_id)
    except:
        os.mkdir(root_dir + "/" + video_id)
        os.chdir(root_dir + "/" + video_id)

    if timestep_key_dire or timestep_add_mode:
        try:
            all_user_full_timestep_dict_file = open(
                'user_dict_all_timestep.json', 'r', encoding='utf-8')
            all_commit_full_timestep_dict_file = open(
                'commits_dict_all_timestep.json', 'r', encoding='utf-8')
            video_info_full_timestep_dire_file = open(
                'video_info_all_timestep.json', 'r', encoding='utf-8')
            video_info_full_timestep_dire = json.load(
                video_info_full_timestep_dire_file)
            all_user_full_timestep_dict = json.load(
                all_user_full_timestep_dict_file)
            all_commit_full_timestep_dict = json.load(
                all_commit_full_timestep_dict_file)
        except:
            print("Could not read dictory that contain full timestep")
            print('Disabling timestep add mode ')
            video_info_full_timestep_dire = {}
            all_user_full_timestep_dict = {}
            all_commit_full_timestep_dict = {}
            timestep_add_mode = False

    url = "https://www.bilibili.com/video/" + video_id  # BV装载

    if timestep_key_dire:
        continue_mode_enable = False

    fp = webdriver.FirefoxProfile(broswer_profile)

    browser = webdriver.Firefox(fp)
    browser.get(url)
    print("已获取链接，等待20秒，确保浏览器完成操作")

    upper_not_done = True
    while upper_not_done:  # 保证浏览器响应成功后再进行下一步操作
        try:
            upper_falg_str = browser.find_element_by_xpath(
                flag_upper_done_element).text
            if re.search(flag_upper_not_done_str, upper_falg_str):
                upper_not_done = True
            else:
                upper_not_done = False
        except:
            upper_not_done = True

    input_not_reached = True
    while input_not_reached:
        try:
            max_page_string = browser.find_element_by_xpath(
                max_page_xpath).text
            input_not_reached = False
        except:
            browser.execute_script(js)
    video_info_pipe = queue.Queue(0)

    def isElementExist(target_xpath):
        flag = True
        try:
            element = browser.find_element_by_xpath(target_xpath)
            return flag

        except:
            flag = False

    json_get_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + video_id
    oid_dire = requests.get(json_get_url)
    oid_dire = oid_dire.text
    video_stat_data = oid_dire
    oid_dire = json.loads(oid_dire)
    oid_dire = oid_dire['data']
    video_info_dire = video_info(video_data=oid_dire)
    video_oid = video_info_dire['video_oid']

    if continue_mode_enable:
        try:
            user_dict_file = open(file="user_dict.json",
                                  mode="r", encoding="utf-8")
            all_user_dict = json.load(user_dict_file)
        except:
            retry_flag = True
            while retry_flag:
                retry_input = input(
                    "Could not read user dictionary file, retry or use overwrite mode to collect user information? (R)etry/(O)ver-write:")
                if retry_input.upper() == "R":
                    retry_flag = True
                elif retry_input.upper() == "O":
                    all_user_dict = {}
                    over_write_user = True
                    retry_flag = False
                else:
                    print(
                        "Please check your input, 'R' for retry, 'O' for overwrite-mode")
                    retry_flag = True
        try:
            commit_dict_file = open(file="commits_dict.json",
                                    mode="r", encoding="utf-8")
            all_commit_direct = json.load(commit_dict_file)
        except:
            retry_flag = True
            while retry_flag:
                retry_input = input(
                    "Could not read comments dictionary file, retry or use overwrite mode to collect comments information? (R)etry/(O)ver-write:")
                if retry_input.upper() == "R":
                    retry_flag = True
                elif retry_input.upper() == "O":
                    over_write_comment = True
                    all_commit_direct = {}
                else:
                    print(
                        "Please check your input, 'R' for retry, 'O' for overwrite-mode")
                    retry_flag = True
        try:
            video_info_dict_file = open(
                file="video_info.json", mode="r", encoding="utf-8")
            last_video_info_dire = json.load(video_info_dict_file)
        except:
            retry_flag = True
            while retry_flag:
                retry_input = input(
                    "Could not read video info file for verify , retry or use coutine mode without check video object id? (R)etry/(W)ith-out-verify:")
                if retry_input.upper() == "R":
                    retry_flag = True
                elif retry_input.upper() == "O":
                    last_video_info_dire = None
                    retry_flag = False
                else:
                    print(
                        "Please check your input, 'R' for retry, 'W' for without verify")
                    retry_flag = True
    else:
        all_user_dict, all_commit_direct = init()

    if continue_mode_enable and last_video_info_dire != None:
        if continue_mode_enable and video_oid != last_video_info_dire['video_oid']:
            print("Video oject id not match , switch into overwrite mode")
            continue_mode_enable = False
    else:
        continue_mode_enable = False

    max_page = int(max_page_string)
    page = 1
    print("共计有" + max_page_string + "页")
    # 初始化结束
    print("开始爬取")
    # Thru all page to get data

    while page < max_page or page == max_page:
        try:
            print("正在爬取" + str(page) + "/"+str(max_page) + "页")

            json_get_url = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn=' + \
                str(page)+'&type=1&oid='+str(video_oid)
            os.chdir(root_dir)
            # time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime())+' '+
            if timestep_file:
                json_path = str(page)+'_'+str(time.time() * 10000000)+'.json'
            else:
                json_path = str(page)+'.json'
            video_commits_data = requests.get(json_get_url).text

            video_commits_data_byte = video_commits_data.encode('utf-8')
            video_commits_data = json.loads(video_commits_data)
            # TODO:一体化入库函数
            if all_in_one and page == 1:
                all_commit_direct, all_user_dict = commit_json_ana(continue_mode_enable=continue_mode_enable, f=None, is_file=False, page_init=True, json_data=video_commits_data,
                                                                all_commit_direct=all_commit_direct, all_user_dict=all_user_dict, video_oid=video_oid, timestep_file=timestep_file, timestep_add_mode=timestep_add_mode, timestep_key_dire=timestep_key_dire, all_user_full_timestep_dict=all_user_full_timestep_dict, all_commit_full_timestep_dict=all_commit_full_timestep_dict)
                # 写入数据库
            if all_in_one and page > 1:
                all_commit_direct, all_user_dict = commit_json_ana(continue_mode_enable=continue_mode_enable, f=None, is_file=False, page_init=False, json_data=video_commits_data,
                                                                all_commit_direct=all_commit_direct, all_user_dict=all_user_dict, video_oid=video_oid, timestep_file=timestep_file, timestep_add_mode=timestep_add_mode, timestep_key_dire=timestep_key_dire, all_user_full_timestep_dict=all_user_full_timestep_dict, all_commit_full_timestep_dict=all_commit_full_timestep_dict)
                # 写入数据库

            if write_copy:
                f = open(file=str(json_path), mode="wb")
                json_data = video_commits_data_byte
                f.write(json_data)
                f.close()
                print('写入成功')
                # 关闭文件
                f.close()

            # ————————————————
            # 版权声明：本文为CSDN博主「achiv」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
            # 原文链接：https://blog.csdn.net/qq_37088317/java/article/details/89363381
            page = page + 1
        except KeyboardInterrupt :
            print("recive siginal to quit")
            print("Saving data")
            break
        except :
            print("An error occurred, quitting")
            break

    if write_copy_dict:
        # TODO: add a way to write file using bvid+timestep as name to sprate time step
        user_dict_file = open(file="user_dict.json",
                              mode="w", encoding="utf-8")
        commit_dict_file = open(file="commits_dict.json",
                                mode="w", encoding="utf-8")
        video_info_dict_file = open(
            file="video_info.json", mode="w", encoding="utf-8")
        if timestep_key_dire:
            user_dict_file = open(file="user_dict_all_timestep.json",
                                  mode="w", encoding="utf-8")
            commit_dict_file = open(file="commits_dict_all_timestep.json",
                                    mode="w", encoding="utf-8")
            video_info_dict_file = open(
                file="video_info_all_timestep.json", mode="w", encoding="utf-8")
            # bilibil timestep example : 1595802663523
            save_time_step = str(int(round(time.time() * 1000)))
            all_user_full_timestep_dict[save_time_step] = all_user_dict
            all_commit_full_timestep_dict[save_time_step] = all_commit_direct
            video_info_full_timestep_dire[save_time_step] = video_info_dire
            json.dump(all_user_full_timestep_dict, user_dict_file)
            json.dump(all_commit_full_timestep_dict, commit_dict_file)
            json.dump(video_info_full_timestep_dire, video_info_dict_file)
        else:
            json.dump(all_user_dict, user_dict_file)
            json.dump(all_commit_direct, commit_dict_file)
            json.dump(video_info_dire, video_info_dict_file)
        user_dict_file.close()
        commit_dict_file.close()
        video_info_dict_file.close()
        print("Write completed")


print("爬取结束")
