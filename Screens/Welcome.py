from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Header, Label
from textual.containers import Container, VerticalScroll

class NotloginScreen(Screen):
    def compose(self) -> ComposeResult:
        with Container(id='outer'):
            yield Header()
            with Container(id="main"):
                with VerticalScroll(id="buttons"):
                    yield Button("首页", id="welcome", classes="switcher")
                    yield Button("设置", id="option", classes="switcher")
                    yield Button("登录", id="login", classes="switcher")
                    yield Button("下载(搜索)", id="search", classes="switcher")
                    yield Button("下载(指定个人)", id="searchp", classes="switcher")
                with Container(id="welcomearea"):
                    yield Label("请先登录!", id="warning")
            yield Footer()

class WelcomeScreen(Screen):
    
    def compose(self) -> ComposeResult:
        with Container(id='outer'):
            yield Header()
            with Container(id="main"):
                with VerticalScroll(id="buttons"):
                    yield Button("首页", id="welcome", classes="switcher")
                    yield Button("设置", id="option", classes="switcher")
                    yield Button("登录", id="login", classes="switcher")
                    yield Button("下载(搜索)", id="search", classes="switcher")
                    yield Button("下载(指定个人)", id="searchp", classes="switcher")
                with Container(id="welcomearea"):
                    yield Label("用前需知", classes="title")
                    yield Label("""本下图器为官源下图器,因此需要你的Osu!账密及Client ID&密钥。
                                \n这些敏感信息将仅以json明文保存于执行文件同目录下且仅用于为实现下图功能所必须的与Osu!服务器进行的通信。
                                \n需注意: Osu官方服务器对单个账户(可能包括ip)有暂不明确的请求限制。本下图器理论上不会触发429(访问过多),
                                \n但会触发下载数量限制(推测为6小时内150-200个曲包(BeatmapSet))。使用本下图器时请注意下载量。
                                \n※ 本下图器会读取osu.db以避免重复下载图包。
                                \n※ 本下图器支持在游玩Osu!时运行\n""", classes="text")
                    yield Label("使用方式", classes="title")
                    yield Label("""0.强烈建议使用Windows_PowerShell启动本下图器。(如果你是Win11用户,使用默认的Windows终端即可。)
                                \nCMD环境下本下图器功能正常运行,但显示效果较差。
                                \n1.在设置中填写所需信息。
                                \n关于Client: 在https://osu.ppy.sh/home/account/edit最下方点击新的Oauth应用(只需填写应用名称)。
                                \n2.(可选性 建议进行)在设置中进行代理状态刷新(同时测试网络可用性)。
                                \n3.在登录页中登录。设计上,本下图器不会保存登录状态。
                                \n4.在下载页中设置搜索项目,进行搜索。
                                \n5.在搜索结果页确认下载 等待下载完成。
                                \n6.(可选性 建议进行)在关闭下图器前在登录页中登出。\n""", classes="text")
                    yield Label("""By 码的很烂的Yuria
                                \n觉得好用可以去Github上点个⭐(
                                \nhttps://github.com/Cyber-noobd/Beatmap-Downloader""", classes="text")
            yield Footer()