from bs4 import BeautifulSoup
import queue

class HtmlParse(object):
    def parse(self,target_html,html_encode="utf-8"):
        if target_html is None:
            return
        #print(target_html)
        #创建BeautifulSoup对象
        listmain_soup = BeautifulSoup(target_html,'lxml')
        #搜索文档树,找出div标签中class为listmain的所有子标签
        chapters = listmain_soup.find_all('div',class_ = 'listmain')
        #使用查询结果再创建一个BeautifulSoup对象,对其继续进行解析
        download_soup = BeautifulSoup(str(chapters), 'lxml')
       # print(download_soup)
        new_urls=self._get_new_urls(download_soup)
        return new_urls


    def _get_new_urls(self,download_soup):
        #print(download_soup)
        #new_urls集合用于存储每章的链接
        new_urls=queue.Queue()
        #开始记录内容标志位,只要正文卷下面的链接,最新章节列表链接剔除
        begin_flag = False
        #遍历dl标签下所有子节点
        for child in download_soup.dl.children:
            #滤除回车
            if child != '\n':
                #找到《神墓》正文卷,使能标志位
                if child.string == u"《一念永恒》正文卷":
                    begin_flag = True
                #爬取链接并下载链接内容
                if begin_flag == True and child.a != None:
                    download_url = "http://www.biqukan.com" + child.a.get('href')
                    new_urls.put(download_url)
        return new_urls
