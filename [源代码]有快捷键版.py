import time
import threading
import pynput.mouse  
from pynput.keyboard import Key, Listener
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QRadioButton, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal

LEFT = 0
RIGHT = 1

class MouseClick(QObject):
    started = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, button, time):
        super().__init__()
        self.mouse = pynput.mouse.Controller()
        self.running = False  
        self.time = time
        self.button = button
        self.listener = Listener(on_press=self.key_press)
        self.listener.start()

    def key_press(self, key):
        if key == Key.f8:
            if self.running:
                self.running = False
                self.stopped.emit()
            else:
                self.running = True
                self.started.emit()
        elif key == Key.esc:
            self.listener.stop()
            self.stopped.emit()

    def mouse_click(self):
        while self.running:
            self.mouse.click(self.button)
            time.sleep(self.time)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.strings = {}  # 添加strings属性
        self.language = "English"  # 设置默认语言为英文
        self.initUI()
        self.update_language()  # 初始化界面时更新语言

    def initUI(self):
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle('Mouse Clicker [with Hotkeys]')
        self.setWindowIcon(QIcon('icon.ico'))  # 设置窗口图标，将 'icon.png' 替换为你的图标文件路径

        self.mouse = LEFT

        self.lab1 = QLabel(self)
        self.lab1.move(20, 10)
        self.lab1.resize(100, 30)
        self.r1 = QRadioButton(self)
        self.r1.move(20, 40)
        self.r2 = QRadioButton(self)
        self.r2.move(120, 40)

        self.lab2 = QLabel(self)
        self.lab2.setText('Interval')
        self.lab2.move(420, 10)
        self.lab2.resize(100, 30)
        self.input = QLineEdit(self)
        self.input.move(420, 40)
        self.input.resize(300, 30)

        self.label3 = QLabel(self)
        self.label3.move(20, 80)
        self.label3.resize(400, 20)
        self.state = QTextEdit(self)
        self.state.move(20, 100)
        self.state.resize(760, 120)

        self.btn_start = QPushButton(self)
        self.btn_start.move(300, 240)
        self.btn_start.resize(200, 30)
        self.btn_start.clicked.connect(self.start)

        self.btn_toggle_language = QPushButton(self)
        self.btn_toggle_language.move(300, 280)
        self.btn_toggle_language.resize(200, 30)
        self.btn_toggle_language.clicked.connect(self.toggle_language)

        self.mouse_clicker = None
        self.started = False

    def start(self):
        try:
            interval = float(self.input.text())
            if self.mouse == LEFT:
                button = pynput.mouse.Button.left
            elif self.mouse == RIGHT:
                button = pynput.mouse.Button.right
            self.btn_start.setEnabled(False)
            self.state.clear()
            self.state.append(self.strings.get("state_waiting", ""))
            self.mouse_clicker = MouseClick(button, interval)
            self.mouse_clicker.started.connect(self.on_started)
            self.mouse_clicker.stopped.connect(self.on_stopped)
            t = threading.Thread(target=self.mouse_clicker.mouse_click)
            t.start()
        except ValueError:
            self.state.clear()
            self.state.append(self.strings.get("invalid_input", ""))

    def on_started(self):
        self.started = True
        self.state.clear()
        self.state.append(self.strings.get("state_clicking", ""))

    def on_stopped(self):
        self.started = False
        self.btn_start.setEnabled(True)
        self.state.clear()
        self.state.append(self.strings.get("state_idle", ""))

    def toggle_language(self):
        if self.language == "English":
            self.language = "Chinese"
        else:
            self.language = "English"
        self.update_language()

    def update_language(self):
        if self.language == "Chinese":
            self.strings = {
                "button_text_start": "开始",
                "button_text_toggle_language": "切换语言",
                "label_current_state": "---------- 当前状态和说明 ----------",
                "label_mouse_button": "鼠标按钮",
                "radio_button_left": "左键",
                "radio_button_right": "右键",
                "state_idle": "当前状态:空闲\n",
                "state_waiting": "当前状态:正在等待\n",
                "state_clicking": "当前状态:正在连点\n",
                "invalid_input": "时间输入出错!\n你应该输入整数或浮点数"
            }
        else:
            self.strings = {
                "button_text_start": "Start",
                "button_text_toggle_language": "Toggle Language",
                "label_current_state": "---------- Current State and Instructions ----------",
                "label_mouse_button": "Mouse Button",
                "radio_button_left": "Left",
                "radio_button_right": "Right",
                "state_idle": "Current State: Idle\n",
                "state_waiting": "Current State: Waiting\n",
                "state_clicking": "Current State: Clicking\n",
                "invalid_input": "Invalid input! Please enter an integer or float number."
            }

        self.lab1.setText(self.strings.get("label_mouse_button", ""))
        self.r1.setText(self.strings.get("radio_button_left", ""))
        self.r2.setText(self.strings.get("radio_button_right", ""))
        self.lab2.setText('时间间隔')
        self.label3.setText(self.strings.get("label_current_state", ""))
        self.btn_start.setText(self.strings.get("button_text_start", ""))
        self.btn_toggle_language.setText(self.strings.get("button_text_toggle_language", ""))
        self.state.clear()
        self.state.append(self.strings.get("state_idle", ""))

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
