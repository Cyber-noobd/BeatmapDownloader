import os
import json
from .OsuTools import OsuTools as ot

class ConfigSL:
    def CheckConfig():
        for a, b, c in os.walk(os.getcwd(), topdown=True):
            if 'BDConfig.json' in c:
                return True
        return False
    
    def LoadSearchSave():
        for a, b, c in os.walk(os.getcwd(), topdown=True):
            if 'SearchSave.json' in c:
                with open('./SearchSave.json','r') as f:
                    return json.load(f)
            else:
                return {}

    def SaveConfig(params: dict):
        config = {
            'username': params.get('username'),
            'password': params.get('password'),
            'osu_path': params.get('osu_path'),
            'client_id': params.get('client_id'),
            'client_key': params.get('client_key'),
            'dl_path': params.get('dl_path'),
            'dl_num': params.get('dl_num'),
        }
        with open('BDConfig.json', 'w') as f:
                    json.dump(config, f)
                    f.close()
                    
    def LoadConfig():
        if ConfigSL.CheckConfig():
            with open("./BDConfig.json") as f:
                config = json.load(f)
                params = {
                'username': config.get('username'),
                'password': config.get('password'),
                'osu_path': config.get('osu_path'),
                'client_id': config.get('client_id'),
                'client_key': config.get('client_key'),
                'dl_path': config.get('dl_path'),
                'dl_num': config.get('dl_num'),
            }
        else:
            params = {
                'username': "",
                'password': "",
                'osu_path': ot.OsuLocation(),
                'client_id': "",
                'client_key': "",
                'dl_path': ot.OsuLocation()+"Songs",
                'dl_num': "100",
            }
        return params


if __name__ == "__main__":
    print(ConfigSL.LoadConfig())