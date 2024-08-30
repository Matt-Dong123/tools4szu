# SZU 宿舍电量微信提醒

## 简介

1. 使用 python 简单获取深圳大学特定的宿舍电量情况。
2. 借助 [Server 酱](http://sc.ftqq.com) 将电量情况发送至微信上。或者使用邮件提醒。
3. 可配合开机自启动完成每日电量提醒功能。
4. 本项目由 [szu-dormitory-electricity-remind](https://github.com/ceynri/szu-electricity-reporter) 修改而来，感谢原作者。

<br/>

## 快速部署
在安装完必要的包，并设置好config后，可以在服务器上运行以下代码在后台静默执行
``` bash
nohup python -u main.py > log 2>&1 &
```

## 提醒内容

- 每日使用电量情况
- 每日剩余电量情况
- 近几日电量详表
- 每日购入电量情况

<br/>

## 效果

微信信息提醒：

![msg.jpg](https://i.loli.net/2019/10/22/9pOLRsrvIWe5Tqn.jpg)

详细数据：

![detail.jpg](https://i.loli.net/2019/10/22/H2w1zFVvcltLjA6.jpg)

<br/>

## 注意

- 项目简陋，仅为正好可用的程度，存在许多可以优化与改进的空间；
- 电量查询表单的更新存在延迟，如果 remind_time 设置了过早的时间，可能无法获取到前一天的电量情况；
- 本项目仅供学习使用，如因采用本项目产生的一切后果，均由使用人负责

<br/>

## 项目结构

- [main.py](main.py)  
  主程序，获得数据并计算电量的报表数值

- [crawler.py](crawler.py)  
  发送电量查询请求，并进行简单数据整理的代码

- [scsender.py](scsender.py)  
  通过 Server 酱 进行微信提醒，使用邮件进行提醒

<br/>

## 使用方法

注意：本脚本需要配置 config.json 文件的内容

必填参数含义：

| 参数名          | 含义               | 例子              |
|--------------|------------------|-----------------|
| room_name    | 宿舍房间号（下面有获取教程）   | "1101"          |
| room_id      | 宿舍楼栋 id（下面有获取教程） | "7596"          |
| client       | （含义不清楚，下面有获取教程）  | "192.168.84.87" |
| interval_day | 报表所要拉取的最近天数范围    | 14              |

选填参数含义：

| 参数名             | 含义                       | 例子                               |
|-----------------|--------------------------|----------------------------------|
| remind_daily    | 是否需要每日提醒（需要和 server 酱配合） | true                             |
| server_chan_key | server 酱的密钥，用于微信提醒       | "https://sc.ftqq.com/xxxxx.send" |
| remind_time     | 每日提醒的时间（单位：时，整数，范围 0~23） | 9                                |
| email_config    | 邮件发送设置                   | 一个具体的例子如下                        |

```json
"email_config": {
    "send_email": true,
    "mail_host": "smtp.qq.com",
    "mail_user": "test@qq.com",
    "mail_pass": "testpassword",
    "receivers": [
      "testemail@qq.com",
      "testemail2@qq.com"
    ]
  }
```


环境：深大校内网

1. 获取指定的宿舍信息。参数值获取途径（以 Chrome 浏览器 为例）：

   校内网环境，点击<kbd>F12</kbd>键或空白处`右键-检查`打开开发者工具，选择 Network
   选项卡，登录深大 [SIMS 电控网上查询系统](http://192.168.84.3:9090/cgcSims/)
   ，填写宿舍信息后，随便选择开始时间、结束时间、查询类型，点击查询，在开发者工具中选择 `selectList.do`
   文件（如果没有该条记录，则尝试刷新页面），查看它的 POST 请求参数。

   ![network.jpg](https://ftp.bmp.ovh/imgs/2019/09/2021ada6023d5368.jpg)

   将 config.json 文件内的配置对应地替换为图中红框所包含的 `client`、`roomId`、`roomName` 参数即可。

2. 如果需要启用邮件提醒功能，需要在 config.json 文件内配置 `email_config` 参数，具体配置方法见上文。
