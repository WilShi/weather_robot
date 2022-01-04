#! -*- coding: utf-8 -*-
"""
Author: Wenbo Shi
Create type_time: 2021-12-27
Info: 定期向企业微信推送天气预报消息
"""
import requests, json
import datetime
import time
import sys


class Weather:
    def check_rain(self, precip):
        if float(precip) == 0:
            return "0.0 毫米 不会下雨，不用担心(￣︶￣)↗"
        return "{} 毫米 可能会下雨，需要带上雨伞！！！！\n☂☂☂☂☂☂☂☂☂☂☂☂☂\n☂☂☂☂☂☂☂☂☂☂☂☂☂\n☂☂☂☂☂☂☂☂☂☂☂☂☂".format(precip)

    def check_cool(self, temp):
        if float(temp) < 10:
            return "{} 摄氏度, 天气寒冷，外出注意保暖！！！！".format(temp)
        return "{} 摄氏度".format(temp)

    def get_weather(self, when="now"):
        """获取天气预报"""
        # 传参
        data = {
            "key": "6a8cd3e53f884f9fa928824d7982c3ee",
            "location": 101190101,
            "lang": "zh",
            "unit": "",
            "gzip": ""
        }
        c_now, c_h, c_m, c_s = SendMsg().get_current_time()

        # 播报明天的天气
        if when == "ahead":
            qweatherApi = "https://devapi.qweather.com/v7/weather/3d?"
            info = requests.get(qweatherApi, data)
            # print(info.text)
            if info.status_code == 200:
                jsonDoc = json.loads(info.text)
                if jsonDoc.get("code") == "200":
                    print("获得三天的天气")
                    updateTime = jsonDoc.get("updateTime", "获取失败!") # 获取时间
                    wealink = jsonDoc.get("fxLink", "获取失败!") # 详细链接
                    threeDays = jsonDoc.get("daily") # 三天的天气
                    tomorrow = jsonDoc.get("daily")[1] # 获取明天的天气
                    fxDate = tomorrow.get("fxDate", "获取失败!") # 预报的日期
                    textDay = tomorrow.get("textDay") # 文字描述天气
                    sunrise = tomorrow.get("sunrise", "获取失败!") # 日出时间
                    moonPhase = tomorrow.get("moonPhase", "获取失败!") # 月相名称
                    tempMax = tomorrow.get("tempMax") # 最高温度
                    tempMin = tomorrow.get("tempMin") # 最低温度
                    windSpeedDay = tomorrow.get("windSpeedDay") # 风力
                    precip = self.check_rain(tomorrow.get("precip")) # 降雨量

                    msg = "到点下班啦！！！！！！ \n当前时间：{}，\n明天的日期是：{} \n明天的天气：{} \n日出时间是：{} \n月相名称：{} \n最高温度：{} \n最低温度：{} \n风力：{} \n降雨量：{} \n如需查看具体天气信息可使用：{}".format(c_now, fxDate, textDay, sunrise, moonPhase, tempMax, tempMin, windSpeedDay, precip, wealink)
                    # print(msg)
                    return msg

            else:
                print("天气预报请求失败! T⌓T")
                return "天气预报请求失败! T⌓T"

        # 播报今天的天气
        else:
            qweatherApi = "https://devapi.qweather.com/v7/weather/now?"
            info = requests.get(qweatherApi, data)
            
            if info.status_code == 200:
                jsonDoc = json.loads(info.text)
                # print(jsonDoc)
                if jsonDoc.get("code") == "200":
                    print("得到当前的天气")
                    updateTime = jsonDoc.get("updateTime", "获取失败!")
                    wealink = jsonDoc.get("fxLink", "获取失败!")
                    temp = self.check_cool(jsonDoc["now"].get("temp"))
                    feelLike = "{} 摄氏度".format(jsonDoc["now"].get("feelsLike"))
                    des = jsonDoc["now"].get("text")
                    precip = self.check_rain(jsonDoc["now"].get("precip"))

                    msg = "当前时间: {}，\n南京的天气：{}\n气温是：{}\n体感温度为：{}\n降雨量：{}\n如需查看具体天气信息可使用：{}".format(c_now, des, temp, feelLike, precip, wealink)
                    return msg

            else:
                print("天气预报请求失败! T⌓T")
                return "天气预报请求失败! T⌓T"

