from selenium import webdriver
from lxml import etree
import time
import pymysql

driver = webdriver.Chrome()
driver.maximize_window()


if __name__ == "__main__":
    url = 'https://login.taobao.com/member/login.jhtml'
    driver.get(url)
    driver.implicitly_wait(10)

    # 让程序休眠10秒，在这期间，弹出登录界面之后，使用你的手机扫码登录淘宝
    time.sleep(10)
    # 定位搜索框，并将其清除
    driver.find_element_by_id('q').clear()
    # 在搜索框内输入“充电宝'
    driver.find_element_by_id('q').send_keys('充电宝')
    # 休息两秒，免得被发现为爬虫
    time.sleep(2)
    # 点击搜索按钮
    driver.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()
    # 休息两秒
    time.sleep(2)

    # 点击来源于“ 天猫 ” 按钮
    driver.find_element_by_xpath('//*[@id="tabFilterMall"]').click()
    # 休息两秒
    time.sleep(2)
    # 点击 “ 销量最高按钮 ”
    driver.find_element_by_xpath('//*[@id="J_relative"]/div[1]/div/ul/li[2]/a').click()
    # 休息两秒
    time.sleep(2)
    # 打印当前页面的URL
    print(driver.current_url)
    # 解析网页
    html = etree.HTML(driver.page_source)
    # 利用xpath寻找大循环。
    items = html.xpath('//div[@class="item J_MouserOnverReq  "]')

    la = []
    for item in items:
        # 利用xpath 进行小循环，打印销量排名靠前的店家名称
        shop = item.xpath('div[2]/div[3]/div[1]/a/span[2]/text()')[0]
        #将数据加到la列表
        la.append(shop)

    #将列表la中重复的数据去除
    def deleteDuplicatedElementFromList(listA):
        return sorted(set(listA), key=listA.index)

    a = deleteDuplicatedElementFromList(la)

    print(a)

    #将数据存入数据库
    for i in range(len(a)):
        conn = pymysql.connect(host='localhost', user='root', password='12345678', db='product name', charset="utf8")
        cur = conn.cursor()
        sql = "insert into product(name)values('{0}')".format(a[i])
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()