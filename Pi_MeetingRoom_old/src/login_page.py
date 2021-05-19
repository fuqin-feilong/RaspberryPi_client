from PyQt5 import QtWidgets
from login import Ui_Form
from index_page import Index
import json
from server import Server_IP
import requests


class Login(QtWidgets.QWidget):

    def __init__(self):
        super(Login, self).__init__()
        self.ui = Ui_Form()
        self.resize(507, 249)
        self.setFixedSize(self.width(), self.height())
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.login)
        self.series = ''
        self.room_id = ''
        self.auto_login()  # 自动登录

    # 绑定会议室序列号，并执行登录
    def login(self):
        print("绑定会议室")
        self.series = self.ui.lineEdit.text()           # 得到输入的值
        response = self.verify_series(self.series, verify_type=0)     # 验证输入的序列号
        print(response)
        if response['status'] == 1:
            self.room_id = response['room_id']
            # 保存配置
            config = {}
            config['series'] = self.series
            config['id'] = self.room_id
            config_file_path = '../config/room.json'
            with open(config_file_path, 'w+') as f:
                config = f.write(json.dumps(config))        # 写入配置文件
            index.get_data()                                # 开启更新检测
            index.show()                                    # 页面跳转
            self.close()
        else:
            # 使用infomation信息框
            QtWidgets.QMessageBox.information(self, "绑定失败", response['message'],  QtWidgets.QMessageBox.Close)

    def auto_login(self):
        config_file_path = '../config/room.json'
        with open(config_file_path, 'r+') as f:
            config = f.read()
            config = json.loads(config)
        if config['series'] == '':
            pass
        else:
            # 验证序列号
            self.series = config['series']
            self.ui.lineEdit.setText(self.series)               # 读取当前配置
            self.room_id = config['id']
            # 向后台请求数据，验证序列号
            # response = self.verify_series(self.series, verify_type=1, room_id=self.room_id)
            # print(response)
            # if response['status'] == 1:     # 验证通过
            #     self.close()
            #     index.show()                # 执行自动登录
            # else:
            #     QtWidgets.QMessageBox.information(self, "验证失败", response['message'], QtWidgets.QMessageBox.Close)

    # 验证/绑定序列号
    def verify_series(self, series, verify_type, room_id=None):                 # verify_type为验证类型，为0时绑定， 为1时验证
        data = {'series': series, 'room_id': room_id, 'type':  verify_type}
        url = Server_IP + '/meeting/verify_series/'
        r = requests.post(url, data=data)
        response = r.content.decode('utf-8')
        response = json.loads(response)
        return response


if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    index = Index()
    login = Login()
    login.show()
    sys.exit(app.exec_())
