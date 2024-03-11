import time
import threading
import pynput.mouse  
from pynput.keyboard import Key, Listener
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QRadioButton, QLineEdit, QTextEdit, QPushButton, QMessageBox
import ctypes
import subprocess

LEFT = 0
RIGHT = 1

# 切换语言函数
def toggle_language():
    global language
    if language == "English":
        language = "Chinese"
        # 修改界面文本为中文
        window.setWindowTitle('鼠标连点器[有快捷键版]')
        label3.setText('---------- 当前状态和说明 ----------')
        lab1.setText('鼠标按钮')
        r1.setText('左键')
        r2.setText('右键')
        lab2.setText('时间间隔')
        btn_start.setText('开始')
        btn_toggle_language.setText('切换语言') 
        state.clear()
        state.append("当前状态:空闲\n")
        state.append("选择您要单击的鼠标按钮并设置时间间隔，然后单击 START 按钮开始等待")
        QMessageBox.information(window, "切换语言", "已切换到中文界面")
    else:
        language = "English"
        # 修改界面文本为英文
        window.setWindowTitle('Mouse Clicker [with Hotkeys]')
        label3.setText('---------- Current State and Instructions ----------')
        lab1.setText('Mouse Button')
        r1.setText('Left')
        r2.setText('Right')
        lab2.setText('Interval')
        btn_start.setText('Start')
        btn_toggle_language.setText('Toggle Language')  
        state.clear()
        state.append("Current State: Idle\n")
        state.append("Choose the mouse button to click and set the interval, then click START button to begin.")
        QMessageBox.information(window, "Toggle Language", "Switched to English Interface")

# 鼠标连点控制类
class MouseClick:
    def __init__(self, button, time):
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
                state.clear()
                state.append("当前状态:正在等待\n")
                state.append("请点击ESC键返回\n")
                state.append("请按F8键开始连点")
                self.mouse_click()
            else:
                self.running = True
                state.clear()
                state.append("当前状态:正在连点\n")
                state.append("请按F8键停止连点\n")
                self.mouse_click()
        elif key == Key.esc:
            btn_start.setEnabled(True)
            state.clear()
            state.append("当前状态:空闲\n")
            state.append("选择您要点击的鼠标按钮并设置时间间隔，然后点击 START 按钮开始点击.")
            self.listener.stop()

    def mouse_click(self):
        key_listener = Listener(on_press=self.key_press)
        key_listener.start()
        while self.running:
            self.mouse.click(self.button)
            time.sleep(self.time)
        key_listener.stop()

# 新线程处理函数
def new_thread_start(button, time):
    MouseClick(button, time)

# START按键处理函数
def start():
    try:
        time = float(input.text())
        if mouse.get() == LEFT:
            button = pynput.mouse.Button.left
        elif mouse.get() == RIGHT:
            button = pynput.mouse.Button.right
        btn_start.setEnabled(False)
        state.clear()
        state.append("当前状态:正在等待\n")
        state.append("请按ESC键返回\n")
        state.append("请按F8键开始连点")
        t = threading.Thread(target=new_thread_start, args=(button, time))
        t.setDaemon(True)
        t.start()
    except:
        state.clear()
        state.append("时间输入出错!\n")
        state.append("你应该输入整数或浮点数")

app = QApplication([])
window = QMainWindow()
window.setGeometry(100, 100, 800, 400)
window.setFixedSize(800, 400)

# 设置初始语言为英文
language = "English"
window.setWindowTitle('Mouse Clicker [with Hotkeys]')

mouse = LEFT
lab1 = QLabel(window)
lab1.setText('Mouse Button')
lab1.move(20, 10)
lab1.resize(100, 30)
r1 = QRadioButton(window)
r1.setText('Left')
r1.setChecked(True)
r1.move(20, 40)
r2 = QRadioButton(window)
r2.setText('Right')
r2.move(120, 40)

lab2 = QLabel(window)
lab2.setText('Interval')
lab2.move(420, 10)
lab2.resize(100, 30)
input = QLineEdit(window)
input.move(420, 40)
input.resize(300, 30)

label3 = QLabel(window)
label3.setText('---------- Current State and Instructions ----------')
label3.move(20, 80)
label3.resize(400, 20)
state = QTextEdit(window)
state.move(20, 100)
state.resize(760, 120)
state.append("Current State: Idle\n")
state.append("Choose the mouse button to click and set the interval, then click START button to begin.")

btn_start = QPushButton(window)
btn_start.setText('Start')
btn_start.move(300, 240)
btn_start.resize(200, 30)
btn_start.clicked.connect(start)

btn_toggle_language = QPushButton(window)
btn_toggle_language.setText('Toggle Language')
btn_toggle_language.move(300, 280)
btn_toggle_language.resize(200, 30)
btn_toggle_language.clicked.connect(toggle_language)

window.show()
app.exec_()
