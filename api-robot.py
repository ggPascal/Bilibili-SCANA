
# PYCMS开发
# 本人初次开发爬虫工具，如果您有更好的建议，可以提出（当然语气请不要太激烈）
from api_commit_get import *

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import queue
import os

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
browser = webdriver.Firefox(fp)
json_browser = webdriver.Firefox(fp)
browser.get(url)
print("已获取链接，等待20秒，确保浏览器完成操作")
time.sleep(20)  # 保证浏览器响应成功后再进行下一步操作
browser.execute_script(js)
time.sleep(10)
browser.execute_script(js)
max_page_string = browser.find_element_by_xpath(max_page_xpath).text
video_info_pipe = queue.Queue(0)


def isElementExist(target_xpath):
    flag = True
    try:
        element = browser.find_element_by_xpath(target_xpath)
        return flag

    except:
        flag = False


max_page = int(max_page_string)
page = 1
print("共计有" + max_page_string + "页")
# 初始化结束
print("开始爬取")
json_get_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + video_id
requests.get(json_get_url)
oid_dire = requests.get(json_get_url)
oid_dire = oid_dire.text
video_stat_data = oid_dire
oid_dire = json.loads(oid_dire)
oid_dire = oid_dire['data']
video_oid = int(oid_dire['aid'])

while page < max_page or page == max_page:
    print("正在爬取" + str(page) + "页")
    json_get_url = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn=' + \
        str(page)+'&type=1&oid='+str(video_oid)
    os.chdir(root_dir)
    # time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime())+' '+
    json_path = str(page)+'.json'
    video_commits_data = requests.get(json_get_url).text
    time.sleep(15)
    video_commits_data_byte = video_commits_data.encode('utf-8')
    video_commits_data = json.loads(video_commits_data)
    # TODO:一体化入库函数
    if all_in_one:
        all_user_dict, all_commit_direct = init()
        video_info_dire = video_info(oid_dire)
        all_commit_direct, all_user_dict = commit_json_ana(f=None, is_file=False, page_init=True, json_data=video_commits_data,
                                                           all_commit_direct=all_commit_direct, all_user_dict=all_user_dict)
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
    browser.execute_script(js)  # 最下方确保获得所有元素
    pass
    # 下方代码作为保留性使用
    browser.find_element_by_xpath(page_input).send_keys(page)  # 准备进入指定页
    print("正在跳转至" + str(page) + "页")
    browser.find_element_by_xpath(page_input).send_keys(Keys.ENTER)  # 执行跳转
    time.sleep(5)

if write_copy_dict:
    user_dict_file = open(file="user_dict.json", mode="wb")
    commit_dict_file = open(file="commits_dict.json", mode="wb")
    user_dict_file.write(all_user_dict)
    commit_dict_file.write(commit_dict_file)
    user_dict_file.close()
    commit_dict_file.close()


print("爬取结束")
