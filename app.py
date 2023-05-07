from textual.app import App, ScreenStackError
from textual.widgets import Button
import Screens.Welcome
import Screens.Options
import Screens.Login
import Screens.Search
import Screens.Searchp
import Screens.MapTable
from Network.WinProxy import WinProxy
from Network.MainHttpReactor import Reactor
from Network.VirtualUser import VUser
from Local.ConfigSL import ConfigSL as conf
from textual import log

class BeatMapDownloader(App[str]):
    CSS_PATH = ["./css/app.css", "./css/dl.css"]
    BINDINGS = [("Ctrl+C", "pass", "退出")]
    SCREENS = {
            "welcome": Screens.Welcome.WelcomeScreen(),
            "option": Screens.Options.OptionScreen(),
            "noset": Screens.Login.NoSettingScreen(),
            "login": Screens.Login.LoginScreen(),
            "logined": Screens.Login.LoginedScreen(),
            "nologin": Screens.Welcome.NotloginScreen(),
            "search": Screens.Search.SearchScreen(),
            "searchp": Screens.Searchp.SearchpScreen()
        }
    r = Reactor(WinProxy.ReadProxy())
    u = VUser()
    Mapset = []
        
    def on_ready(self) -> None:
         self.push_screen("welcome")
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if 'switcher' in event.button.classes:
            screen_id = "logined" if event.button.id == 'login' and self.u.islogined() else event.button.id
            if screen_id in ["search", "searchp"] and not self.u.islogined():
                screen_id = 'nologin'
            if screen_id == "login" and not conf.CheckConfig():
                screen_id = 'noset'
            try:
                self.switch_screen(screen_id)
            except ScreenStackError as e:
                self.push_screen(screen_id)
            log(self.screen_stack)
    
            
if __name__ == "__main__":
    app = BeatMapDownloader()
    app.run()
