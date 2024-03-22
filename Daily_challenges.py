# ======README======
# 适用屏幕比例：    全比例
# 适用分辨率：      全分辨率（原始坐标依据3840*2160分辨率编写）
# 最后编辑日期：    2024年01月24日
# 最后版本：        v1.7
# 
# 2023-12-16 | v1.0 | 1、选择关卡后自动开始游戏；自动过关；跳过夺冠动画；完成目标局数后自动回到大厅并关闭脚本
# 2023-12-17 | v1.1 | 2、加入计时器
# 2023-12-19 | v1.2 | 3、将完成局数改为25局
# 2023-12-20 | v1.3 | 4、自动输入关卡ID
# 2023-12-23 | v1.4 | 5、将计数交由夺冠动画来判定；打印使用说明到命令行窗口上
# 2024-01-03 | v1.5 | 6、指定pyscreeze版本；加入前台窗口判定
# 2024-01-05 | v1.6 | 7、删除原func3、原func4
# 2024-01-24 | v1.7 | 8、自定义完成后自动更换游戏语言
# 2024-03-08 | v1.8 | 9、根据每日任务的变化，将过关任务改成奔跑3000米
# 
# ======README======

import threading
import os
import time
try:
    import pyautogui
except ImportError:  # 如果没有安装pyautogui，则自动安装
    import os
    os.system('pip install pyautogui')
    os.system('pip install pyscreeze==0.1.28')
    import pyautogui
import pygetwindow as gw

# 定义已成局数变量
round_count = 0 
# 需要完成的局数目标
target_rounds = 6

# ======适配全比例、全分辨率屏幕======
width, height = pyautogui.size()      # 获取当前屏幕分辨率
# print("屏幕分辨率为：{}x{}".format(width, height))
screen_gain = width / 3840            # 计算放大比例
width_offset, height_offset = 0, 0
if width/height < 16 / 9:             # 屏幕为16:10这种窄比例
    height_offset = int((height - width / 16 * 9) / 2)
elif width/height > 16 / 9:           # 屏幕为带鱼屏这种宽比例
    width_offset = int((width - height / 9 * 16) / 2)

# ======计算偏移量======
def add_offset(offset, gain):
    def inner(func):
        def wrapper(original_values):
            return [int(i * gain + offset) for i in original_values]
        return wrapper
    return inner

@add_offset(width_offset, screen_gain)
def calc_x_offset(x):
    return x

@add_offset(height_offset, screen_gain)
def calc_y_offset(y):
    return y

# ======判断窗口是否活跃在前台======
def is_window_active(title):
    try:
        window = gw.getWindowsWithTitle(title)[0]
        active_window_title = gw.getActiveWindow().title
        return active_window_title == window.title
    except:
        return False


# ======跳过夺冠动画并计数======
def func1():
    global round_count

    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [3438]
    y1 = [2054]
    rgb1 = [(28,28,28)]
    x2 = [60]
    y2 = [100]
    rgb2 = [(254, 106, 0)]
    # 变化坐标
    x1_offset = calc_x_offset(x1)
    y1_offset = calc_y_offset(y1)
    x2_offset = calc_x_offset(x2)
    y2_offset = calc_y_offset(y2)

    while True:
        if is_window_active('FallGuys_client'):
            if pyautogui.pixelMatchesColor(x1_offset[0], y1_offset[0], rgb1[0], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[0], y2_offset[0], rgb2[0], tolerance=2):  # 跳过胜利动画
                pyautogui.keyUp('w') # 结束func4的pyautogui.keyDown('w')
                pyautogui.press('enter')
                round_count = round_count + 1
                print("已完成{}局".format(round_count), end='\r')            
                time.sleep(15) # 等待15秒，防止重复计数
            else:
                time.sleep(0.5)
        else:
            time.sleep(1)

