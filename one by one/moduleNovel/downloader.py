from urllib import request,error

class HtmlDownLoader(object):
    def downloader(self,target_url,retry_count=3):
        if target_url is None:
            return None
        try:
            #User-Agent
            head = {}
            head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
            target_req = request.Request(url = target_url, headers = head)
            target_response = request.urlopen(target_req)
            target_html = target_response.read().decode('gbk','ignore')
            print("整个页面"+target_html)
        except error.HTTPError as e:
            print("HtmlDownLoader download error:",e.reason)
            target_html=None
            if retry_count>0:        #重试下载
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return self.downloader(target_url,retry_count-1)
        return target_html
