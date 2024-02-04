import sys

from PyQt6.QtWidgets import *


class MyApplication(QMainWindow):
    def __init__(self, macro):
        super().__init__()
        self.macro = macro
        self.input_btn = QPushButton('입력시작')
        self.statusbar = self.statusBar()
        self.init_ui()

    def init_ui(self):
        self.input_btn.setCheckable(True)
        self.input_btn.clicked.connect(self.input_toggled)
        macro_start_btn = QPushButton('매크로시작')
        macro_start_btn.clicked.connect(self.macro_start)
        text_browser = QTextBrowser()

        widget = QWidget()
        btnbox = QHBoxLayout()
        btnbox.addStretch(1)
        btnbox.addWidget(self.input_btn)
        btnbox.addWidget(macro_start_btn)
        btnbox.addStretch(1)

        layout = QGridLayout(widget)
        layout.addWidget(text_browser, 0, 0)
        layout.addLayout(btnbox, 1, 0)

        self.statusbar = self.statusBar().showMessage('ready')
        self.setCentralWidget(widget)
        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('mouse macro made by python')
        self.show()

    def input_toggled(self, check):
        if check:
            self.input_btn.setText('입력종료')
            self.statusbar = self.statusBar().showMessage('입력 중')
        else:
            self.input_btn.setText('입력시작')
            self.statusbar = self.statusBar().showMessage('입력완료')

    def macro_start(self):
        print('macro start click')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApplication()
    sys.exit(app.exec())
