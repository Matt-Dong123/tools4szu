import requests
import csv
import random
import time


def xxt_signin(activeId, puid, name, stuid):
    url = "http://mobilelearn.chaoxing.com:80/widget/sign/signIn"
    request_data = {
        'activeId': str(activeId),
        'puid': str(puid),
        '_from': '',
        'ignoreEwnCode': '1',
        'forminfo': str([{"name": "姓名", "must": 1, "value": name}, {"name": "学号", "must": 1, "value": stuid}])
    }
    request_headers = {"Upgrade-Insecure-Requests": "1",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                       "Referer": "https://mobilelearn.chaoxing.com/widget/sign/signIn",
                       "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9",
                       "Connection": "close"
                       }
    data = requests.get(url, params=request_data, headers=request_headers)
    return data.text


if __name__ == '__main__':
    '''
    学习通无视二维码过期时间，无视不显示邀请码签到脚本。
    1. 用https://cli.im/deqr/other扫描二维码，获取activeId
    2. 将需要签到的人的姓名和学号写入user.csv，注意第一行为表头，不要修改。接下来每一行为一个人的姓名和学号，用英文逗号隔开。
    3. 运行脚本进行签到
    4. 可以进入https://mobilelearn.chaoxing.com/widget/sign/end_sign?activeId={} (大括号换成activeId)查看签到结果    
    '''
    activeId = 13953107
    user = []
    with open('user.csv', 'r') as f:
        for row in csv.DictReader(f, skipinitialspace=True, delimiter=','):
            user.append(row)
    print(f'共有{len(user)}个用户')
    for u in user:
        print(u['name'], u['stuid'])
    print('\n开始签到')
    for usr in user:
        response = xxt_signin(activeId, 100769212 + random.randint(0, 50000000), usr['name'], usr['stuid'])
        if '<title>签到成功</title>' in response:
            print('{} {} 签到成功'.format(usr['name'], usr['stuid']))
        else:
            print('{} {} 签到失败'.format(usr['name'], usr['stuid']))
        time.sleep(random.randint(0, 5))
    print('签到结束,请访问下面的链接查看签到结果')
    print(f'https://mobilelearn.chaoxing.com/widget/sign/end_sign?activeId={activeId}')
