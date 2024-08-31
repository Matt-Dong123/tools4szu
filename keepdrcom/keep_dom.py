import os
import time
import requests
from datetime import datetime


def login(username, password, ip):
    burp0_url = (
        f"http://172.30.255.42:801/eportal/portal/login?callback=dr1003&login_method=1&user_account=%2C0%2C{username}&user_password={password}&"
        f"wlan_user_ip={ip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.1.3&"
        f"terminal_type=1&lang=zh-cn&v=6275&lang=zh")
    burp0_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.141 Safari/537.36",
        "Accept": "*/*", "Referer": "http://172.30.255.42/", "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
    ret = requests.get(burp0_url, headers=burp0_headers)
    return ret.text


def getIP():
    os.environ['NO_PROXY'] = 'http://www1.szu.edu.cn/'
    burp0_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.141 Safari/537.36",
        "Accept": "*/*", "Referer": "http://172.30.255.42/", "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
    ret = requests.get('http://www1.szu.edu.cn/nc/speedtest/', headers=burp0_headers).text
    if '<font color="#D00000">1' not in ret:
        return None
    sl = ret.find('<font color="#D00000">1') + len('<font color="#D00000">1') - 1
    el = ret.find('<', sl)
    ret = ret[sl:el]
    return ret


if __name__ == '__main__':
    username = input('username:').strip()
    password = input('password:')
    during = 60
    print('正在自动获取ip')
    ip = getIP()
    if ip is None:
        ip = input('无法自动获取ip，请手动输入')
    else:
        print('自动获取ip成功，ip:', ip)
    os.system('cls')
    print('username:', username)
    print('password:', '*' * len(password))
    print('ip:', ip)
    while True:
        try:
            ip = getIP()
            ret = login(username, password, ip)
            print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '\t' + ret)
        except InterruptedError as e:
            exit(0)
        except Exception as e:
            print(e)
        finally:
            time.sleep(during)
