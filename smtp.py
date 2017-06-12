#!/usr/bin/python
#coding=utf-8

import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr, parseaddr

from_addr = 'brrnpd@sina.com'
password = 'f33917'
smtp_server = 'smtp.sina.com'
to_addr = 'zhsecway@163.com'
subject = 'Test Mail'

#邮件对象
msg = MIMEMultipart()
msg['Subject'] = Header(subject, 'utf-8').encode()
msg['From'] = from_addr
msg['To'] = to_addr

#邮件正文是MIMEText
msg.attach(MIMEText('bdTEst', 'plain', 'utf-8'))

#添加附件就是加上一个MIMEBase，从本地读取一个文件
with open('/home/zcom/jmeter.log','r') as f:
    #设置附件的MIME和文件名，这里是log类型
    mime = MIMEBase('text', 'log', filename = 'jmeter.log')
    #加上必要的头信息：
    mime.add_header('Content-Disposition', 'attachment', filename = 'jmeter.log')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    #把附件的内容读进来
    mime.set_payload(f.read())
    #用Base64编码
    encoders.encode_base64(mime)
    #添加到MIMEMultipart:
    msg.attach(mime)

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
