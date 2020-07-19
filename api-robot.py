
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



broswer_profile = "C:\\Users\\20363\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\jpuqy65r.default-release"
video_id = input("输入需要获取评论的BV号： ")
url = "https://www.bilibili.com/video/" + video_id  # BV装载

all_in_one = True
write_copy = False
write_copy_dict = True
root_dir = "E:/爬虫/test-data/"
fp = webdriver.FirefoxProfile(broswer_profile)

max_page_xpath = '//*[@id="comment"]/div[@class="common"]/div[@class="comment"]/div[@class="bb-comment "]/div[@class="bottom-page paging-box-big"]/div[@class="page-jump"]/span'
page_input = '//*[@id="comment"]/div[@class="common"]/div[@class="comment"]/div[@class="bb-comment "]/div[@class="bottom-page paging-box-big"]/div[@class="page-jump"]/input'
js = "window.scrollTo(0, document.body.scrollHeight)"
flag_upper_done_element = '/html/body/div[3]/div/div[1]/div[3]/div[1]/span[4]/i'
flag_upper_not_done_str = '--'
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
while input_not_reached :
    try:
        max_page_string = browser.find_element_by_xpath(max_page_xpath).text
        input_not_reached = False
    except :
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
video_info_dire=video_info(video_data=oid_dire)
video_oid = video_info_dire['video_oid']

max_page = int(max_page_string)
page = 1
print("共计有" + max_page_string + "页")
# 初始化结束
print("开始爬取")
# Thru all page to get data
all_user_dict, all_commit_direct = init()
while page < max_page or page == max_page:
    try:
        print("正在爬取" + str(page) + "/"+str(max_page) + "页")
        
        json_get_url = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn=' + \
            str(page)+'&type=1&oid='+str(video_oid)
        os.chdir(root_dir)
        # time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime())+' '+
        json_path = str(page)+'.json'
        video_commits_data = requests.get(json_get_url).text

        video_commits_data_byte = video_commits_data.encode('utf-8')
        video_commits_data = json.loads(video_commits_data)
        # TODO:一体化入库函数
        if all_in_one and page == 1 :
            all_commit_direct, all_user_dict = commit_json_ana(f=None, is_file=False, page_init=True, json_data=video_commits_data,
                                                            all_commit_direct=all_commit_direct, all_user_dict=all_user_dict, video_oid=video_oid)
            # 写入数据库
        if all_in_one and page > 1 :
            all_commit_direct, all_user_dict = commit_json_ana(f=None, is_file=False, page_init=False, json_data=video_commits_data,
                                                            all_commit_direct=all_commit_direct, all_user_dict=all_user_dict, video_oid=video_oid)
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
    

    except Exception as e:
        print("发生了错误，终止爬取")
        print("目前截止页数：" + str(page) + "页")
        tb.print_exc()
        break
    

    


if write_copy_dict:
    user_dict_file = open(file="user_dict.json", mode="w", encoding="utf-8")
    commit_dict_file = open(file="commits_dict.json",
                            mode="w", encoding="utf-8")
    video_info_dict_file = open(file="video_info.json", mode="w", encoding="utf-8")
    json.dump(all_user_dict, user_dict_file)
    json.dump(all_commit_direct, commit_dict_file)
    json.dump(video_info_dire,video_info_dict_file)
    user_dict_file.close()
    commit_dict_file.close()
    video_info_dict_file.close()


print("爬取结束")
