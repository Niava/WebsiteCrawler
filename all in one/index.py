import re
import os
import sys
from bs4 import BeautifulSoup
from urllib import request,error
import ssl
import threading
import time

# url = 'http://www.biqiuge.com/book/4772/'
# url = 'https://www.qu.la/book/1/'
#url = 'https://www.biqukan.com/book/1/'
url = 'https://www.biqiuge.com/book/'   #多线程

def getHtmlCode(url,retry_count=3):
    if url is None:
        return None
    try:
        #User-Agent
        head = {}
        head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
        target_req = request.Request(url = url, headers = head)
        page = request.urlopen(target_req)
        html = page.read()  
        htmlTree = BeautifulSoup(html,'html.parser')
    except error.HTTPError as e:
        print("HtmlDownLoader download error:",e.reason)
        htmlTree=None
        if retry_count>0:        #重试下载
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return getHtmlCode(url,retry_count-1)

    return htmlTree

    #return htmlTree.prettify()
# def getKeyContent(url):
htmlTree = getHtmlCode(url)
print(htmlTree)

def parserCaption(url):
    htmlTree = getHtmlCode(url)
    storyName = htmlTree.h2.get_text() + '.txt'
    print('小说名:',storyName)
    
    aList = htmlTree.find_all('a',href=re.compile('(\d)*.html')) 
    #print(aList)
    #aList是一个标签类型的列表，class = Tag 写入文件之前需要转化为str
    print(int(aList[1]['href'][0:-5]))
    aDealList = []
    print(aDealList)
    for line in aList:
        # line['href'] = url + line['href']
        # print(line['href'])
        chapter = int(line['href'][0:-5])
        if chapter not in aDealList:    #去重
            aDealList.append(chapter)
    aDealList.sort()    #排序
    print(aDealList)    
    # print(len(aDealList))
    # aDealList = str(aDealList)
    urlList = []
    for line in aDealList:
        line = url + str(line) + '.html'
        urlList.append(line)
    # print(urlList)
    return (storyName,urlList)
def parserChapter(url):
    htmlTree = getHtmlCode(url)
    title = htmlTree.h1.get_text()  #章节名
    content = htmlTree.find_all('div',id = 'content')
    content = content[0].contents[1].get_text()
    return (title,content)
def main(url):
    (storyName,urlList) = parserCaption(url)
    #flag = True
    # cmd = 'del ' + storyName
    # os.system(cmd)
    # cmd = 'cls'
    count = 1
    for url_alone in urlList:
        lv = count / len(urlList) * 100
        message = storyName + u'进度为:   '
        print('%-9s:    %0.2f%%'%(message,lv))
        f = open(storyName,'a+',encoding = 'utf-8')
        (title,content) = parserChapter(url_alone)
        tmp = title + '\n' + content
        f.write(tmp)
        f.close()
        count = count + 1

exitFlag = False

class myThread(threading.Thread):
    def __init__(self,threadID,name,url):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.url = url
    def run(self):
        print('开始线程:' + self.name)
        main(self.url)
        print("退出线程:" + self.name)
    
# cmd = 'del /q /s *.txt'
# os.system(cmd)
start = 16764
space = 16765

for i in range(start,space):
    url_tmp = url + str(i) + '/'
    print(url_tmp)
    tmp = 'Thread-' + str(i)
    threadName = myThread(i,tmp, url_tmp)
    threadName.start()
for i in range(1,space):
    threadName = myThread(i,tmp, url_tmp)
    threadName.join()
print("exit")
