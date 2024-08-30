# xxt_autosign
a tool for xxt app to signup without qrcode time limitation


学习通无视二维码过期时间，无视不显示邀请码批量签到脚本。
只需要一个二维码（过期的也可以），即可实现批量给多人签到。

1. 用https://cli.im/deqr/other 扫描二维码，获取activeId
2. 将需要签到的人的姓名和学号写入user.csv，注意第一行为表头，不要修改。接下来每一行为一个人的姓名和学号，用英文逗号隔开。
3. 运行脚本进行签到
4. 可以进入https://mobilelearn.chaoxing.com/widget/sign/end_sign?activeId={} (大括号换成activeId) 查看签到结果
5. 本项目仅供学习，使用本工具造成的一切后果均由脚本使用者负责，开发者不承担任何责任。
