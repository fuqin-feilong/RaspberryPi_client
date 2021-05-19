# 这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame, QApplication, QMessageBox)
from PyQt5.QtGui import QColor


class Index(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(300, 300)

        comfire = QPushButton('确定', self)
        comfire.setCheckable(True)
        comfire.move(10, 10)

        comfire.clicked[bool].connect(self.input_series)
        self.setWindowTitle('会议室签到管理系统')
        self.show()

    def input_series(self, pressed):
        QMessageBox.question(self, "提问对话框", "你要继续搞测试吗？", QMessageBox.Close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Index()
    sys.exit(app.exec_())
