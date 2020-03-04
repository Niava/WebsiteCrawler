from urllib import request
from multiprocessing import Pool
from multiprocessing import Lock
from threading import Thread   #线程
from bs4 import BeautifulSoup
import sys
import threading
import datetime
import queue

class PoolDownLoader(object):
    def __init__(self):
        self.new_urls=queue.Queue()
        self.lock=threading.Lock()
        self.lock1=threading.Lock()
    def WriteText(self,download_name,texts):
        file = open('一念永恒1.txt', 'a', encoding='utf-8')
        soup_text = BeautifulSoup(str(texts), 'lxml')
        write_flag = True
        file.write(download_name + '\n\n')
        for each in soup_text.div.text.replace('\xa0',''):
            if each == 'h':
                write_flag = False
            if write_flag == True and each != ' ':
                file.write(each)
            if write_flag == True and each == '\r':
                file.write('\n')
        file.write('\n\n')
        #打印爬取进度
        print("已下载:"+download_name + '\r')


    def funcDown(self,download_url):
        head = {}
        head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
        download_req = request.Request(url = download_url, headers = head)
        download_response = request.urlopen(download_req)
        download_html = download_response.read().decode('gbk','ignore')
        soup_texts = BeautifulSoup(download_html, 'lxml')
        h1=soup_texts.h1.string
        texts = soup_texts.find_all(id = 'content', class_ = 'showtxt')
        #print(h1)
        self.lock.acquire()
        self.WriteText(h1,texts)
        self.lock.release()



    def PoolDown(self,new_urls):
        lock = Lock()
        p=Pool(processes=4,initargs=(lock,))


        for download_url in new_urls:
            #print(download_url)
            p.apply_async(self.funcDown,args=(download_url,))

        p.close()
        p.join()
        print("小说下载完成，已写入文档！\n")


    def ThreadDown(self,new_urls):
        starttime=datetime.datetime.now()
        self.new_urls=new_urls
        threads=[]
        while threads or self.new_urls:
            for thread in threads:
                if not thread.isAlive():
                    threads.remove(thread)
            while len(threads)<8 and not self.new_urls.empty():
                new_url=self.new_urls.get()
                thread =threading.Thread(target=self.funcDown,args=(new_url,))
                thread.setDaemon(True)
                thread.start()
                threads.append(thread)
        #thread.join()
        endtime=datetime.datetime.now()
        print("下载小说共用了;",(endtime-starttime).seconds)


    def oneprocess(self,new_urls):
        starttime=datetime.datetime.now()
        self.new_urls=new_urls
        while not self.new_urls.empty():
            new_url=new_urls.get()
            self.funcDown(new_url)
        endtime=datetime.datetime.now()
        print("下载小说共用了：",(endtime-starttime).seconds)
