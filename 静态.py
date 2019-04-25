from requests_html import HTMLSession
import requests
import re
import  pymysql

#获取网页后台代码
def getHTMLtext(url):
    session = HTMLSession()
    r = session.get(url)
    return r


def getpage(url):
    for i in range(1, 9):
        r=getHTMLtext(url)
        aa = []
        bb = []
        cc = []

        #爬取标题
        data_title = r.html.find(
            '#content > div > div.article > ul > li:nth-child(' + str(i) + ') > div.media__body > h2 > a',
            first=True)
        #爬取详情
        data_detail = r.html.find(
            '#content > div > div.article > ul > li:nth-child(' + str(
                i) + ') > div.media__body > p.subject-abstract.color-gray',
            first=True)
        #爬取图片
        data_img = r.html.find(
            '#content > div > div.article > ul > li:nth-child(' + str(i) + ') > div.media__img > a > img',
            first=True)
        #用正则获取图片的链接
        url_img = re.findall(r"src='(.*?)'", str(data_img))

        #将标题，详情，图片分别添加到列表aa，bb，cc中
        aa.append(data_title.text)
        bb.append(data_detail.text)
        for i in url_img:
            cc.append(i)

        #输出爬取的内容
        print(aa)
        print(bb)
        print(cc)


        #把数据插入数据库

        for i in range(len(bb)):
            conn = pymysql.connect(host='localhost', user='root', password='12345678', db='myApp', charset="utf8")
            cur = conn.cursor()
            sql = "insert into myApp2_bookdetails(title,detail,imgs)values('{1}','{2}','{3}')".format(i, aa[i], bb[i],
                                                                                                     cc[i])
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()



def main():
    session = HTMLSession()
    url = 'https://book.douban.com/chart?subcat=F&icn=index-topchart-fiction'
    getpage(url)
main()