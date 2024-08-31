# coding=utf-8
import os
import urllib.request
from urllib import parse
import time

debug = True
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Connection': 'keep-alive',
    'Host': 'drcom.szu.edu.cn',
    'Origin': 'https://drcom.szu.edu.cn',
    'Referer': 'https://drcom.szu.edu.cn/a70.htm'
}

data = {
    'DDDDD': '',  # 校园卡号
    'upass': '',  # 密码
    'R1': '0',
    'R2': '',
    'R6': '0',
    'para': '00',
    '0MKKey': '123456'
}
username = input('请输入校园卡号：')
password = input('请输入密码：')
data['DDDDD'] = username
data['upass'] = password
os.system('cls')
data = bytes(parse.urlencode(data), encoding='utf8')
request = urllib.request.Request(url='https://drcom.szu.edu.cn/a70.htm', headers=headers, data=data, method='POST')
network = urllib.request.Request(url='https://www.baidu.com')
error = True
while (1):
    try:
        status = urllib.request.urlopen(network, timeout=3)
        if status.reason == 'OK':
            if debug and error == True:
                print('网络在线中......')
                error = False
    except Exception:
        error = True
        if debug:
            print('可能网线未插好,正在重试......')
        if debug:
            print('{} 检测到断网,开始重连'.format(time.strftime("%d/%m/%Y %H:%M:%S")))
        try:
            response = urllib.request.urlopen(request)
            if response.reason == 'OK':
                body = response.read().decode('gb2312')
                if body.find('Drcom PC登陆成功页') > 0:
                    if debug:
                        print('登陆成功！')
                else:
                    if debug:
                        print('登陆失败,正在重试......')
            else:
                if debug:
                    print('可能响应协议变了,正在重试......')
        except Exception:
            if debug:
                print('可能网线未插好,正在重试......')
    time.sleep(5)
