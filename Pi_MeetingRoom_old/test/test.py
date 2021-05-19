# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QApplication
from Win_Fathar import Ui_MainWindow
from Win_Child import Ui_MainWindow as Ui_Child
import sys


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open)
        self.child = Child()

    def open(self):
        self.child.show()


class Child(QMainWindow, Ui_Child):
    def __init__(self):
        super(Child, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.exit)

    def exit(self):
        self.close()

    # def OPEN(self):
    #     self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    # ch = Child()
    main.show()
    # main.pushButton.clicked.connect(ch.OPEN)
    sys.exit(app.exec_())