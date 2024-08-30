import datetime
import json
import time

import crawler
import sc_sender


def getConfig():
    with open('config.json', encoding='utf-8') as f:
        config = json.load(f)
    return config


# main函数
def main():
    # 获取配置
    config = getConfig()
    room_name = config['room_name']
    room_id = config['room_id']
    client = config['client']
    interval_day = config['interval_day']
    sc_key = config['server_chan_key']
    remind_daily = config['remind_daily']
    remind_time = config['remind_time']
    email_config = config['email_config']

    if room_name == '' or room_id == '':
        print('[error] 未配置config.json!')
        exit()
    # 获得数据
    table_data = crawler.crawlData(client, room_name, room_id, interval_day)
    if len(table_data) == 0:
        print('[爬取数据失败，请检查是否能访问电费查询网站"http://192.168.84.3:9090/cgcSims/"]')
        exit()
    print('[爬取数据结束]')

    # 处理数据
    data = processingData(table_data)[::-1]
    print('[数据处理结束]')
    # 在控制台格式化输出爬虫获得的数据
    printData(data)

    if email_config['send_email']:
        sc_sender.email_handle(email_config, data)
        print('[已发送至邮箱]')

    # 若 sc_key 存在，则发送微信提醒
    if sc_key != '':
        # describe参数内容会添加到内容详情最前端
        describe = f'ᶘ ᵒᴥᵒᶅ {room_name}电量查询'
        # 处理数据为要发送的表格格式信息
        send_msg = sc_sender.handle(data, describe)
        # 发送信息
        sc_sender.send(
            key_url=sc_key,
            data=send_msg,
        )
        print('[已发送至微信]')

    if remind_daily is False or sc_key == '':
        exit()
    today_date = datetime.date.today()
    next_day_date = today_date + datetime.timedelta(days=1)
    next_exec_time = datetime.datetime.combine(
        next_day_date, datetime.time(hour=remind_time)
    )
    delta_time = (next_exec_time - datetime.datetime.now()).total_seconds()
    print(f'下次查询电量的时间：{next_exec_time}')
    time.sleep(delta_time)


# 加工数据获得想要的数据格式
def processingData(table_data: list):
    data = []
    day_num = len(table_data)

    # 日期 | 当日用电量
    for i in range(1, day_num):
        charge = table_data[i][3] - table_data[i - 1][3]
        data.append({
            'date': table_data[i][0],
            'cost': table_data[i - 1][1] - table_data[i][1],
            'rest': table_data[i][1],
            'charge': charge
        })
        if charge != 0:
            data[-1]['cost'] += charge  # 充了电，则需要修正耗电计算公式问题
        else:
            data[-1]['charge'] = '-'  # 没充电费

    # # 最后一天需要单独赋值
    # data.append({
    #     'date': table_data[day_num - 1][0],
    #     'cost': '-',
    #     'rest': table_data[day_num - 1][1],
    #     'charge': '-'
    # })

    return data


# 格式化输出爬虫获得的数据
def printData(data: list):
    print('日期'.ljust(8, ' '), '当日用电'.ljust(8, ' '), '可用电量'.ljust(8, ' '), '当日充电'.ljust(8, ' '))
    for row in data:
        for datum in row:
            value = row[datum]
            if isinstance(value, float):
                value = '{:.2f}'.format(value)
            print(value.ljust(12, ' '), end='')
        print()
    return


if __name__ == '__main__':
    while True:
        main()
