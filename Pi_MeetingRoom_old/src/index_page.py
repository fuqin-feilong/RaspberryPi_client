from PyQt5 import QtWidgets, QtCore
from index import Ui_MainWindow
from update_thread import Update
from meeting_page import Meeting
import threading, time, datetime
import json


class Index(QtWidgets.QMainWindow):

    def __init__(self):
        super(Index, self).__init__()
        self.ui = Ui_MainWindow()
        self.resize(451, 254)
        #self.setFixedSize(self.width(), self.height())      # 禁止更改大小
        self.ui.setupUi(self)
        self.update_thread = Update(self)
        self.ui.pushButton.clicked.connect(self.room_config)
        self.ui.pushButton_2.clicked.connect(self.get_data)
        self.ui.pushButton_3.clicked.connect(self.stop_get_data)
        self.ui.pushButton_4.clicked.connect(self.exit)
        self.vedio = Meeting()
        self.series = ''
        self.room_id = ''
        self.meeting_list = []
        self.current_meeting = None  # 当前会议ID
        self.getConfig()
        self.update_thread.start()  # 启动多线程更新数据
        # self.meeting_thread = threading.Thread(target=self.get_meeting_status)
        # self.meeting_thread.start()
        self.timer = QtCore.QTimer()                            # 设置定时器
        self.timer.timeout.connect(self.get_meeting_status)
        self.timer.start(1000)                                  # 每隔1s执行一次get_meeting_status函数
        self.cap_is_open = False                                # 判断摄像头状态（打开/关闭）

    def room_config(self):
        dialog = QtWidgets.QInputDialog()
        text, ok = dialog.getText(self, 'Input Dialog', '更新会议室序列号:', text="1234")    # text设置默认值
        if ok:
            print("更新配置，会议室序列号更新为：", text)

    # 退出
    def exit(self):
        # 设置弹出框
        question = QtWidgets.QMessageBox.question(self, 'Extract', 'Do you really want to quit?',
                                                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if question == QtWidgets.QMessageBox.Yes:
            print("Closing app")
            self.close()
            # sys.exit()
        else:
            pass

    # 开启更新线程
    def get_data(self):
        self.update_thread.flag = 1
        self.start_meeting()                        # 打开摄像头，开始签到

    # 会议开始，开启摄像头签到
    def start_meeting(self):
        print("开启会议", type(self))
        try:
            self.current_meeting = self.meeting_list[0]['id']
            self.vedio.ui.label_3.setText(self.meeting_list[0]['title'])
            self.vedio.ui.label_4.setText(self.meeting_list[0]['sign_in_start_time'][11:16]+'-'+self.meeting_list[0]['sign_in_end_time'][11:16])
            self.vedio.meeting_id = self.current_meeting                    # 设置会议id
            self.vedio.video_widget.set_on_detect()       # 开始检测人脸
            self.vedio.show()                           # 打开人脸识别
            pass
        except Exception as e:
            print(e)

    # 关闭更新线程
    def stop_get_data(self):
        self.update_thread.flag = 0

    # 加载配置
    def getConfig(self):
        config_file_path = '../config/room.json'
        with open(config_file_path, 'r+') as f:
            config = f.read()
            config = json.loads(config)
        self.series = config['series']
        self.room_id = config['id']

    def get_meeting_status(self):
        print("更新会议状态")
        # 设置会议开始时间
        try:
            # 检测到会议时判断是否打开/关闭摄像头
            if len(self.meeting_list) > 0:
                start_time = self.meeting_list[0]['sign_in_start_time'][:16]            # 年月日 时分
                end_time = self.meeting_list[0]['sign_in_end_time'][:16]
                # start_time = '2020.4.11 15:42'
                # end_time = '2020.4.11 15:43'
                start_time = datetime.datetime.strptime(start_time, "%Y.%m.%d %H:%M")  # 设置开始时间
                end_time = datetime.datetime.strptime(end_time, "%Y.%m.%d %H:%M")    # 设置关闭时间
                now_time = datetime.datetime.now().strftime("%Y.%m.%d %H:%M")
                now_time2 = datetime.datetime.strptime(now_time, "%Y.%m.%d %H:%M")  # 当前时间
                if (now_time2 - start_time).seconds > 0 and not self.cap_is_open:                  # 当前时间等于会议开启时间
                    print(type(self))
                    self.start_meeting()
                    self.cap_is_open = True
                if (now_time2 - end_time).seconds < 0 and self.cap_is_open:                        # 当前时间等于会议关闭时间
                    self.vedio.exit()
                    self.cap_is_open = False
                    print("关闭会议")
            else:
                # 未检测到会议时不进行任何操作
                pass
        except Exception as e:
            print(e)


if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    index=Index()
    index.show()
    sys.exit(app.exec_())