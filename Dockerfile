# 使用官方 Python 镜像
FROM python:3.11

# 工作目录设为 /app
WORKDIR /app

# 复制依赖文件并安装依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有文件到工作目录
COPY ./app .

# 启用 unbuffered 输出，让日志将即时的输出，方便查看
ENV PYTHONUNBUFFERED 1

# 这里我们只是演示如何打包，不自动启动Celery
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]