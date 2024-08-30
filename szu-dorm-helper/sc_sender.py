import os
import smtplib
from email.mime.text import MIMEText

import requests
from tabulate import tabulate

# 不用代理
os.environ['NO_PROXY'] = 'https://sc.ftqq.com/'


# 使用 Server酱 发送电量数据至微信
def send(key_url: str, data: list):
    # post请求
    requests.post(key_url, data=data)
    return


def handle(data: list, describe: str):
    text = '昨日用电{:.2f}度，剩余可用{:.2f}度'.format(data[-2]['cost'], data[-1]['rest'])
    # 表头
    desp = describe + '\n\n'
    # 出于Sever酱的markdown表格样式问题，首行表格空格为全角空格
    desp += ('|　日期　|　当日用电　|　可用电量　|　当日充电　|\n'
             '| :---: | :------: | :------: | :------: |\n')

    # 表格数据
    for line in data:
        for datum in line:
            # float数据控制小数点为两位
            if isinstance(line[datum], float):
                desp += '| {:.2f} '.format(line[datum])
            else:
                desp += '| {} '.format(line[datum])
        desp += '|\n'

    data = {
        'text': text,
        'desp': desp
    }

    return data


def email_handle(email_config: dict, data: list):
    # 第三方 SMTP 服务
    mail_host = email_config["mail_host"]  # 设置服务器
    mail_user = email_config["mail_user"]
    mail_pass = email_config["mail_pass"]
    receivers = email_config["receivers"]

    table_data = [['日期', '当日用电', '可用电量', '当日充电']]
    for da in data:
        tmp = []
        for datum in da:
            if isinstance(da[datum], float):
                tmp.append('{:.2f}'.format(da[datum]))
            else:
                tmp.append(da[datum])
        table_data.append(tmp)
    table_html = tabulate(table_data, headers="firstrow", tablefmt='html')

    # 邮件内容设置
    message = MIMEText(table_html, 'html', 'utf-8')
    # 邮件主题
    message['Subject'] = '昨日用电{:.2f}度，剩余可用{:.2f}度'.format(data[0]['cost'], data[0]['rest'])
    print(message['Subject'])
    # 发送方信息
    message['From'] = mail_user

    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        for receiver in receivers:
            message['To'] = receiver
            smtpObj.sendmail(
                mail_user, receiver, message.as_string()
            )
            print(f"邮件发送成功，收件人：{receiver}")
        # 退出
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误
    return
