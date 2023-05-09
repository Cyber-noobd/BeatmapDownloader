from textual.app import ComposeResult
from textual.containers import VerticalScroll, Grid, Container
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Label, Header, Footer
from Local.ConfigSL import ConfigSL as conf

class NoSettingScreen(Screen):
    
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
                    yield Button("下载(指定id)", id="searchm", classes="switcher")
                with Container(id="welcomearea"):
                    yield Label("请先进行设置!", id="warning")
            yield Footer()


class ErrScreen(ModalScreen):
    
    def __init__(self, ty):
        super().__init__()
        self.ty = "入" if ty == "in" else "出"
    
    def compose(self) -> ComposeResult:
        yield Grid(
            Label(f"登{self.ty}失败", id="question"),
            Button("确认", variant="error", id="ok"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()

class LoginedScreen(Screen):
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
                    yield Button("下载(指定id)", id="searchm", classes="switcher")
                with Container(id="welcomearea"):
                    yield Label("现在登录为:[green]{}[green]".format(conf.LoadConfig().get('username')))
                    yield Button("登出", variant="error", id="Slogout")
            yield Footer()
        
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "Slogout":
            if self.app.u.logout(self.app.r.client):
                self.app.switch_screen("login") 
            else:
                self.app.push_screen(ErrScreen("out"))        

class LoginScreen(Screen):
    params = {}
    def compose(self) -> ComposeResult:
        self.params = conf.LoadConfig()
        with Container(id='outer'):
            yield Header()
            with Container(id="main"):
                with VerticalScroll(id="buttons"):
                    yield Button("首页", id="welcome", classes="switcher")
                    yield Button("设置", id="option", classes="switcher")
                    yield Button("登录", id="login", classes="switcher")
                    yield Button("下载(搜索)", id="search", classes="switcher")
                    yield Button("下载(指定个人)", id="searchp", classes="switcher")
                    yield Button("下载(指定id)", id="searchm", classes="switcher")
                with Container(id="welcomearea"):
                    if not conf.CheckConfig():
                        yield Label("请先进行设置!", id="warning")
                    elif not self.app.u.islogined():
                        yield Label("将登录为:[green]{}[green]".format(self.params.get('username')))
                        yield Button("登录", variant="success", id="Slogin")
            yield Footer()
        

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "Slogin":
            a = self.app.u.login(self.params.get('username'), self.params.get('password'), self.app.r.client)
            if a:
                self.app.switch_screen("logined")
                self.app.uninstall_screen("Search")
                self.app.uninstall_screen("Searchp")
            else:
                self.app.push_screen(ErrScreen("in")) 
        elif event.button.id == "Slogout":
            if self.app.u.logout(self.app.r.client):
                self.app.switch_screen("login") 
            else:
                self.app.push_screen(ErrScreen("out")) 
                
    def on_mount(self) -> None:
        if self.app.u.islogined():
            self.app.switch_screen("logined") 
        