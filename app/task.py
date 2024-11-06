from celery import Celery
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import smtplib

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

@celery_app.task(name="sendmail")
def send_activation_email(email, activation_code):
    print("Sending activation email")

    # SMTP configuration
    smtp_server = SMTPSERVER
    smtp_port = 465
    smtp_user = SMTPUSER
    smtp_password = SMTPPASSWORD

    sender_email = smtp_user
    receiver_email = email
    subject = 'Activate Your Account'

    # Convert activation_code to string
    activation_code_str = str(activation_code)

    # Email content with HTML for improved formatting
    html_content = f"""
    <html>
    <head>
        <style>
            .email-container {{
                font-family: Arial, sans-serif;
                color: #333333;
                background-color: #f9f9f9;
                padding: 20px;
                border: 1px solid #dddddd;
                max-width: 600px;
                margin: 0 auto;
                border-radius: 8px;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                color: white;
                background-color: #007BFF;
                border-radius: 5px;
                text-decoration: none;
            }}
            .footer {{
                font-size: 12px;
                color: #888888;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <h2>Welcome to Our Service!</h2>
            <p>Thank you for signing up. To activate your account, please use the code below:</p>
            <h3 style="color: #007BFF;">{activation_code_str}</h3>
            <p>Or, click the button below to activate your account:</p>
            <p><a href="https://yourdomain.com/activate?code={activation_code_str}" class="button">Activate Account</a></p>
            <p>If you did not request this email, please ignore it.</p>
            <div class="footer">
                <p>Best regards,</p>
                <p>Your Company Team</p>
                <p><a href="https://yourdomain.com">yourdomain.com</a></p>
            </div>
        </div>
    </body>
    </html>
    """

    # Fallback plain text version
    text_content = f"""
    Welcome to Our Service!
    
    Thank you for signing up. Your activation code is: {activation_code_str}

    Alternatively, you can activate your account by clicking on this link:
    https://yourdomain.com/activate?code={activation_code_str}
    
    Best regards,
    Your Company Team
    """

    # Build the message
    msg = MIMEMultipart("alternative")
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach both plain and HTML versions
    msg.attach(MIMEText(text_content, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))

    # Connect to SMTP server and send email
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


# @celery_app.task(name="sentmail")
# def send_activation_email(email, activation_code):
#     print("Sending activation email")
#     smtp_server = SMTPSERVER
#     smtp_port = 465
#     smtp_user = SMTPUSER
#     smtp_password = SMTPPASSWORD

#     sender_email = SMTPUSER
#     receiver_email = email
#     subject = 'Account Activation'
#     # Convert activation_code to string
#     activation_code_str = str(activation_code)

#     # 构建邮件内容
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject

#     body = f'Your activation code is: {activation_code_str}'
#     msg.attach(MIMEText(body, 'plain'))

#     # 连接到 SMTP 服务器并发送邮件
#     with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
#         server.login(smtp_user, smtp_password)
#         server.sendmail(sender_email, receiver_email, msg.as_string())