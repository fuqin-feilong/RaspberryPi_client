from PyQt5.QtCore import QThread
import time, datetime
from server import Server_IP
import requests
import json
from meeting_page import Meeting


class Update(QThread):
    def __init__(self, window, parent=None):
        super(Update, self).__init__(parent)
        self.flag = 0                           # 默认关闭更新，当登录后启动数据获取
        self.window = window                    # 主线程
        self.meeing_list = []                   # 会议列表
        self.current_meeting = None             # 当前会议ID

    def run(self):
        while True:
            if self.flag == 1:
                self.heat()  # 心跳检测
                self.get_data()
                time.sleep(5)
            else:
                pass

    def stop(self):
        print("停止更新数据")
        self.flag = 0

    # 获取会议数据
    def get_data(self):
        print("正在获取数据")
        # 获取该会议室最近的两场会议
        data = {'room_id': self.window.room_id}
        url = Server_IP + '/meeting/get_meeting_for_room/'
        r = requests.post(url, data=data)
        response = r.content.decode('utf-8')
        response = json.loads(response)
        print(response)
        self.window.meeting_list = response['data']
        self.meeing_list = response['data']
        # self.window.ui.label.setText("Java开发者大会")
        if response['status'] == 1:
            self.setMeeting(response['data'])
            pass
        else:
            print("获取会议列表失败")
        # 检测会议是否开始
        # self.isMeetingStart()
        # self.isMeetingEnd()


    # 心跳检测机制
    def heat(self):
        data = {'room_id': self.window.room_id}
        url = Server_IP + '/meeting/heat/'
        r = requests.post(url, data=data)
        response = r.content.decode('utf-8')
        response = json.loads(response)
        print(response)

    # 设置会议显示
    def setMeeting(self, meeting_list):
        if len(meeting_list) == 0:              # 没有会议数据
            self.window.ui.label.setText("无数据")
            self.window.ui.label_2.setText("")
            self.window.ui.label_3.setText("无数据")
            self.window.ui.label_4.setText("")
        elif len(meeting_list) == 1:            # 只获取到一条数据
            self.window.ui.label.setText(meeting_list[0]['title'])
            self.window.ui.label_2.setText("会议签到时间："+meeting_list[0]['sign_in_start_time'][:16]+'-'+meeting_list[0]['sign_in_end_time'][11:16])
            self.window.ui.label_3.setText("无数据")
            self.window.ui.label_4.setText("")
        else:                                   # 获取到两条数据
            self.window.ui.label.setText(meeting_list[0]['title'])
            self.window.ui.label_2.setText("会议签到时间：" + meeting_list[0]['sign_in_start_time'][:16]+'-'+meeting_list[0]['sign_in_end_time'][11:16])
            self.window.ui.label_3.setText(meeting_list[1]['title'])
            self.window.ui.label_4.setText("会议签到时间：" + meeting_list[1]['sign_in_start_time'][:16]+'-'+meeting_list[1]['sign_in_end_time'][11:16])

    # 判断是否有开始的会议
    def isMeetingStart(self):
        now_time = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        now_time2 = datetime.datetime.strptime(now_time, "%Y.%m.%d %H:%M:%S")  # 当前时间
        start_time = self.meeing_list[0]['sign_in_start_time']
        start_time2 = datetime.datetime.strptime(start_time, "%Y.%m.%d %H:%M:%S")
        if (now_time2 - start_time2).days >=0:
            self.current_meeting = self.meeing_list[0]['id']
            self.window.current_meeting = self.meeing_list[0]['id']
            self.window.start_meeting()  # 开启会议签到
        else:
            print("会议"+ self.meeing_list[0]['title'] +"未开始")

    # 判断当前会议是否结束
    def isMeetingEnd(self):
        now_time = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        now_time2 = datetime.datetime.strptime(now_time, "%Y.%m.%d %H:%M:%S")  # 当前时间
        end_time = self.meeing_list[0]['sign_in_end_time']
        end_time2 = datetime.datetime.strptime(end_time, "%Y.%m.%d %H:%M:%S")
        if (now_time2 - end_time2).days >= 0:
            self.window.vidio.exit()                # 关闭签到，会议结束
        else:
            print("会议" + self.meeing_list[0]['title'] + "未开始")
