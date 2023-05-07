import winreg
import httpx

class WinProxy:
    """
    Get Windows Proxy Setting by reading Winreg
    """
    def ReadProxy():
        """
        Only Read;
        Return None if not using Proxy
        """
        __path = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
        __INTERNET_SETTINGS = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,
                                                    __path, 0, winreg.KEY_ALL_ACCESS)
        try:
            if winreg.QueryValueEx(__INTERNET_SETTINGS, "ProxyEnable")[0] == 1:
                p = winreg.QueryValueEx(__INTERNET_SETTINGS, "ProxyServer")[0].split(":")
                proxy = {
                    "http://": "http://{0}:{1}".format(p[0], p[1]),
                    "https://": "http://{0}:{1}".format(p[0], p[1])
                }
                return proxy
        except FileNotFoundError:
            return None

    def TestProxy(p):
        """
        Test:Try to connect to Google
        Timeout: 5s
        """
        if not p:
            return False
        r = httpx.get('https://www.google.com/',timeout=5,proxies=p)
        try:
            return True
        except httpx.ConnectTimeout:
            return False
        except Exception as e:
            return False

if __name__ == "__main__":
    p = WinProxy.ReadProxy()
    if p:
        WinProxy.TestProxy(p)
