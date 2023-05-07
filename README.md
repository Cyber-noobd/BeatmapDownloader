# BeatmapDownloader

基于[Textual](https://github.com/textualize/textual/)的Osu!下图器。

## 支持功能

条件搜索(od,ar,cs,星数等)。

下载某人bp/上传谱面。

## 用前需知

**推荐以Windows PowerShell(Win10)/终端(Win11默认)启动本下图器。**

本下图器为官源下图器,因此需要你的Osu!账密及Client ID&密钥。
这些敏感信息将仅以json明文保存于执行文件同目录下且仅用于为实现下图功能所必须的与Osu!服务器进行的通信。

需注意: Osu官方服务器对单个账户(可能包括ip)有暂不明确的请求限制。本下图器理论上不会触发429(访问过多),但会触发下载数量限制(推测为6小时内150-200个曲包(BeatmapSet))。
使用本下图器时请注意下载量。

## 截图
![image](https://user-images.githubusercontent.com/77134214/236674464-75832aa2-111f-49a1-bdaf-48d94a93805d.png)
![image](https://user-images.githubusercontent.com/77134214/236674480-99f70b31-a460-4a43-958b-5d31a6a029b2.png)

## 更新计划

踢开多线程。
