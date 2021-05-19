import sys
import cv2
from capture import QtWidgets, Capture, VideoWidget
from PyQt5 import QtWidgets as Widgets, QtGui


class Window(QtWidgets.QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setGeometry(100, 100, 600, 600)                # 起始位置，宽高
        self.setWindowTitle("VideoStreamApp")               # 设置标题
        #self.setWindowIcon(QtGui.QIcon('opencvlogo.png'))
        self.capture = Capture()                            # 设置摄像头组件
        self.video_widget = VideoWidget()                   # 设置视频组件
        image_window = self.video_widget.image_window       # 获取播放器组件的播放窗口
        self.capture.image_data.connect(image_window)       # 将系统消息绑定到播放器窗口
        self.add_buttons()          # 窗口初始化时设置按钮
        self.set_layout()           # 窗口初始化时设置布局

    # 设置布局
    def set_layout(self):
        buttons_layout = QtWidgets.QHBoxLayout()  # 在水平的方向上排列控件 左右排列
        buttons_layout.addWidget(self.start_cap_button)  # 在布局中添加按钮
        buttons_layout.addWidget(self.close_cap_button)
        buttons_layout.addWidget(self.save_cap_button)
        buttons_layout.addWidget(self.face_detect_on_button)
        buttons_layout.addWidget(self.face_detect_off_button)
        buttons_layout.addWidget(self.quit_app_button)

        layout = QtWidgets.QVBoxLayout()  # 设置垂直布局
        layout.addLayout(buttons_layout)  # 添加按钮的布局
        layout.addWidget(self.video_widget)  # 添加视频布局

        self.setLayout(layout)  # 设置整体布局


    # 设置按钮
    def add_buttons(self):
        self.start_cap_button = QtWidgets.QPushButton("Start capture")              # 开始拍照按钮定义
        self.close_cap_button = QtWidgets.QPushButton("Close capture")              # 关闭摄像头定义
        self.face_detect_on_button = QtWidgets.QPushButton("Face detection on")     # 启动人脸检测按钮定义
        self.face_detect_off_button = QtWidgets.QPushButton("Face detection off")   # 关闭人脸检测按钮定义
        self.quit_app_button = QtWidgets.QPushButton("Quit app")                    # 退出程序定义
        self.save_cap_button = QtWidgets.QPushButton("Save capture")                # 保存图片定义

        self.start_cap_button.clicked.connect(self.start_cap)               # 按钮绑定事件
        self.close_cap_button.clicked.connect(self.end_cap)                 # 关闭摄像头
        self.quit_app_button.clicked.connect(self.close_app)
        self.save_cap_button.clicked.connect(self.capture.save_cap)                     # 保存拍照的按钮
        self.face_detect_on_button.clicked.connect(self.video_widget.set_on_detect)     # 开始检测
        self.face_detect_off_button.clicked.connect(self.video_widget.set_off_detect)   # 停止检测

    # 开启摄像头
    def start_cap(self):
        self.capture.start_cap()

    # 关闭摄像头
    def end_cap(self):
        self.capture.end_cap()
        # self.video_widget.close_video()

    # 关闭应用
    def close_app(self):
        # 设置弹出框
        question = QtWidgets.QMessageBox.question(self, 'Extract', 'Do you want to close camera?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if question == QtWidgets.QMessageBox.Yes:
            print("Closing camera")
            self.capture.cap.release()
            cv2.destroyAllWindows()
            self.close()
            # sys.exit()
        else:
            pass


    
