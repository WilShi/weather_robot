#! -*- coding: utf-8 -*-
"""
Author: Wenbo Shi
Create type_time: 2021-12-27
Info: 定期向企业微信推送天气预报消息
"""
import requests, json
import datetime
import time

# wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4e2e2326-3ade-451c-9168-e5ff545d5d31"  # 测试机器人

wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=50da2f29-660a-4c46-8528-ac15620da25f"  # 蟒蛇机器人

def get_weather():
    """获取天气预报"""
    qweatherApi = "https://devapi.qweather.com/v7/weather/now?"
    data = {
        "key": "6a8cd3e53f884f9fa928824d7982c3ee",
        "location": 101190101,
        "lang": "zh",
        "unit": "",
        "gzip": ""
    }

    info = requests.get(qweatherApi, data)
    
    if info.status_code == 200:
        jsonDoc = json.loads(info.text)
        # print(jsonDoc)
        if jsonDoc.get("code") == "200":
            print("得到天气")
            updateTime = jsonDoc.get("updateTime", "获取失败!")
            wealink = jsonDoc.get("fxLink", "获取失败!")
            temp = "{} 摄氏度".format(jsonDoc["now"].get("temp"))
            feelLike = "{} 摄氏度".format(jsonDoc["now"].get("feelsLike"))
            des = jsonDoc["now"].get("text")
            c_now, c_h, c_m, c_s = get_current_time()
            msg = "当前时间: {}，\n南京的天气是：{}\n气温是：{}\n体感温度为：{}\n如需查看具体天气信息可使用：{}".format(c_now, des, temp, feelLike, wealink)
            print(msg)
            return msg

    else:
        print("天气预报请求失败! T⌓T")
        return "天气预报请求失败! T⌓T"


def get_current_time():
    """获取当前时间，当前时分秒"""
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hour = datetime.datetime.now().strftime("%H")
    mm = datetime.datetime.now().strftime("%M")
    ss = datetime.datetime.now().strftime("%S")
    return now_time, hour, mm, ss


def sleep_time(hour, m, sec):
    """返回总共秒数"""
    return hour * 3600 + m * 60 + sec


def send_msg(content):
    """艾特全部，并发送指定信息"""
    data = json.dumps({"msgtype": "text", "text": {"content": content, "mentioned_list":["@all"]}})
    r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
    print(r.json)


def every_time_send_msg(interval_h=0, interval_m=0, interval_s=10, special_h="00", special_m="00", mode="special"):
    """每天指定时间发送指定消息"""

    # 设置自动执行间隔时间
    second = sleep_time(interval_h, interval_m, interval_s)

    # 死循环
    while 1 == 1:
        # 获取当前时间和当前时分秒
        c_now, c_h, c_m, c_s = get_current_time()
        print("当前时间：", c_now, c_h, c_m, c_s)

        msg = get_weather() #获取当前的实时天气

        if mode == "special":
            if c_h == special_h and c_m == special_m:
                # 执行
                print("正在发送...")
                send_msg(msg)
        elif c_h == "07" and c_m == "30":
            send_msg(msg)
        else:
            print("等待")
            # send_msg(msg)
            
        print("每隔" + str(interval_h) + "小时" + str(interval_m) + "分" + str(interval_s) + "秒执行一次")
        # 延时
        time.sleep(second)


if __name__ == '__main__':

    every_time_send_msg(mode="no")


