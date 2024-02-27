import pyautogui
import tkinter as tk
from tkinter import messagebox

# 切换语言函数
def toggle_language():
    global language
    if language == "English":
        language = "Chinese"
        # 修改界面文本为中文
        window.title("鼠标连点器[无快捷键版]")
        label1.config(text="输入连点次数:")
        label2.config(text="输入点击间隔(秒):")
        button.config(text="开始连点")
        btn_toggle_language.config(text="切换语言")
        messagebox.showinfo("切换语言", "已切换到中文界面")
    else:
        language = "English"
        # 修改界面文本为英文
        window.title("Mouse Clicker [No Hotkeys]")
        label1.config(text="Enter Clicks:")
        label2.config(text="Enter Interval (seconds):")
        button.config(text="Start Clicking")
        btn_toggle_language.config(text="Toggle Language")
        messagebox.showinfo("Toggle Language", "Switched to English Interface")

# 创建 tkinter 窗口
window = tk.Tk()
window.title("Mouse Clicker [No Hotkeys]")
window.geometry("1920x1080")

# 设置窗口图标
window.iconbitmap('d.ico')
# 创建标签和输入框
label1 = tk.Label(window, text="Enter Clicks:")
label1.pack()
entry1 = tk.Entry(window, width=10)
entry1.pack()

label2 = tk.Label(window, text="Enter Interval (seconds):")
label2.pack()
entry2 = tk.Entry(window, width=10)
entry2.pack()

# 创建按钮和执行函数
def click_mouse():
    n_clicks = int(entry1.get())
    interval = float(entry2.get())

    for i in range(n_clicks):
        pyautogui.click()
        pyautogui.PAUSE = interval

button = tk.Button(window, text="Start Clicking", command=click_mouse)
button.pack()

# 切换语言按钮
language = "English"  # 默认语言为英文
btn_toggle_language = tk.Button(window, text='Toggle Language', command=toggle_language)
btn_toggle_language.pack()

# 运行窗口
window.mainloop()