# ======自动开始======
def func2():
    start_time = time.time()

    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [2760, 3300, 3100, 1560, 3160, 1050, 2650, 50]
    y1 = [1800, 1800, 1800, 800, 660, 100, 660, 90]
    rgb1 = [(48, 194, 227), (249, 53, 163), (255, 208, 68), (34, 34, 38)]
    x2 = [2180, 2180, 2250]
    y2 = [400, 400, 2130]
    rgb2 = [(49, 49, 49), (49, 49, 49), (28, 28, 28)]
    # 变化坐标
    x1_offset = calc_x_offset(x1)
    y1_offset = calc_y_offset(y1)
    x2_offset = calc_x_offset(x2)
    y2_offset = calc_y_offset(y2)

    while True:
        if is_window_active('FallGuys_client'):
            if(
            pyautogui.pixelMatchesColor(x1_offset[0], y1_offset[0], rgb1[0], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[0], y2_offset[0], rgb2[0], tolerance=2)     # 识别蓝色开始按键
            or pyautogui.pixelMatchesColor(x1_offset[1], y1_offset[1], rgb1[1], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[1], y2_offset[1], rgb2[1], tolerance=2)  # 识别红色开始按键
                ):
                if round_count < target_rounds:
                    pyautogui.click(x=x1_offset[2], y=y1_offset[2]) # 点击开始按键
                    time.sleep(0.5)
                else:
                    print("{}局自定义已完成".format(target_rounds))
                    pyautogui.press('esc')
                    time.sleep(2)
                    pyautogui.press('enter')
                    time.sleep(1)
                    total_seconds = time.time() - start_time
                    minutes, seconds = divmod(total_seconds, 60)
                    a_alert = pyautogui.alert(text='{}局自定义已完成\n共计用时{}分钟{}秒'.format(target_rounds, int(minutes), int(seconds)), title='每日任务') # alert弹框
                    os._exit(0)  # 立即关闭整个程序
            else:
                time.sleep(0.5)
        else:
            time.sleep(1)

# ======输入房间代码======
def func3():
    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [2180, 3000, 2500]
    y1 = [400, 1550, 1600]
    rgb1 = [(49, 49, 49)]
    x2 = [2760]
    y2 = [1800]
    rgb2 = [(194, 194, 194)]
    # 变化坐标
    x1_offset = calc_x_offset(x1)
    y1_offset = calc_y_offset(y1)
    x2_offset = calc_x_offset(x2)
    y2_offset = calc_y_offset(y2)

    while True:
        if is_window_active('FallGuys_client'):
            if pyautogui.pixelMatchesColor(x1_offset[0], y1_offset[0], rgb1[0], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[0], y2_offset[0], rgb2[0], tolerance=2): # 检测到未输入房间代码
                time.sleep(1)
                pyautogui.click(x=x1_offset[1], y=y1_offset[1]) # 点击选择关卡
                time.sleep(1)
                pyautogui.press('alt')
                time.sleep(1)
                # pyautogui.write('253774198791') # 秒通关地图
                pyautogui.write('549821568727') # 我的刷任务关卡
                time.sleep(1)
                pyautogui.click(x=x1_offset[2], y=y1_offset[2]) # 点击开始
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(8)
            else:
                time.sleep(1)
        else:
            time.sleep(1)

# ======自动过关======
def func4():
    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [1994]
    y1 = [1020]
    rgb1 = [(253, 112, 88)]
    # 变化坐标
    x1_offset = calc_x_offset(x1)
    y1_offset = calc_y_offset(y1)

    while True:
        if is_window_active('FallGuys_client'):
            if pyautogui.pixelMatchesColor(x1_offset[0], y1_offset[0], rgb1[0], tolerance=2):
                time.sleep(0.4)
                pyautogui.keyDown('w')
                time.sleep(15)
            else:
                time.sleep(0.4)
        else:
            time.sleep(1)

if __name__ == "__main__":
    ticks = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # time.sleep(3) # 等待3秒，防误触
    print(ticks, '\n\n============　前言　============\n本脚本仅适用于PC端键鼠用户，请勿在程序执行过程中使用手柄\n当前仅对游戏内语言为简体中文的客户端\
测试过，其他语言暂未测试\n游戏过程中请将画面设置为全屏，目前暂无针对窗口化模式的适配\n\n============使用说明============\n请回到糖豆人，建立一个自定义房\
间\n其后不要随意移动鼠标和键盘，直至程序执行结束。\n\n============开始执行============')
    p1 = threading.Thread(target = func1)
    p2 = threading.Thread(target = func2)
    p3 = threading.Thread(target = func3)
    p4 = threading.Thread(target = func4)
    p1.start()
    p2.start()
    p3.start()
    p4.start()