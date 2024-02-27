import time
import threading
import pynput.mouse  
from pynput.keyboard import Key, Listener
from tkinter import *
from tkinter import messagebox
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
        root.title('鼠标连点器[有快捷键版]')
        label3.config(text='---------- 当前状态和说明 ----------')
        lab1.config(text='鼠标按钮')
        r1.config(text='左键')
        r2.config(text='右键')
        lab2.config(text='时间间隔')
        btn_start.config(text='开始')
        btn_toggle_language.config(text='切换语言') 
        state.delete('0.0', END)
        state.insert(INSERT, "当前状态:空闲\n")
        state.insert(INSERT, "选择您要单击的鼠标按钮并设置时间间隔，然后单击 START 按钮开始等待")
        messagebox.showinfo("切换语言", "已切换到中文界面")
    else:
        language = "English"
        # 修改界面文本为英文
        root.title('Mouse Clicker [with Hotkeys]')
        label3.config(text='---------- Current State and Instructions ----------')
        lab1.config(text='Mouse Button')
        r1.config(text='Left')
        r2.config(text='Right')
        lab2.config(text='Interval')
        btn_start.config(text='Start')
        btn_toggle_language.config(text='Toggle Language')  
        state.delete('0.0', END)
        state.insert(INSERT, "Current State: Idle\n")
        state.insert(INSERT, "Choose the mouse button to click and set the interval, then click START button to begin.")
        messagebox.showinfo("Toggle Language", "Switched to English Interface")


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
                state.delete('0.0', END)
                state.insert(INSERT, "当前状态:正在等待\n")
                state.insert(INSERT, "请点击ESC键返回\n")
                state.insert(INSERT, "请按F8键开始连点")
                self.mouse_click()
            else:
                self.running = True
                state.delete('0.0', END)
                state.insert(INSERT, "当前状态:正在连点\n")
                state.insert(INSERT, "请按F8键停止连点\n")
                self.mouse_click()
        elif key == Key.esc:
            btn_start['state'] = NORMAL
            state.delete('0.0', END)
            state.insert(INSERT, "当前状态:空闲\n")
            state.insert(
                INSERT, "选择您要点击的鼠标按钮并设置时间间隔，然后点击 START 按钮开始点击.")
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
        time = float(input.get())
        if mouse.get() == LEFT:
            button = pynput.mouse.Button.left
        elif mouse.get() == RIGHT:
            button = pynput.mouse.Button.right
        btn_start['state'] = DISABLED
        state.delete('0.0', END)
        state.insert(INSERT, "当前状态:正在等待\n")
        state.insert(INSERT, "请按ESC键返回\n")
        state.insert(INSERT, "请按F8键开始连点")
        t = threading.Thread(target=new_thread_start, args=(button, time))
        t.setDaemon(True)
        t.start()
    except:
        state.delete('0.0', END)
        state.insert(INSERT, "时间输入出错!\n")
        state.insert(INSERT, "你应该输入整数或浮点数")

root = Tk()
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', ScaleFactor/75)
root.iconbitmap("./d.ico")

# 设置初始语言为英文
language = "English"
root.title('Mouse Clicker [with Hotkeys]')
root.geometry('1920x1080')

mouse = IntVar()
lab1 = Label(root, text='Mouse Button', font=("微软雅黑", 11), fg="gray")
lab1.place(relx=0.05, y=10, relwidth=0.4, height=30)
r1 = Radiobutton(root,
                 text='Left',
                 font=("微软雅黑", 10),
                 value=0,
                 variable=mouse)
r1.place(relx=0.05, y=40, relwidth=0.15, height=30)
r2 = Radiobutton(root,
                 text='Right',
                 font=("微软雅黑", 10),
                 value=1,
                 variable=mouse)
r2.place(relx=0.2, y=40, relwidth=0.3, height=30)

lab2 = Label(root, text='Interval', font=("微软雅黑", 11), fg="gray")
lab2.place(relx=0.55, y=10, relwidth=0.4, height=30)
input = Entry(root, relief="flat", font=("微软雅黑", 10))
input.place(relx=0.55, y=40, relwidth=0.4, height=30)

label3 = Label(root,
               text='---------- Current State and Instructions ----------',
               font=("微软雅黑", 8),
               fg="gray")
label3.place(relx=0.05, y=90, relwidth=0.9, height=20)
state = Text(root, relief="flat", font=("微软雅黑", 10))
state.place(relx=0.05, y=110, relwidth=0.9, height=120)
state.insert(INSERT, "Current State: Idle\n")
state.insert(INSERT, "Choose the mouse button to click and set the interval, then click START button to begin.")

btn_start = Button(root,
                   text='Start',
                   font=("微软雅黑", 12),
                   fg="white",
                   bg="#207fdf",
                   relief="flat",
                   command=start)
btn_start.place(relx=0.3, y=240, relwidth=0.4, height=30)

btn_toggle_language = Button(root, text='Toggle Language', font=("微软雅黑", 12), fg="white", bg="#207fdf", relief="flat", command=toggle_language)
btn_toggle_language.place(relx=0.3, y=280, relwidth=0.4, height=30)


root.mainloop()
