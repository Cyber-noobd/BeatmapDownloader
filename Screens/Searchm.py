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

class SearchmScreen(Screen):
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
                    yield Button("下载(指定id)", id="searchm", classes="switcher")
                with Container(id="welcomearea"):
                    if not self.app.u.islogined():
                        yield Label("请先登录!", id="warning")
                    else:
                        with VerticalScroll(id="searcharea"):
                            yield Label("单次最大下载150首!\n", id="warning")
                            yield Label("搜索设置", classes="title")
                            yield Container(
                                Label("bid或sid(注意区分):\n"),
                                Input(name="mid", placeholder="谱面/图包id  id1,id2,.."),
                                classes="InputContainerm",
                            )
                            yield Grid(
                                Container(
                                    Label("类型:"),
                                    OptionList("bid", "sid", name="mtype"),
                                    classes="ListContainer",
                                    id="type"
                                ),
                                id="chooseaream"
                            )
                            yield Button("开始搜索", variant="success", id="SSearchm")
            yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.params[event.input.name] = event.input.value

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        self.params[event.option_list.name] = event.option_index
        

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "SSearchm":
            if self.params.get('mid') != None:
                q = self.params.get('mid').replace(" ", "").replace("，", "").split(',')
                t = ["bid", "sid"]
                oparams = {
                    "t": t[self.params.get('mtype')] if self.params.get('mtype') else t[0],
                    "q": q,
                    "cid": conf.LoadConfig().get('client_id'),
                    "ckey": conf.LoadConfig().get('client_key')
                }
                m = MapFinder()
                try:
                    self.app.Mapset = m.Searchm(oparams,self.app.r.client)
                    self.app.push_screen(TableScreen())
                except Exception as e:
                    log(e)
                    log(e)
                    log(e)
                    self.app.push_screen(ErrScreen())
            else:
                self.app.push_screen(ErrScreen())
