from textual.app import App, ComposeResult
from textual.containers import Grid,Container, VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Footer, Header, Label, Input
from Local.ConfigSL import ConfigSL as conf
from Network.WinProxy import WinProxy
from textual import work
from textual import log
        
class ResultScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("设置已保存", id="question"),
            Button("确认", variant="success", id="ok"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()

class CommitScreen(ModalScreen):
    
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("确认设置更改?", id="question"),
            Button("确认", variant="primary", id="commit"),
            Button("Cancel", variant="default", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "commit":
            self.app.pop_screen()
            conf.SaveConfig(eval(self.name))
            self.app.push_screen(ResultScreen())
        else:
            self.app.pop_screen()
            
class RefreshScreen(ModalScreen):
    def compose(self) -> ComposeResult:      
        yield Grid(
            Label("刷新中......", id="question"),
            Button("确认", variant="primary", id="r_commit", disabled=True),
            id="dialog",
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()
    
    async def on_mount(self):
        self.CreateWorker()
        
    @work(exclusive=False)
    def CreateWorker(self):
        log("worker begin working")
        self.app.r.Restart(WinProxy.ReadProxy())
        p = WinProxy.ReadProxy()
        usable = self.app.r.Test()
        self.query_one("#question").update(f"现在使用的代理为:{p}\n测试结果:{usable}")
        self.query_one("#r_commit").disabled = False
        
class OptionScreen(Screen):
    params = {}
    
    def compose(self) -> ComposeResult:
        config = conf.LoadConfig()
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
                    yield Label("Osu!", classes="title")
                    yield Container(
                        Label("\nOsu路径:"),
                        Input(value=config['osu_path'], name="osu_path", placeholder="Input Osu Location Here"),
                        classes="InputContainer",
                    )
                    yield Container(
                        Label("\nOsu账户:"),
                        Input(value=config['username'], name="username",placeholder="你的用户名"),
                        classes="InputContainer",
                    )
                    yield Container(
                        Label("\nOsu密码:"),
                        Input(value=config['password'], name="password",placeholder="密码"),
                        classes="InputContainer",
                    )
                    yield Container(
                        Label("\nClient ID:"),
                        Input(value=config['client_id'], name="client_id",placeholder="Client ID"),
                        classes="InputContainer",
                    )
                    yield Container(
                        Label("\nClient Key:"),
                        Input(value=config['client_key'], name="client_key",placeholder="Client Key"),
                        classes="InputContainer",
                    )
                    yield Label("下载相关", classes="title")
                    yield Button("刷新代理启用", variant="warning", id="refresh")
                    yield Container(
                        Label("\n下载路径:"),
                        Input(value=config['dl_path'], name="dl_path",placeholder="密码"),
                        classes="InputContainer",
                    )
                    yield Container(
                        Label("\n下载数量:"),
                        Input(value=config['dl_num'], name="dl_num",placeholder="密码"),
                        classes="InputContainer",
                    )
                    yield Button("保存", variant="success", id="save", classes="save")
            yield Footer()
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.app.push_screen(CommitScreen(name=str(self.params)))
        elif event.button.id == "refresh":
            self.app.push_screen(RefreshScreen())
        
    def on_input_changed(self, event: Input.Changed) -> None:
        self.params[event.input.name] = event.input.value
        

