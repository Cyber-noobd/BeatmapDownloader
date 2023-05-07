import httpx

class Reactor:
    """
    Just a HttpX Client LOL
    """
    def __init__(self, proxy):
        self.client = httpx.Client(proxies=proxy, follow_redirects=True)
        self.initHeaders()
        
    def initHeaders(self):
        self.client.headers.update(
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'})
        self.client.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
        self.client.headers.update({'Accept-Language': 'en-US,en;q=0.5'})
        self.client.headers.update({'Accept-Encoding': 'gzip, deflate'})
        self.client.headers.update({'Connection': 'keep-alive'})
        self.client.headers.update({"origin": "https://osu.ppy.sh"})
        self.client.headers.update({"referer": "https://osu.ppy.sh/home"})
    
    
    def Restart(self, proxy):
        """
        Maybe useful?
        """
        self.client.close()
        self.client = httpx.Client(proxies=proxy, follow_redirects=True)
        self.initHeaders()
        
    def Test(self):
        try:
            a = self.client.get('https://osu.ppy.sh/home',timeout=3)
            if a.status_code == 200:
                return '200 OK'
            else:
                return "状态码:{0}".format(a.status_code)
        except httpx.ConnectTimeout:
            return '连接超时'
            
        
    def Close(self):
        self.client.close()
        

if __name__ == "__main__":
    from Network.WinProxy import WinProxy
    p = WinProxy.ReadProxy()
    if not WinProxy.TestProxy(p):
        p = None
    r = Reactor(p)
    print(type(r.client))
    print(r.client.get("https://www.google.com").status_code)
    r.Close()