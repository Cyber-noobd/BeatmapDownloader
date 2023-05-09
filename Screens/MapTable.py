from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, DataTable, Header, Footer
from .Download import DownloadScreen



class TableScreen(Screen):
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
                    yield DataTable(id="maptable")
                    yield Button("确认下载", variant="success", id="download")
            yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        rows = iter(self.app.Mapset)
        table.add_columns("标题","sid","模式","艺术家","麻婆","星数","Tag")
        table.add_rows(rows)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "download":
            self.app.pop_screen()
            self.app.push_screen(DownloadScreen())
