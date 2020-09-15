
# PYCMS开发
# 本人初次开发爬虫工具，如果您有更好的建议，可以提出（当然语气请不要太激烈）

# The note will be comment the code at below one line
# Example:
# # SOME note
# The code that note are saying

from .api_commit_get import *

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import queue
import os
import re
import traceback as tb
from multiprocessing import Pool
import queue
import json 

# Time step file is waiting for develoap done.
timestep_file = False
# This options will let program use a pointer to deal with same data in pervious timestep
timestep_add_mode = True
# This option will let all timestep data write into a singal dictionary file
timestep_key_dire = True

# floder you want to stroge data
root_dir = "E:/爬虫/test-data/"
bvid_list = ['BV1JD4y1U72G', 'BV1ri4y1u7JR',
             'BV1av411v7E1', 'BV1UC4y1b7eG', 'BV1DC4y1b7UA', 'BV1Gf4y19773', 'BV15h411Z7N1', 'BV1Ht4y1D7QX', 'BV1vE411T7Xb', 'BV1ZE411E7P5']
#
#bvid_list = ['BV1UC4y1b7eG', 'BV1DC4y1b7UA']
sleep_seconds = 300

if bvid_list == None:
    bvid_list.append(input("输入需要获取评论的BV号： "))

# All in one processs, default to set enable(unless you want to use in module way)
# Module way will be avabile in future
all_in_one = True
# Write each page's raw json data to file
write_copy = False
# Write dictionary result data to file
write_copy_dict = True
# recover from last position
continue_mode_enable = True

# xpath to get the data
max_page_xpath = '//*[@id="comment"]/div[@class="common"]/div[@class="comment"]/div[@class="bb-comment "]/div[@class="bottom-page paging-box-big"]/div[@class="page-jump"]/span'
page_input = '//*[@id="comment"]/div[@class="common"]/div[@class="comment"]/div[@class="bb-comment "]/div[@class="bottom-page paging-box-big"]/div[@class="page-jump"]/input'
# JS to scroll to bottom
js = "window.scrollTo(0, document.body.scrollHeight)"
# This flag is use to automatically sure thr page is done, still testing
flag_upper_done_element = '/html/body/div[3]/div/div[1]/div[3]/div[1]/span[4]/i'
flag_upper_not_done_str = '--'
# This profile can make sure every selenium browser has same configuration
broswer_profile = "C:\\Users\\20363\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\jpuqy65r.default-release"

# Proxy settings to avoid ip control
proxy_enable = True
def initlyze_request_session():
    import requests
    requests = requests.session()
    if proxy_enable:
        requests.verify = True
        proxies = {'http': 'socks5://127.0.0.1:9150',
                'https': 'socks5://127.0.0.1:9150'}



