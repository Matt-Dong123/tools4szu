# 研究生选课
import json
import os
import time

import requests

os.environ["no_proxy"] = "http://ehall.szu.edu.cn/"  # 不使用代理

# 只修改以下两个变量即可
cookie = ''  # 请填写你的cookie，字符串格式即可，会自动解析，例如：'JSESSIONID=xxxxxx; others=xxxxxx'
classList = ['20232-02027000-2703096-1704782958121', '20232-02027000-2703119-1704785821738']  # 请填写你要选的课程班级代码


'''
下方代码不要修改
下方代码不要修改
下方代码不要修改
'''
cookies = {}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://ehall.szu.edu.cn',
    'Referer': 'https://ehall.szu.edu.cn/yjsxkapp/sys/xsxkapp/xsxkHome/gotoChooseCourse.do',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def chooseCourse(classID):
    ret = requests.post(
        'https://ehall.szu.edu.cn/yjsxkapp/sys/xsxkapp/xsxkCourse/choiceCourse.do',
        cookies=cookies,
        headers=headers,
        data={"bjdm": classID, "lx": "0"},
    )
    return ret


def loadStdCourseInfo():
    ret = requests.post(
        'https://ehall.szu.edu.cn/yjsxkapp/sys/xsxkapp/xsxkCourse/loadStdCourseInfo.do',
        cookies=cookies,
        headers=headers,
    )
    courses = json.loads(ret.text)['results']
    courses.reverse()
    print('====================选课结果====================')
    for course in courses:
        print(f"班级代码：{course['BJDM']}, 课程名称：{course['KCMC']}, 任课教师：{course['RKJS']} ")
    return ret


def serverCurrentTime():
    ret = requests.get(
        'https://ehall.szu.edu.cn/yjsxkapp/sys/xsxkapp/xsxkHome/loadPublicInfo.do',
        cookies=cookies,
        headers=headers,
    )
    return json.loads(ret.text)['dqsj']


def loadStuInfo():
    ret = requests.get(
        'https://ehall.szu.edu.cn/yjsxkapp/sys/xsxkapp/xsxkHome/loadStdInfo.do',
        cookies=cookies,
        headers=headers,
    )
    info = json.loads(ret.text)
    print('====================学生信息====================')
    print(f"学号：{info['XH']}, 姓名：{info['XM']}")
    print(f"{info['YXMC']}  {info['ZYMC']}")
    return ret


successList = []

if __name__ == '__main__':
    try:
        cookie_list = cookie.split(';')
        for item in cookie_list:
            item = item.strip()
            items = item.split('=')
            cookies[items[0]] = items[1]
    except Exception as e:
        print(f'Parsing cookie failed {e}')
        exit(-1)

    print(f"当前服务器时间：{serverCurrentTime()}")
    loadStuInfo()
    print('====================开始选课====================')
    while True:
        if len(successList) == len(classList):
            print('全部选课成功')
            break
        for course in classList:
            if course in successList:
                print(f'{course} 已选中')
                continue
            try:
                print(course, end=' ')
                data = chooseCourse(course)
                if data.status_code != 200:
                    print(data.text)
                    print('status_code:', data.status_code)
                    exit(0)
                if json.loads(data.text)['code'] == 1:
                    successList.append(course)
                    print(data.text + ' 选课成功')
                else:
                    print(data.text)
            except KeyboardInterrupt as e:
                print('KeyboardInterrupt')
                exit(0)
            except Exception as e:
                print(f'Exception occurred! {e}')
            time.sleep(0.5)
    loadStdCourseInfo()
