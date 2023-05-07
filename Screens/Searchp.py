from textual.app import ComposeResult
from textual.containers import Grid, Container, VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Label, Input, OptionList, Switch, Header, Footer
from Local.ConfigSL import ConfigSL as conf
from Network.FindMap import MapFinder
from textual import log
from .MapTable import TableScreen



class ErrScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("搜索失败,请检查输入或网络!", id="question"),
            Button("确认", variant="error", id="ok"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()

class SearchpScreen(Screen):
    params = {}
    save = conf.LoadSearchSave()

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
                    if not self.app.u.islogined():
                        yield Label("请先登录!", id="warning")
                    else:
                        with VerticalScroll(id="searcharea"):
                            yield Label("单次最大下载150首!\n", id="warning")
                            yield Label("搜索设置", classes="title")
                            yield Container(
                                Label("\n指定ID:"),
                                Input(name="pname", placeholder="某人的Osu!名称"),
                                classes="InputContainer",
                            )
                            yield Grid(
                                Container(
                                    Label("类型:"),
                                    OptionList("BP", "上传谱面", name="ptype"),
                                    classes="ListContainer",
                                    id="type"
                                ),
                                Container(
                                    Label("模式(BP):"),
                                    OptionList("all", "osu", "taiko",
                                            "catch", "mania", name="pmode"),
                                    classes="ListContainer",
                                ),
                                id="chooseareap"
                            )
                            yield Button("开始搜索", variant="success", id="SSearchp")
            yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.params[event.input.name] = event.input.value

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        self.params[event.option_list.name] = event.option_index
        

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "SSearchp":
            if self.params.get('pname') != None:
                q = self.params.get('pname')
                t = ["bp", "up"]
                m = ["all", "osu","taiko","fruits","mania"]
                oparams = {
                    "m": m[self.params.get('pmode')] if self.params.get('pmode') else "all",
                    "t": t[self.params.get('ptype')] if self.params.get('ptype') else t[0],
                    "q": q,
                    "cid": conf.LoadConfig().get('client_id'),
                    "ckey": conf.LoadConfig().get('client_key')
                }
                m = MapFinder()
                try:
                    self.app.Mapset = m.Searchp(oparams,self.app.r.client)
                    self.app.push_screen(TableScreen())
                except Exception as e:
                    log(e)
                    log(e)
                    log(e)
                    self.app.push_screen(ErrScreen())
            else:
                self.app.push_screen(ErrScreen())
