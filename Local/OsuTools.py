import winreg
from .OsuDBReader.ReadOsuDB import OsuDB


class OsuTools:
    def OsuLocation() -> str:
        osu_location = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE,
                                        r"SOFTWARE\Classes\osu\DefaultIcon", 0, winreg.KEY_READ)
        p = winreg.QueryValueEx(osu_location, "")[0].split(",")[0].split("\\")
        location = ''
        for i in range(len(p) - 1):
            location += p[i] + "/"
        osu_path = location[1:]
        return osu_path

    def GetSidList(path) -> list:
        o = OsuDB(path)
        return o.sid_list()


if __name__ == "__main__":
    print(OsuTools.OsuLocation())
    print(type(OsuTools.GetSidList(OsuTools.OsuLocation())[0]))
