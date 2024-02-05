import time

from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import *
from pynput import mouse
from pynput.mouse import Controller, Button


class Recorder(QThread):
    def __init__(self, text_browser, is_running=False):
        super().__init__()
        self._is_running = is_running
        self._text_browser = text_browser
        self._listener = mouse.Listener(on_click=self._on_click)
        self._list = []

    def resetMacroPath(self):
        self._list.clear()

    def set_running(self, is_running):
        print('is_running:', is_running)
        self._is_running = is_running
        if not self._is_running:
            plaintext = self._text_browser.toPlainText().split('\n')
            self._text_browser.clear()
            for index in range(0, len(plaintext)-2):
                self._text_browser.append(plaintext[index])

    def getRecord(self):
        return self._list

    def _on_click(self, x, y, button, pressed):
        if self._is_running:
            self._list.append({'button': button,
                              'x': x,
                              'y': y,
                              'pressed': pressed})
            self._text_browser.append(str({'button': button,
                                          'x': x,
                                          'y': y,
                                          'pressed': pressed}))

    def run(self):
        with self._listener:
            self._listener.join()


class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.input_btn = QPushButton('입력시작')
        self.macro_start_btn = QPushButton('매크로시작')
        self.text_browser = QTextBrowser()
        self.init_ui()
        self.recorder = Recorder(self.text_browser)
        self.recorder.start()

    def init_ui(self):
        self.input_btn.clicked.connect(self.input_toggled)
        self.input_btn.setCheckable(True)
        self.macro_start_btn.clicked.connect(self.macro_start)
        self.macro_start_btn.setCheckable(True)

        widget = QWidget()
        btnbox = QHBoxLayout()
        btnbox.addStretch(1)
        btnbox.addWidget(self.input_btn)
        btnbox.addWidget(self.macro_start_btn)
        btnbox.addStretch(1)

        layout = QGridLayout(widget)
        layout.addWidget(self.text_browser, 0, 0)
        layout.addLayout(btnbox, 1, 0)

        self.statusBar().showMessage('ready')
        self.setCentralWidget(widget)
        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('mouse macro made by python')
        self.show()

    def input_toggled(self, check):
        self.recorder.set_running(check)
        if check:
            self.recorder.resetMacroPath()
            self.input_btn.setText('입력종료')
            self.statusBar().showMessage('입력 중')
            self.text_browser.clear()
        else:
            self.input_btn.setText('입력시작')
            self.statusBar().showMessage('입력완료')

    def macro_start(self, check):
        if not self.input_btn.isChecked():
            if check:
                print('macro start click')
                mouse = Controller()
                list = self.recorder.getRecord()
                for i in range(0, len(list) - 2):
                    el = list[i]
                    print(el)
                    if el['pressed']:
                        continue
                    mouse.position = (el['x'], el['y'])
                    mouse.click(Button.left, 1)
                    time.sleep(0.5)
