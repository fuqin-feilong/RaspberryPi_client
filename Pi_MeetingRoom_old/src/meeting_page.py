from PyQt5 import QtWidgets
from meeting import Ui_MainWindow
from capture import Capture, VideoWidget
import cv2
import uuid
import time
import requests
import json
import copy
from server import Server_IP
import os
#from mlx90614 import MLX90614
from time import sleep


class Meeting(QtWidgets.QMainWindow):

    def __init__(self):
        
        super(Meeting, self).__init__()
        self.ui = Ui_MainWindow()
        self.resize(490, 326)
        #self.setFixedSize(self.width(), self.height())
        self.capture = Capture()  # 设置摄像头组件
        self.video_widget = VideoWidget()  # 设置视频组件
        # image_window = self.video_widget.image_window           # 获取播放器组件的播放窗口
        # self.capture.image_data.connect(image_window)           # 播放器线程， 接收到摄像头数据时执行，在该函数中执行人脸检测及识别
        self.capture.image_data.connect(self.face_recognition)  # 播放器线程， 接收到摄像头数据时执行，在该函数中执行人脸检测及识别
        self.ui.setupUi(self)
        self.setCapture()
        self.setButtom()
        self.meeting_id = None
        #self.sensor = MLX90614()
        self.tem = 36.9
        self.fps= self.capture.get()

    def setCapture(self):
        # layout = QtWidgets.QVBoxLayout()                # 设置垂直布局
        # layout.addWidget(self.video_widget)             # 添加视频布局
        self.ui.horizontalLayout_2.addWidget(self.video_widget)
        self.capture.start_cap()                        # 开启摄像头

    def setButtom(self):
        self.ui.pushButton_4.clicked.connect(self.capture.save_cap)  # 按钮绑定事件
        self.ui.pushButton_3.clicked.connect(self.video_widget.set_on_detect)  # 按钮绑定事件
        self.ui.pushButton_2.clicked.connect(self.video_widget.set_off_detect)  # 按钮绑定事件
        self.ui.pushButton.clicked.connect(self.exit)  # 按钮绑定事件

    # 摄像头工作时自动执行
    def face_recognition(self, image_data):
        
        tmp_path = '../tmp'
        tmp_files = os.listdir(tmp_path)
        for tmp_file in tmp_files:
            try:
                os.remove(tmp_path + '/' + tmp_file)        # 删除不必要的临时图片
            except Exception as e:
                print(e)
        if (self.video_widget.if_face_detect == True):
            faces = self.video_widget.get_faces(image_data)
            if len(faces) > 0:
                for (x, y, w, h) in faces:  # 识别到人脸
                    copy_image_data = copy.deepcopy(image_data)
                    cv2.rectangle(image_data, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(image_data, str(int(self.fps)), (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    num=0
                    seconds=0.0
                    start=0.0
                    end=0.0
                    start = time.time()
                    while self.capture.isOpened():
                        # get a frame
                        
                        rval, frame = self.capture.read()
                        # save a frame
                        
                        #  frame = cv2.flip(frame,0)
                        # Start time
                        
                        #print(start)
                        #换成自己调用的函数
                        # End time
                        if(num==100):
                            end = time.time()
                            print(end-start)
                            seconds = end - start
                            print( "Time taken : {0} seconds".format(seconds))
                            fps  = 100 / seconds
                            print( "Estimated frames per second : {0}".format(fps))
                            break
                        # Time elapsed
                        
                        
                        # Calculate frames per second
                        
                        #bboxes_draw_on_img(frame,rclasses,rscores,rbboxes)
                        #print(rclasses)
                        #out.write(frame)
                        num=num+1
                        print(num)
                        #fps = cap.get(cv2.CAP_PROP_FPS)
                        #print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)) 
                        

                    # 读取图片并上传服务器
                    # print("识别出的人脸：", image_data.shape, type(image_data))
                    # if self.video_widget.face_count < 10:
                    #     self.video_widget.face_count += 1
                    #     self.video_widget.face_list.append(image_data)
                    # else:  # 10次人脸迭代，延长处理周期
                    #     file_name = str(uuid.uuid4()) + '.jpg'
                    #     file_path = '../tmp/' + file_name
                    #     cv2.imwrite(file_path, copy_image_data)  # 保存识别出来的人脸
                    #     files = {'file': (file_name, open(file_path, 'rb'), 'image/jpeg')}
                    #     data = {'meeting_id': self.meeting_id}
                    #     # data = json.dumps(data)
                    #     print(data)
                    #     url = Server_IP + '/meeting/get_user_by_face/'
                    #     print("网络请求地址：", url)
                    #     r = requests.post(url, data=data, files=files)
                    #     # 返回的结果为识别出的用户姓名和签到时间
                    #     time.sleep(2)  # 休眠2s，等待服务器返回结果
                    #     response = r.content.decode('utf-8')
                    #     response = json.loads(response)
                    #     print(response, type(response))
                    #     print(r.status_code)
                    #     if response['status'] == 1:
                    #         pass
                    #         self.ui.label_5.setText("姓名：" + response['user_name'])                   # 设置姓名
                    #         self.ui.label_6.setText("状态：" + response['message'])                   # 设置签到
                    #         self.ui.label_7.setText("时间：" + response['time'][10:16])                   # 设置签到时间
                    #         while self.tem > 50.0 or self.tem < 20.0:                             #设置体温
                    #             sleep(0.1)
                    #             #self.tem = self.sensor.get_obj_temp()
                    #             print(self.tem)
                    #         self.ui.label_8.setText(str("36.5")+"C体温正常")
                    #         self.ui.label_8.setStyleSheet("color:green")
                    #         if self.tem >= 37.5:
                    #             self.ui.label_8.setText("体温：" + str(self.tem)+" 体温异常")
                    #             self.ui.label_8.setStyleSheet("color:red")
                    #     self.video_widget.face_count = 0
                    #     self.video_widget.face_list = []

            else:
                # 未识别到人脸
                self.ui.label_5.setText("姓名：")  # 设置姓名
                self.ui.label_6.setText("状态：")  # 设置签到
                self.ui.label_7.setText("时间：")  # 设置签到时间
                self.ui.label_8.setText("体温：")  # 设置体温
        else:
            pass
        self.video_widget.image = self.video_widget.get_qimg(image_data)
        self.video_widget.setFixedSize(self.video_widget.image.size())
        self.video_widget.update()


    def exit(self):
        # 设置弹出框
        '''
        question = QtWidgets.QMessageBox.question(self, 'Extract', 'Do you want to close camera?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if question == QtWidgets.QMessageBox.Yes:
            print("Closing camera")
            # self.capture.cap.release()
            # cv2.destroyAllWindows()
            self.video_widget.set_off_detect()
            self.video_widget.face_count = 0
            self.video_widget.face_list = []
            self.close()
            # sys.exit()
        else:
            pass
        '''
        print("Closing camera")
        self.video_widget.set_off_detect()
        self.video_widget.face_count = 0
        self.video_widget.face_list = []
        self.close()
        # sys.exit()


if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    meeting=Meeting()
    meeting.show()
    sys.exit(app.exec_())
