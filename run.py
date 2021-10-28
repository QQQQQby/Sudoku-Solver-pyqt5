import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

from gui import Ui_MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    MainWindow.setWindowIcon(QIcon('icon.ico'))
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
