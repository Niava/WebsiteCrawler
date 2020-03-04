from moduleNovel import parse
from moduleNovel import ProcessPoolDownload
from moduleNovel  import downloader


class SpiderMain(object):
    def __init__(self):
        self.Htmldownloader= downloader.HtmlDownLoader()
        self.parse     = parse.HtmlParse()
        self.PoolDown  = ProcessPoolDownload.PoolDownLoader()

    def TheStart(self,target_url):
        #一念永恒小说目录地址
        target_html=self.Htmldownloader.downloader(target_url)
        new_urls=self.parse.parse(target_html)
        self.PoolDown.oneprocess(new_urls)
        #self.PoolDown.ThreadDown(new_urls)



if __name__ == "__main__":
    target_url = 'http://www.biqukan.com/1_1094/'
    Spider=SpiderMain()
    Spider.TheStart(target_url)
