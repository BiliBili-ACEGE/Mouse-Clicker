import pyautogui
import tkinter as tk

# 创建 tkinter 窗口
window = tk.Tk()
window.title("鼠标连点器[无快捷键版]")
window.geometry("1920x1080")

# 设置窗口图标
window.iconbitmap('d.ico')

# 创建标签和输入框
label1 = tk.Label(window, text="输入连点次数:")
label1.pack()
entry1 = tk.Entry(window, width=10)
entry1.pack()

label2 = tk.Label(window, text="输入点击间隔(秒):")
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

button = tk.Button(window, text="开始连点", command=click_mouse)
button.pack()

# 运行窗口
window.mainloop()
