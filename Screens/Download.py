from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, DataTable, Header, Footer, Static, Label
from textual.message import Message
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress
from textual import log, work
from Local.ConfigSL import ConfigSL as conf
import os
import time


class DLStarted(Message):
        def __init__(self, sid) -> None:
            self.sid = sid
            super().__init__()
            
class DLInfo(Message):
        def __init__(self, sid, description, total) -> None:
            self.sid = sid
            self.description = description
            self.total = total
            super().__init__()

class DLAdvance(Message):
        def __init__(self, sid, advance) -> None:
            self.sid = sid
            self.advance = advance
            super().__init__()
    
class DLProgress(Message):
        def __init__(self, sid, progress) -> None:
            self.sid = sid
            self.progress = progress
            super().__init__()
            
class DLDone(Message):
        def __init__(self, sid) -> None:
            self.sid = sid
            super().__init__()
            
class DLError(Message):
        def __init__(self, sid, e) -> None:
            self.sid = sid
            self.e = e
            super().__init__()
            
class RichProgress(Static):
    def __init__(self,id):
        super().__init__(id=id)
        self.bar = Progress()  

    def on_mount(self) -> None:
        self.update_render = self.set_interval(
            1 / 60, self.update_progress_bar
        )  

    def update_progress_bar(self) -> None:
        self.update(self.bar)

class DownloadScreen(Screen):
    ban_list = ['<', '>', '/', '\\', '|', ':', '"', '*', '?', "%20", "%2D"]
    path = conf.LoadConfig().get('dl_path') + "\\"
    taskids = {}
    
    def compose(self) -> ComposeResult:
        with Container(id='outer'):
            yield Header()
            with Container(id="main"):
                with VerticalScroll(id="buttons"):
                    yield Button("首页", id="welcome", classes="switcher", disabled=True)
                    yield Button("设置", id="option", classes="switcher", disabled=True)
                    yield Button("登录", id="login", classes="switcher", disabled=True)
                    yield Button("下载(搜索)", id="search", classes="switcher", disabled=True)
                    yield Button("下载(指定个人)", id="searchp", classes="switcher", disabled=True)
                with Container(id="welcomearea"):
                    yield DataTable(id="dltable")
                    yield RichProgress(id="progress")
                    yield Label(id="dlcm")
            yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        rows = iter(self.app.Mapset)
        table.add_columns("标题","sid","模式","艺术家","麻婆","星数","Tag")
        table.add_rows(rows)
        self.CreateWorker()
        
    @work(exclusive=False)
    def CreateWorker(self):
        self.post_message(DLStarted("总进度"))
        self.post_message(DLInfo("总进度","总进度",len(self.app.Mapset)))
        with ThreadPoolExecutor(max_workers=4) as nigger:
            all_tasks = []
            for mps in self.app.Mapset:
                log(self.path)
                all_tasks.append(nigger.submit(self.job, mps[1], mps[0], False))
                time.sleep(0.5)
            for future in as_completed(all_tasks):
                if future.exception():
                    r = eval(str(future.exception()))
                    all_tasks.append(nigger.submit(self.job, r[0], r[1], True))
                    
    def job(self,sid,name, re):
        self.post_message(DLStarted(sid))
        file_name = name
        for b in self.ban_list:
            file_name = file_name.replace(b, '-')
        with open(self.path + file_name + ".tmp", "wb") as f:
            try:
                with self.app.r.client.stream('GET', f"https://osu.ppy.sh/beatmapsets/{sid}/download") as resp:
                    len = int(resp.headers.get('Content-Length')) if resp.headers.get('Content-Length') else 9999999
                    self.post_message(DLInfo(sid, file_name, len))
                    for chunk in resp.iter_bytes():
                        f.write(chunk)
                        self.post_message(DLProgress(sid, resp.num_bytes_downloaded))
                    f.close()
                    os.rename(self.path + file_name + ".tmp", self.path + file_name + ".osz")
                    self.post_message(DLAdvance("总进度", 1))
                    self.post_message(DLDone(sid))
            except Exception as e: 
                f.close()
                os.remove(self.path + file_name + ".tmp")
                self.post_message(DLError(sid, e))
                if re:
                    self.post_message(DLDone(sid))
                    self.post_message(DLAdvance("总进度", 1))
                    return
                else:
                    time.sleep(5)
                    self.post_message(DLDone(sid))
                    raise Exception([sid, name])
                
                        
    def on_dlstarted(self, message: DLStarted) -> None:
        self.taskids[message.sid] = self.query_one("#progress").bar.add_task(description='开始下载', total=9999999)
    
    def on_dlinfo(self, message: DLInfo) -> None:
         self.query_one("#progress").bar.update(self.taskids[message.sid], description=message.description,
                                           total = message.total)
    
    def on_dladvance(self, message: DLAdvance) -> None:
        self.query_one("#progress").bar.update(self.taskids[message.sid], advance=message.advance)
        if  self.query_one("#progress").bar.tasks[self.taskids[message.sid]].completed == len(self.app.Mapset):
            self.query_one("#dlcm").update("下载完成")
            for b in self.query(".switcher"):
                b.disabled = False
    
    def on_dlprogress(self, message: DLProgress) -> None:
        self.query_one("#progress").bar.update(self.taskids[message.sid], completed=message.progress)
    
    def on_dldone(self, message: DLDone) -> None:
        self.query_one("#progress").bar.remove_task(self.taskids[message.sid])
        
    def on_dlerror(self, message: DLError) -> None:
        self.query_one("#progress").bar.update(self.taskids[message.sid], description=f"重试下载:{message.sid}")
        log(message.e)

    
    
