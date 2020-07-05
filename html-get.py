
# PYCMS开发
# 开发之初并未参考咩2016的代码（2020/06/15补充），功能可能类似，但是代码不同
# 本人初次开发爬虫工具，如果您有更好的建议，可以提出（当然语气请不要太激烈）
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

video_id = input("输入需要获取评论的BV号： ")
url = "https://www.bilibili.com/video/" + video_id # BV装载
 


max_page_xpath = '//*[@id="comment"]/div[@class="common"]/div[@class="comment"]/div[@class="bb-comment "]/div[@class="bottom-page paging-box-big"]/div[@class="page-jump"]/span'
page_input = '//*[@id="comment"]/div[@class="common"]/div[@class="comment"]/div[@class="bb-comment "]/div[@class="bottom-page paging-box-big"]/div[@class="page-jump"]/input'
js="window.scrollTo(0, document.body.scrollHeight)"
browser = webdriver.Firefox()
browser.get(url)
time.sleep(20) # 保证浏览器响应成功后再进行下一步操作
browser.execute_script(js)
time.sleep(10)
browser.execute_script(js)
max_page_string = browser.find_element_by_xpath(max_page_xpath).text
def isElementExist():
    flag=True
    try:
        element=browser.find_element_by_xpath(target_xpath)
        return flag
        
    except:
        flag=False

max_page = int(max_page_string)
page = 1
print("共计有" + max_page_string + "页")
# 初始化结束
print("开始爬取")

while page < max_page or page == max_page :
    print("正在爬取" + str(page) + "页")
    
    get_html = str(page) + ".html" 
    #打开文件，准备写入
    f = open(get_html,'wb')
    
    
    browser.execute_script(js)# 最下方确保获得所有元素
    while commit_index < 20 : # 收集评论内容
        # 参考用Xpath：
        # //*[@id="comment"]/div/div[2]/div/div[4]/div[3]/div[2]/div[3]/div[4]/b 总回复数，评论INDEX=3
        # 满回复是10条一页
        # //*[@id="comment"]/div/div[2]/div/div[4]/div[3]/div[2]/div[3]/div[1]/div[1]/div/span 回复INDEX=1, 评论INDEX=3,评论内容
        # //*[@id="comment"]/div/div[2]/div/div[4]/div[3]/div[2]/div[3]/div[2]/div[1]/div/span 回复INDEX=2，评论INDEX=3，回复内容
        # 回复span内容：<span class="text-con">回复 <a href="//space.bilibili.com/43960260" target="_blank" data-usercard-mid="43960260">@禁言小小 </a> :推荐一些呗</span>
        target_xpath = '//*[@id="comment"]/div/div[2]/div/div[4]/div['+str(commit_index)+']/div[2]/div[3]/div[4]/a'
        isElementExist()
        if flag :
            element.click()
            #TODO：编写针对多页回复的爬取行为
            
            reply_index = 1
            while reply_index < 10 or reply_index = 10 :
                reply_element=browser.find_element_by_xpath('//*[@id="comment"]/div/div[2]/div/div[4]/div[3]/div[2]/div[3]/div['+str(reply_index)+']/div[1]/div/span ').text 
                #获取待解析的文字内容，注意包含<a>用户内容
                
                
        else :
            print("评论第"+str(commit_index)+"不存在相关回复") 
            


    
    #写入文件
    f.write(browser.page_source.encode("utf-8"))
    print('写入成功')
    #关闭文件
    f.close() 
    # ————————————————
    # 版权声明：本文为CSDN博主「achiv」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
    # 原文链接：https://blog.csdn.net/qq_37088317/java/article/details/89363381
    page = page + 1
    browser.find_element_by_xpath(page_input).send_keys(page)#准备进入指定页
    print("正在跳转至" + str(page) +"页")
    browser.find_element_by_xpath(page_input).send_keys(Keys.ENTER)# 执行跳转
    time.sleep(5)

print("爬取结束")


