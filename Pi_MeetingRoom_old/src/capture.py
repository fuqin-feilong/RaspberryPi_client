import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui
import uuid
import time
import requests
import json
from server import Server_IP


class Capture(QtCore.QThread):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.cap = cv2.VideoCapture(camera_port)
        self.cap.set(3, 309)                        # 设置摄像头的宽
        self.cap.set(4, 249)                        # 设置摄像头的高
        self.timer = QtCore.QBasicTimer()
        self.fps=0
    def get(self):
        fps=self.cap.get(cv2.CAP_PROP_FPS)
        return fps
    def read(self):
        return self.cap.read()
    def start_cap(self):
        print('Start capture')
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return
        ret, frame = self.cap.read()
        if ret:
            self.image_data.emit(frame)

    def end_cap(self):
        print("Ending capture")
        self.timer.stop()
        self.cap.release()
    def isOpened(self):
        return self.cap.isOpened()

    def save_cap(self):
        print("Saving capture")
        _, frame = self.cap.read()
        file_name = '../saved_images/img_' + str(uuid.uuid4()) + '.png'
        cv2.imwrite(file_name, frame)


class VideoWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, file_path='../haarcascade_frontalface_default.xml'):
        super().__init__(parent)
        self.image = QtGui.QImage()
        self.face_cascade = cv2.CascadeClassifier(file_path)
        self.if_face_detect = False
        self.face_count = 0  # 收集的识别的人脸次数
        self.face_list = []  # 收集识别的人脸

    # 摄像头工作时自动执行
    def image_window(self, image_data):
        if (self.if_face_detect == True):
            faces = self.get_faces(image_data)
            for (x, y, w, h) in faces:                                                  # 识别到人脸
                cv2.rectangle(image_data, (x, y), (x + w, y + h), (0, 255, 0), 2)
               
                # 读取图片并上传服务器
                print("识别出的人脸：", image_data.shape, type(image_data))
                if self.face_count < 10:
                    self.face_count += 1
                    self.face_list.append(image_data)
                else:                                                                     # 10次人脸迭代，延长处理周期
                    file_name = str(uuid.uuid4()) + '.jpg'
                    file_path = '../tmp/' + file_name
                    cv2.imwrite(file_path, image_data)                                      # 保存识别出来的人脸
                    files = {'file':(file_path, open(file_name, 'rb'), 'image/jpeg')}
                    data = {'room_id': '1', 'meeting_id': '1'}
                    # data = json.dumps(data)
                    print(data)
                    url = Server_IP + '/meeting/face_recognition/'
                    print("网络请求地址：", url)
                    r = requests.post(url, data=data, files=files)
                    # 返回的结果为识别出的用户姓名和签到时间
                    time.sleep(2)  # 休眠2s，等待服务器返回结果
                    print(r.content.decode('utf-8'))
                    print(r.status_code)
                    self.face_count = 0
                    self.face_list = []

        else:
            pass
        self.image = self.get_qimg(image_data)
        self.setFixedSize(self.image.size())
        self.update()

    def get_faces(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # working better with gray imgs
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces

    def get_qimg(self, image):
        h, w, ch = image.shape
        bytesPerLine = 3 * w
        image = QtGui.QImage(image.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def set_on_detect(self):
        self.if_face_detect = True

    def set_off_detect(self):
        self.if_face_detect = False
        self.face_count = 0
        self.face_list = []



