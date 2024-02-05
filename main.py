import sys

from PyQt6.QtWidgets import *

from MyApplication import MyApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApplication()
    sys.exit(app.exec())