class SendMsg:
    def get_current_time(self):
        """获取当前时间，当前时分秒"""
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hour = datetime.datetime.now().strftime("%H")
        mm = datetime.datetime.now().strftime("%M")
        ss = datetime.datetime.now().strftime("%S")
        return now_time, hour, mm, ss


    def sleep_time(self, hour, m, sec):
        """返回总共秒数"""
        return hour * 3600 + m * 60 + sec


    def send_msg(self, content, env):

        if env == "test":
            wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4e2e2326-3ade-451c-9168-e5ff545d5d31"  # 测试机器人
        else:
            wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=50da2f29-660a-4c46-8528-ac15620da25f"  # 蟒蛇机器人

        """艾特全部，并发送指定信息"""
        data = json.dumps({"msgtype": "text", "text": {"content": content, "mentioned_list":["@all"]}})
        try:
            requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
        except Exception as error:
            time.sleep(50)
            requests.post(wx_url, data, auth=('Content-Type', 'application/json'))


    def send_markdown(self, content, env):

        if env == "test":
            wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4e2e2326-3ade-451c-9168-e5ff545d5d31"  # 测试机器人
        else:
            wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=50da2f29-660a-4c46-8528-ac15620da25f"  # 蟒蛇机器人

        """艾特全部，并发送指定信息"""
        data = json.dumps({"msgtype": "markdown", "markdown": {"content": content, "mentioned_list":["@all"]}})
        r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
        print(r.json)


    def every_time_send_msg(self, interval_h=0, interval_m=0, interval_s=1, special_h="00", special_m="00", mode="special", env="test"):
        """每天指定时间发送指定消息"""

        # 设置自动执行间隔时间
        second = self.sleep_time(interval_h, interval_m, interval_s)
        print("执行每天{}时{}分定时发送...".format(special_h, special_m))

        # print("写入命令：")

        strat = 0

        # 死循环
        while True:
            # 获取当前时间和当前时分秒
            c_now, c_h, c_m, c_s = self.get_current_time()
            # print("当前时间：", c_now, c_h, c_m, c_s)

            if mode == "special":
                # print("执行每天{}时{}分定时发送...".format(special_h, special_m))

                if c_h == special_h and c_m == special_m and c_s == "00": # 早上
                    # 执行
                    print("正在发送...")
                    msg = Weather().get_weather("now") #获取当前的实时天气
                    self.send_msg("早上好！！！！ \n"+msg, env)

                elif c_h == "18" and c_m == "00" and c_s == "00": # 晚上下班
                    print("正在发送晚间预报...")
                    msg = Weather().get_weather("ahead") #获取明天天气
                    self.send_msg(msg, env)

                elif c_h == "11" and c_m == "55" and c_s == "00": # 中午吃饭
                    print("正在发送午饭提醒...")
                    msg = Weather().get_weather("now") #获取当前的实时天气
                    self.send_msg("到点吃饭啦 ١١(❛ᴗ❛) \n" + msg, env)

                elif strat == 0:
                    print("机器人开始运行\n将会发送信息至URL：{}".format(env))

                    msg = "欢迎使用蟒蛇机器人"
                    if env != "test":
                        self.send_msg(msg, "test")
                    # self.send_msg(msg, env)

                    self.send_msg("执行每天{}时{}分定时发送...".format(special_h, special_m), "test")
                    strat+=1

                elif c_m == "00" and c_s == "00": # 检测程序是否还在运行
                    msg = "当前时间：{}，程序还在正常运行...".format(c_now)
                    print(msg)
                    self.send_msg(msg, "test")


            else:
                print("等待")
                
            # print("每隔" + str(interval_h) + "小时" + str(interval_m) + "分" + str(interval_s) + "秒执行一次")
            # print("**"*50)
            # print("**"*50)
            # 延时
            time.sleep(second)


if __name__ == '__main__':


    if len(sys.argv) == 4:
        SendMsg().every_time_send_msg(special_h=str(sys.argv[2]), special_m=str(sys.argv[3]), mode="special", env=sys.argv[1])
    else:
        print({"error": 1, "msg": "python weatherRobot.py env special_h special_m"})

    # print(get_weather())
    # msg = get_weather("now")
    # send_msg("到点吃饭啦 ١١(❛ᴗ❛) \n" + msg)


