from celery import Celery
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

db_password = os.getenv("REDIS_DB_PASSWORD")
redis_host = os.getenv("REDIS_DB_HOSTNAME")
redis_port = os.getenv("REDIS_DB_PORT")
redis_db = os.getenv("REDIS_DB_NAME")
redis_user = os.getenv("REDIS_USER_NAME")

mq_password = os.getenv("MQ_USERPASSWORD")
mq_username = os.getenv("MQ_USERNAME")
mq_host = os.getenv("MQ_HOSTNAME")
mq_dbname = os.getenv("MQ_DBNAME")
mq_port = os.getenv("MQ_DBPORT")

SMTPSERVER = os.getenv("SMTPSERVER")
SMTPPORT = os.getenv("SMTPPORT")
SMTPUSER = os.getenv("SMTPUSER")
SMTPPASSWORD = os.getenv("SMTPPASSWORD")


celery_app = Celery('task', broker=f'amqp://{mq_username}:{mq_password}@{mq_host}:{mq_port}/{mq_dbname}',
                    backend=f'redis://:{db_password}@{redis_host}:{redis_port}/{redis_db}')

@celery_app.task
def add(x, y):
    return x + y


@celery_app.task(name="sentmail")
def send_activation_email(email, activation_code):
    print("Sending activation email")
    smtp_server = SMTPSERVER
    smtp_port = 465
    smtp_user = SMTPUSER
    smtp_password = SMTPPASSWORD

    sender_email = SMTPUSER
    receiver_email = email
    subject = 'Account Activation'
    # Convert activation_code to string
    activation_code_str = str(activation_code)

    # 构建邮件内容
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    body = f'Your activation code is: {activation_code_str}'
    msg.attach(MIMEText(body, 'plain'))

    # 连接到 SMTP 服务器并发送邮件
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())