# NAS 音乐助手

本项目基于[GD音乐台](https://music.gdstudio.org)的API，我打包成了 docker 镜像，方便搜索歌曲，一键入库 NAS。

## ⚠️ 注意事项
- 由于某些你懂的原因，请确保你的 NAS 接入了国际互联网，解锁所有音源。
- API 访问频率限制（动态更新）：5分钟内不超50次请求
- 如果依然无法使用，请前往原作者站点查看原因。

## 🧩 快速部署
docker compose 配置文件
```
services:
  nas-music-kit:
    image: ghcr.io/juneix/nas-music-kit
    container_name: nas-music-kit
    network_mode: host
    restart: unless-stopped
    environment:
      - PORT=8000 #自定义端口号
    volumes:
      - ./music:/music #映射你的 NAS 音乐文件夹
```
