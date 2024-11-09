# Celery_docker 部署Demo
该项目利用docker-python去部署celry，将Fastapi和Celery进行分离部署，使用同一个redis和rabbitmq，可以让后端api生成任务id，让celery-docker去执行

# 如何添加任务
在task.py文件中去添加自己的任务代码，如发送邮件，io操作

# Celery-beat
定时任务部署也可以新启动一个docker，按照上面的代码进行部署
