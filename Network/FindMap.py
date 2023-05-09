import httpx
import json
import time
from Local.OsuTools import OsuTools

class MapFinder:
    url = "https://osu.ppy.sh/beatmapsets/search"
    conf = {
        "params": {},
        "num": 0
    }
    local_map = OsuTools.GetSidList(OsuTools.OsuLocation())
    
    def SetParams(self, inparams: dict, num: int):
        self.conf['params'] = {
            "e": inparams.get('e'),  # video and sb
            "c": inparams.get('c'),  # recommended
            "g": inparams.get('g'),  # useless
            "l": inparams.get('l'),  # useless
            "m": inparams.get('m'),  # mode 0 1 2 3
            "nsfw": inparams.get('nsfw'),  # none or false
            "q": inparams.get('q'),  # 搜索项 虽然但是 哪都没写这东西的附带参数
            "r": inparams.get('r'),  # 成绩 useless
            "sort": inparams.get('sort'),  # 排序 plays_desc useless?
            "s": inparams.get('s'),  # 分类 留空rank+ loved
            "played": inparams.get('played'),  # supporter only
            "cursor_string": inparams.get('cs'),  # 分页
        }
        self.conf['num'] = num
        
    def UpdateCs(self, cs):
        self.conf['params']['cursor_string'] = cs
    
    def Search(self, client: httpx.Client):
        """
        仅应当在登录后调用
        """
        meta = json.loads(client.get(self.url, params=self.conf['params']).content)
        self.UpdateCs(meta.get('cursor_string'))
        beatmapsets = meta.get('beatmapsets') # list
        result = []
        for bset in beatmapsets: # dict
            artist = bset.get('artist_unicode')
            sid = bset.get('id')
            if sid in self.local_map:
                continue
            mode = bset.get('beatmaps')[0].get('mode')
            title = bset.get('title_unicode')
            tags = bset.get('tags').split(' ')
            if len(tags)>5:
                tag = tags[:5]
            else:
                tag = tags
            mapper = bset.get('creator')
            diffs = sorted([i.get('difficulty_rating') for i in bset.get('beatmaps')])
            result.append((title, sid, mode, artist, mapper, str(diffs).replace('[','').replace(']',''), str(tag).replace('[','').replace(']','')))
        return result
    
    def getPass(self,cid,ckey,client):
        url = 'https://osu.ppy.sh/oauth/token'
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        d = {
            "client_id": cid,
            "client_secret": ckey,
            "grant_type": "client_credentials",
            "scope": "public"
        }
        key = json.loads(client.post(
            url, json=d, headers=headers, timeout=5).content).get('access_token')
        return {
            "Authorization": 'Bearer %s' % key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
    def getUserID(self, name,client:httpx.Client,headers):
        urlb = f"https://osu.ppy.sh/api/v2/users/{name}"
        params = {
            "key": "username"
        }
        back = json.loads(client.get(urlb, headers=headers, params=params).content)
        uid = back.get('id')
        return uid
        
    def getUserScore(self,uid,m,client:httpx.Client,headers):
        urlb = f"https://osu.ppy.sh/api/v2/users/{uid}/scores/best"
        params = {
            "mode": m,
            "limit": '100'
        }
        back = json.loads(client.get(urlb, headers=headers, params=params).content)
        result = []
        for bset in back:
            sid = bset.get("beatmapset").get('id')
            if sid in self.local_map:
                continue
            artist = bset.get("beatmapset").get('artist_unicode')
            mode = m
            title = bset.get("beatmapset").get('title_unicode')
            tag = bset.get("beatmapset").get('source')
            mapper = bset.get("beatmapset").get('creator')
            diffs = " "
            result.append((title, sid, mode, artist, mapper, diffs, tag))
        return result
    
    def getUserMaps(self, uid, client:httpx.Client, headers):
        ml = ["loved", "pending", "ranked", "graveyard"]
        result = []
        x = 0
        for um in ml:
            while 1:
                offset = x
                apiurl = f"https://osu.ppy.sh/api/v2/users/{uid}/beatmapsets/{um}?limit=999&offset={offset}"
                maps = json.loads(client.get(apiurl, headers=headers, timeout=5).content)
                if maps:
                    for bset in maps:
                        x += 1
                        sid = bset.get('id')
                        if sid in self.local_map:
                            continue
                        artist = bset.get('artist_unicode')
                        mode = bset.get('beatmaps')[0].get('mode')
                        title = bset.get('title_unicode')
                        tags = bset.get('tags') if bset.get('tags') else bset.get("source")
                        if len(tags.split(' '))>5:
                            tag = tags.split(' ')[:5]
                        else:
                            tag = tags
                        mapper = bset.get('creator')
                        diffs = sorted([i.get('difficulty_rating') for i in bset.get('beatmaps')])
                        result.append((title, sid, mode, artist, mapper, str(diffs).replace('[','').replace(']',''), str(tag)))
                if len(maps) < 100:
                    break
        return result
    
    def Searchp(self,params, client: httpx.Client):
        headers = self.getPass(params.get('cid'),params.get('ckey'),client)
        u = self.getUserID(params.get('q'), client, headers)
        t = params.get('t')
        m = params.get('m')
        result = []
        if t == 'bp':
            if m == "all":
                for t in ["osu","taiko","fruits","mania"]:
                    result += self.getUserScore(u,t,client,headers)
                    time.sleep(0.25)
            else:
                result = self.getUserScore(u,m,client,headers)
        if t == "up":
            result = self.getUserMaps(u,client,headers)
        client.request("DELETE","https://osu.ppy.sh/api/v2/oauth/tokens/current", headers=headers)
        if len(result)>150:
            return result[:150]
        else:return result
        
    def getMapBySid(self,sid,client,headers):
        url = f"https://osu.ppy.sh/api/v2/beatmapsets/{sid}"
        back = json.loads(client.get(url, headers=headers).content)
        sid = back.get('id')
        if sid in self.local_map:
            sid = "*已有 " + str(sid)
        artist = back.get('artist_unicode')
        mode = back.get('beatmaps')[0].get('mode')
        title = back.get('title_unicode')
        tags = back.get('tags') if back.get('tags') else back.get("source")
        if len(tags.split(' '))>5:
            tag = tags.split(' ')[:5]
        else:
            tag = tags
        mapper = back.get('creator')
        diffs = sorted([i.get('difficulty_rating') for i in back.get('beatmaps')])
        return (title, sid, mode, artist, mapper, str(diffs).replace('[','').replace(']',''), str(tag).replace('[','').replace(']',''))

    def BidToSid(self,mid, client, headers):
        url = f"https://osu.ppy.sh/api/v2/beatmaps/{mid}"
        return json.loads(client.get(url, headers=headers).content).get("beatmapset_id")
        
    def Searchm(self,params, client: httpx.Client):
        headers = self.getPass(params.get('cid'),params.get('ckey'),client)
        t = params.get('t')
        q = params.get('q')
        result = []
        if t == "sid":
            for mid in q:
                result.append(self.getMapBySid(mid,client, headers))
        else:
            for mid in q:
                result.append(self.getMapBySid(self.BidToSid(mid, client, headers), client, headers))
        client.request("DELETE","https://osu.ppy.sh/api/v2/oauth/tokens/current", headers=headers)
        if len(result)>150:
            return result[:150]
        else:return result
    
    def CreateMapList(self, client: httpx.Client):
        result = []
        while len(result) < self.conf['num']:
            result += self.Search(client)
        return result[:self.conf['num']]
    



   
