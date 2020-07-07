
# PYCMS开发
# 本人初次开发爬虫工具，如果您有更好的建议，可以提出（当然语气请不要太激烈）
from api_commit_get import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import queue


video_id = input("输入需要获取评论的BV号： ")
url = "https://www.bilibili.com/video/" + video_id  # BV装载


max_page_xpath = '//*[@id="comment"]/div[@class="common"]/div[@class="comment"]/div[@class="bb-comment "]/div[@class="bottom-page paging-box-big"]/div[@class="page-jump"]/span'
page_input = '//*[@id="comment"]/div[@class="common"]/div[@class="comment"]/div[@class="bb-comment "]/div[@class="bottom-page paging-box-big"]/div[@class="page-jump"]/input'
js = "window.scrollTo(0, document.body.scrollHeight)"
browser = webdriver.Firefox()
json_broswer = webdriver.Firefox()
browser.get(url)
time.sleep(20)  # 保证浏览器响应成功后再进行下一步操作
browser.execute_script(js)
time.sleep(10)
browser.execute_script(js)
max_page_string = browser.find_element_by_xpath(max_page_xpath).text
video_info_pipe = queue.Queue(0)



def video_info(video_data):
    video_basic_data = video_data['data']
    video_oid = video_basic_data['aid']
    copyright_type = video_basic_data['copyright']
    picture_add = video_basic_data['pic']
    post_time_step = video_basic_data['pubdate']
    cite_time_step = video_basic_data['ctime']
    desctrion = video_basic_data['desc']

    owner_data = video_data['owner']
    owner_mid = owner_data['mid']

    state_data = video_data['stat']
    view_number = state_data['view']
    commit_number = state_data['reply']
    favorite_number = state_data['favorite']
    coin_number = state_data['coin']
    share_number = state_data['share']
    daily_highest_rank = state_data['his_rank']
    like_number = state_data['like']
    dislike_number = state_data['dislike']

    video_info_dire = {
        'video_av': video_oid，
        'copyright_type': copyright_type,
        'picture_add': picture_add,
        'post_time_step': post_time_step,
        'cite_time_step': cite_time_step,
        'desctrion': desctrion,
        'owner_uid': owner_mid,
        'view_number': view_number,
        'favorite_number': favorite_number,
        'coin_number': coin_number,
        'share_number': share_number,
        'daily_highest_rank': daily_highest_rank,
        'like_number': like_number,
        'dislike_number': dislike_number

    }
    return video_info_dire 


def isElementExist():
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

while page < max_page or page == max_page:
    print("正在爬取" + str(page) + "页")
    json_get_url = 'https://api.bilibili.com/x/v2/reply/reply?&jsonp=jsonp&pn=' + \
        str(page)+'&type=1&oid='+str(video_oid)

   json_broswer.get(json_get_url)

    if all_in_one:
        video_info()
        commit_json_ana()
        # 写入数据库
    
    if write_copy:
        f = open(json_path, 'wb')
        json_broswer.get(json_get_url)
        f.write(json_broswer.page_source.encode("utf-8"))
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
    browser.find_element_by_xpath(page_input).send_keys(page)#准备进入指定页
    print("正在跳转至" + str(page) +"页")
    browser.find_element_by_xpath(page_input).send_keys(Keys.ENTER)# 执行跳转
    time.sleep(5)

    

print("爬取结束")
