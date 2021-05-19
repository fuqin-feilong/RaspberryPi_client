from PyQt5.QtWidgets import QApplication
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from index import Ui_MainWindow


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_widget = Ui_MainWindow()
    main_widget.setupUi(main_window)
    # main_window.setCentralWidget(main_widget)
    main_window.show()
    sys.exit(app.exec_())


