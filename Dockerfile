FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建音乐下载目录
RUN mkdir -p /music

# 暴露端口 (将被 docker-compose 覆盖，但保留作为文档)
EXPOSE 8000

# 确保日志直接输出
ENV PYTHONUNBUFFERED=1

# 使用 Gunicorn 启动，4个 worker，绑定到指定端口，日志级别为 info
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT:-8000} --access-logfile - --error-logfile - app:app"]
