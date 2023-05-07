import httpx
import json
from bs4 import BeautifulSoup

class VUser:
    base_url = "https://osu.ppy.sh/"
    XSRF_TOKEN = ""
    info = ""
    
    def login(self, username, password, client: httpx.Client):
        try:
            soup = BeautifulSoup(client.get(self.base_url + "home", timeout=5).text, 'html.parser')
        except Exception as e:
            return False
        data = {
            '_token': soup.find('input').attrs['value'],
            'username': username,
            'password': password
        }
        try:
            a = client.post(self.base_url + "session", data=data)
            b = json.loads(a.text).get('user')
            self.XSRF_TOKEN = a.cookies["XSRF-TOKEN"]
            self.info = b.get('username')
            return True
        except Exception as e:
            return False
        
    def islogined(self):
        if self.XSRF_TOKEN:
            return True
        else:
            return False
        
    def logout(self, client: httpx.Client):
        client.headers.update({'x-csrf-token': self.XSRF_TOKEN})
        logout_url = "https://osu.ppy.sh/session"
        v = client.delete(logout_url)
        if v.status_code == 200:
            self.XSRF_TOKEN = ""
            return True
        else:
            return False
    
        
        
if __name__ == "__main__":
    from MainHttpReactor import Reactor
    from WinProxy import WinProxy
    r =Reactor(WinProxy.ReadProxy())
    u = VUser()
    u.login('[GB]Yuria',"Yur1ach2n",r.client)
    print(u.info)
    u.logout()