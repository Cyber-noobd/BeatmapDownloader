from textual.app import ComposeResult
from textual.containers import Grid, Container, VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Label, Input, OptionList, Switch, Header, Footer
from Local.ConfigSL import ConfigSL as conf
from Network.FindMap import MapFinder
from textual import log
from .MapTable import TableScreen
import re
import json


class ErrScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("搜索失败,请检查网络", id="question"),
            Button("确认", variant="error", id="ok"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()

class SearchScreen(Screen):
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
                    with VerticalScroll(id="searcharea"):
                        yield Label("搜索设置", classes="title")
                        yield Container(
                            Label("\n搜索内容:"),
                            Input(value=self.save.get('query'),
                                name="query", placeholder="与官网搜索相同"),
                            classes="InputContainer",
                        )
                        yield Label("※ 排序不为最相关时,搜索结果很可能与输入不符", id="warning")
                        yield Grid(
                            Container(
                                Label("Rank状态:"),
                                OptionList("拥有排行榜", "上架(ranked)", "过审(qualified)",
                                        "社区喜爱(loved)", name="status"),
                                classes="ListContainer",
                                id="long"
                            ),
                            Container(
                                Label("模式:"),
                                OptionList("all", "osu", "taiko",
                                        "catch", "mania", name="mode"),
                                classes="ListContainer",
                            ),
                            Container(
                                Label("BGA&SB:"),
                                OptionList("默认", "有视频", "有故事板", "都有", name="sb"),
                                classes="ListContainer",
                            ),
                            Container(
                                Label("排序:"),
                                OptionList("最相关", "由新到旧", "由旧到新","评分从高到低","评分从低到高","难度从高到低","难度从低到高", name="sort"),
                                classes="ListContainer",
                            ),
                            id="choosearea"
                        )
                        yield Grid(
                            Container(
                                Label("\n排除NSFW:"),
                                Switch(animate=False, name="NONSFW"),
                                classes="SwContainer",
                            ),
                            Container(
                                Label("\n使用推荐难度:"),
                                Switch(animate=False, name="re_diff"),
                                classes="SwContainer",
                            ),
                            Container(
                                Label("\n仅精选艺术家:"),
                                Switch(animate=False, name="FA"),
                                classes="SwContainer",
                            ),
                            id="swarea"
                        )
                        yield Grid(
                            Container(
                                Label("\nod:"),
                                Input(value=self.save.get('od'), name="od",
                                    placeholder="仅整数 最小od:最大od 例: 5:8 留空不筛选od范围"),
                                classes="OdContainer",
                                id="od"
                            ),
                            Container(
                                Label("\n星数:"),
                                Input(value=self.save.get('star'), name="star",
                                    placeholder="精确度两位小数 最小星数:最大星数 例: 5:5.09"),
                                classes="OdContainer",
                                id="star"
                            ),
                            Container(
                                Label("\nar:"),
                                Input(value=self.save.get('ar'), name="ar", placeholder="同上"),
                                classes="OdContainer",
                            ),
                            Container(
                                Label("\ncs:"),
                                Input(value=self.save.get('cs'), name="cs", placeholder="同上"),
                                classes="OdContainer",
                            ),
                            Container(
                                Label("\nRank日期:"),
                                Input(value=self.save.get('date'), name="date",
                                    placeholder="起始-结束 YYYYMMDD 例:20220101-20230101 留空不筛选"),
                                classes="OdContainer",
                                id="date"
                            ),
                            id="odarea"
                        )
                        yield Button("开始搜索", variant="success", id="SSearch")
            yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.params[event.input.name] = event.input.value

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        self.params[event.option_list.name] = event.option_index

    def on_switch_changed(self, event: Switch.Changed):
        self.params[event.switch.name] = event.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "SSearch":
            input_save = {
                'query': self.params.get('query'),
                'od': self.params.get('od'),
                'ar': self.params.get('ar'),
                'cs': self.params.get('cs'),
                'star': self.params.get('star'),
                'date': self.params.get('date')
            }
            with open('SearchSave.json', 'w') as f:
                json.dump(input_save, f)
                f.close()
            e = ["", 'video', 'storyboard', 'video.storyboard']
            c = ""
            so = ["relevance_desc", "ranked_desc", "ranked_asc", "rating_desc", "rating_asc", "difficulty_desc", "difficulty_asc"]
            if self.params.get('FA'):
                c += "featured_artists"
            if self.params.get('re_diff') and self.params.get('FA'):
                c += "."
            if self.params.get('re_diff'):
                c += "recommended"
            nsfw = 'false' if self.params.get('NONSFW') else ""
            q = self.params.get('query') + " " if self.params.get('query') else " "
            m = ["", '0', '1', '2', '3']
            s = ["", "ranked", "qualified", "loved"]
            if self.params.get('od'):
                try:
                    a, b = self.params.get('od').split(":")
                    if int(a) in range(0, 10) and int(b) in range(0, 10) and int(a) < int(b):
                        q += "od>={0} od<={1}".format(a, b)
                except:
                    pass
            if self.params.get('star'):
                try:
                    a, b = self.params.get('star').split(":")
                    if int(a) in range(0, 20) and int(b) in range(0, 20) and int(a) <= int(b):
                        q += "od>={0} od<={1}".format(a, b)
                except:
                    pass
            if self.params.get('ar'):
                try:
                    a, b = self.params.get('ar').split(":")
                    if int(a) in range(0, 10) and int(b) in range(0, 10) and int(a) < int(b):
                        q += " ar>={0} ar<={1}".format(a, b)
                except:
                    pass
            if self.params.get('cs'):
                try:
                    a, b = self.params.get('cs').split(":")
                    if int(a) in range(0, 10) and int(b) in range(0, 10) and int(a) < int(b):
                        q += " cs>={0} cs<={1}".format(a, b)
                except:
                    pass
            if self.params.get('date'):
                try:
                    a, b = self.params.get('date').split("-")
                    if len(a) == 8 and len(b) == 8 and re.search('[0-9]{8}', a) and re.search('[0-9]{8}', b):
                        q += " ranked>{0} ranked<{1}".format(a, b)
                except:
                    pass
            if q[-1] == " ":
                q = q[:-1]
            oparams = {
                "e": e[self.params.get('sb')] if self.params.get('sb') else "",  # video and sb
                "c": c,  # recommended
                "m": m[self.params.get('mode')] if self.params.get('mode') else "",  # mode 0 1 2 3
                "nsfw": nsfw ,  # none or false
                "q": q,  # 搜索项
                "sort": so[self.params.get('sort')] if self.params.get('sort') else 'relevance_desc',  # 排序 
                "s": s[self.params.get('status')] if self.params.get('status') else "",  # 分类 留空rank+ loved
            }
            m = MapFinder()
            m.SetParams(oparams, int(conf.LoadConfig().get('dl_num')))
            try:
                self.app.Mapset = m.CreateMapList(self.app.r.client)
                self.app.push_screen(TableScreen())
            except Exception as e:
                log(e)
                self.app.push_screen(ErrScreen())
