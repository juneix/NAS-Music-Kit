# NAS 音乐助手

本项目基于[GD 音乐台](https://music.gdstudio.org)提供的 API，我打包成了 Docker 容器，方便搜索歌曲，一键入库 NAS。  

如果有帮助到你，请顺手点个`🌟Star`支持一下，或者直接[🧧打赏鼓励](https://juneix.github.io/donate.webp)，感谢！

<img width="1780" height="1015" alt="demo" src="https://github.com/user-attachments/assets/43763cea-2129-4885-ac07-a1e8d5a0db3c" />

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
- 由于某些你懂的原因，建议让你的 NAS 接入国际互联网，解锁所有音源
- API 访问频率限制（动态更新）：5 分钟内不超 50 次请求
- 如果依然无法使用，请前往原作者站点查看原因

## 🧩 快速部署
Docker Compose 配置文件，各种 NAS 系统可一键抄作业，同时支持 `x86-64` 和 `arm64` 架构，自动识别。  

```yaml
services:
  nas-music-kit:
    # 毫秒镜像加速请换成 ghcr.1ms.run/ghcr.io/juneix/nas-music-kit
    image: ghcr.io/juneix/nas-music-kit
    container_name: nas-music-kit
    network_mode: host
    restart: unless-stopped
    environment:
      - PORT=8000 #自定义端口号
      # 如需访问国际互联网，请配置以下内容并取消注释
      # - HTTP_PROXY=http://10.1.1.4:9110
      # - HTTPS_PROXY=http://10.1.1.4:9110
      # - NO_PROXY=172.17.0.1,127.0.0.1,localhost
    volumes:
      # - /vol1/1000/music:/music # 飞牛示例
      # - /volume1/music:/music # 群晖示例
      - ./music:/music #映射你的 NAS 音乐文件夹
```
