# NAS 音乐助手

本项目基于[GD 音乐台](https://music.gdstudio.org)提供的 API，我打包成了 Docker 容器，方便搜索歌曲，一键入库 NAS。

## 🎵 NAS 音乐方案
顺便分享下我的自用方案，几乎`全平台`制霸了，但我不是发烧友，音乐爱好者可参考吧。此方案涉及的所有工具基础功能`完全免费`，目前可实现一键入库，自动匹配音乐元数据。
- 媒体库（服务端）：[Plex](https://www.plex.tv/media-server-downloads)
  - Win、Mac、Linux、NAS、Docker、Android 等
- 播放器（客户端）：[Plexamp](https://www.plex.tv/plexamp/)
  - Win、Mac、Linux、iOS（支持 CarPlay）、Android、网页、树莓派/Armbian盒子
- 元数据管理：自动匹配 [Plex 网易云插件](https://github.com/timmy0209/WangYiYun.bundle)、增强匹配 [Music Tag Web 音乐标签](https://github.com/xhongc/music-tag-web)
- 多房间播放：我的另一个项目[Plexamp Cast](https://github.com/juneix/plexamp-cast)

## ⚠️ 注意事项
> 请各位大 UP、KOL 不要在国内自媒体、社群、论坛公开传播此项目。如果被盯上了，广大网友会谢谢你全家的。😅
- 由于某些你懂的原因，请确保你的 NAS 接入了国际互联网，解锁所有音源
- API 访问频率限制（动态更新）：5 分钟内不超 50 次请求
- 如果依然无法使用，请前往原作者站点查看原因

## 🧩 快速部署
Docker Compose 配置文件
⚡️ 已配置毫秒镜像加速，中国大陆地区专用
```
services:
  nas-music-kit:
    image: 1ms.run/ghcr.io/juneix/nas-music-kit
    container_name: nas-music-kit
    network_mode: host
    restart: unless-stopped
    environment:
      - PORT=8000 #自定义端口号
    volumes:
      - ./music:/music #映射你的 NAS 音乐文件夹
```