def main_collect_process(video_id, root_dir, timestep_key_dire, timestep_add_mode, all_user_full_timestep_dict_file_name, all_commit_full_timestep_dict_file_name, video_info_full_timestep_dire_file_name):
    
    print('Now we are collecting information from '+video_id)

    
    # Smart create a new floder to contain data if the floder is not exits
    try:
        print("Found exit floder")
        os.chdir(os.path.join(root_dir, video_id))
    except:
        print("Createing floder")
        os.mkdir(os.path.join(root_dir, video_id))
        os.chdir(os.path.join(root_dir, video_id))

    
    # Load files that is nedded for timestep kind mode
    if timestep_key_dire or timestep_add_mode:
        try:
            all_user_full_timestep_dict_file = open(
                os.path.join(root_dir, all_user_full_timestep_dict_file_name), 'r', encoding='utf-8')
            all_commit_full_timestep_dict_file = open(
                os.path.join(root_dir, all_commit_full_timestep_dict_file_name), 'r', encoding='utf-8')
            video_info_full_timestep_dire_file = open(
                os.path.join(root_dir, video_info_full_timestep_dire_file_name), 'r', encoding='utf-8')
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

    # Build up the URL address
    url = "https://www.bilibili.com/video/" + video_id

    # timestep_key_dire mode will write each timestep as a file, no need to use contuine mode
    if timestep_key_dire:
        continue_mode_enable = False

    fp = webdriver.FirefoxProfile(broswer_profile)

    browser = webdriver.Firefox(fp)
    browser.get(url)
    print("已获取链接，等待20秒，确保浏览器完成操作")

    # Smart waiting fuction for waiting upper part done
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

    # Scroll down to bottom
    input_not_reached = True
    while input_not_reached:
        try:
            max_page_string = browser.find_element_by_xpath(
                max_page_xpath).text
            input_not_reached = False
        except:
            browser.execute_script(js)
    video_info_pipe = queue.Queue(0)


    json_get_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + video_id
    oid_dire = requests.get(json_get_url)
    oid_dire = oid_dire.text
    video_stat_data = oid_dire
    oid_dire = json.loads(oid_dire)
    oid_dire = oid_dire['data']
    video_info_dire = video_info(video_data=oid_dire)
    video_oid = video_info_dire['video_oid']

    # Make sure all continue mode data is currect
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

    # Failed safe for case of can not read video info
    if continue_mode_enable and last_video_info_dire != None:
        # Failed safe for case of video info is currect
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
    # Start to get the data
    ssl_retry = True
    def page_collect_process(page):
        try:
            print("正在爬取" + str(page) + "/"+str(max_page) + "页")

            json_get_url = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn=' + \
                str(page)+'&type=1&oid='+str(video_oid)
            # time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime())+' '+
            if timestep_file:
                # Convert timestep to bilibili server format, this will use muilt times
                json_path = str(page)+'_'+str(time.time() * 10000000)+'.json'
            else:
                json_path = str(page)+'.json'
            video_commits_data = requests.get(json_get_url).text

            video_commits_data_byte = video_commits_data.encode('utf-8')
            video_commits_data = json.loads(video_commits_data)
            # First collect, will include the hot comments and top comments
            if all_in_one and page == 1:
                all_commit_direct, all_user_dict = commit_json_ana(continue_mode_enable=continue_mode_enable, f=None, is_file=False, page_init=True, json_data=video_commits_data,
                                                                    all_commit_direct=all_commit_direct, all_user_dict=all_user_dict, video_oid=video_oid, timestep_file=timestep_file, timestep_add_mode=timestep_add_mode, timestep_key_dire=timestep_key_dire, all_user_full_timestep_dict=all_user_full_timestep_dict, all_commit_full_timestep_dict=all_commit_full_timestep_dict)
                # 写入数据库
            # This collect will not collect hot comments and top comments, these data is repeated in the data of fllowing pages
            if all_in_one and page > 1:
                all_commit_direct, all_user_dict = commit_json_ana(continue_mode_enable=continue_mode_enable, f=None, is_file=False, page_init=False, json_data=video_commits_data,
                                                                    all_commit_direct=all_commit_direct, all_user_dict=all_user_dict, video_oid=video_oid, timestep_file=timestep_file, timestep_add_mode=timestep_add_mode, timestep_key_dire=timestep_key_dire, all_user_full_timestep_dict=all_user_full_timestep_dict, all_commit_full_timestep_dict=all_commit_full_timestep_dict)
                # 写入数据库
            # Copy wirte for write_copy mode
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

        # Deal with Keyboard Quit Signal
        except KeyboardInterrupt:
            print("recive siginal to quit")
            print("Saving data")
            

        # Deal with Connection Aborted
        except ConnectionAbortedError:
            print("connection lost, waiting for "+sleep_seconds+" seconds")
            time.sleep(sleep_seconds)
            ssl_retry = True

        # Deal with other errors (Now just restart the pages)
        except:
            print("An error occurred, quitting")
            time.sleep(sleep_seconds)
            ssl_retry = True

    while page < max_page or page == max_page and ssl_retry:
        page_collect_process(page)
        
# Wirte result dictonary to file
if write_copy_dict:
    # TODO: add a way to write file using bvid+timestep as name to sprate time step

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
        user_dict_file = open(file="user_dict.json",
                                mode="w", encoding="utf-8")
        commit_dict_file = open(file="commits_dict.json",
                                mode="w", encoding="utf-8")
        video_info_dict_file = open(
            file="video_info.json", mode="w", encoding="utf-8")
        json.dump(all_user_dict, user_dict_file)
        json.dump(all_commit_direct, commit_dict_file)
        json.dump(video_info_dire, video_info_dict_file)
    user_dict_file.close()
    commit_dict_file.close()
    video_info_dict_file.close()
    print("Write completed")


print("爬取结束")
