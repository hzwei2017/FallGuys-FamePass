# ======README======
# 适用屏幕比例：    全比例
# 适用分辨率：      全分辨率（原始坐标依据3840*2160分辨率编写）
# 最后编辑日期：    2024年03月10日
# 最后版本：        v2.4
# 
# 2023-11-28 | v1.0 | 1、自动准备、打开ID、跳过动画、游戏内防挂机掉线
# 2023-12-02 | v1.1 | 2、把防挂机掉线改为向右移动鼠标1像素
# 2023-12-02 | v1.2 | 3、修改了匹配退出的坐标错误
# 2023-12-07 | v2.0 | 4、防挂机掉线改为按键；适配全分辨率、全比例屏幕
# 2023-12-15 | v2.1 | 5、多进程模式改为多线程模式，降低资源占用
# 2024-01-03 | v2.2 | 6、指定pyscreeze版本；加入前台窗口判定
# 2024-01-10 | v2.3 | 7、调整挂机判定间隔；加入启动画面广告自动跳过
# 2024-03-10 | v2.4 | 8、适配新版经验动画
# 
# ======README======

from multiprocessing import Process
import threading
import time
try:
    import pyautogui
except ImportError:  # 如果没有安装pyautogui，则自动安装
    import os
    os.system('pip install pyautogui')
    os.system('pip install pyscreeze==0.1.28')
    import pyautogui
import pygetwindow as gw

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


# ======防挂机掉线======
def func1():
    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [1720, 2600]
    y1 = [810, 1100]
    rgb1 = [(73, 151, 180), (42, 176, 209)]
    x2 = [2040]
    y2 = [890]
    rgb2 = [(41, 146, 179)]
    # 变化坐标
    x1_offset = calc_x_offset(x1)
    y1_offset = calc_y_offset(y1)
    x2_offset = calc_x_offset(x2)
    y2_offset = calc_y_offset(y2)

    while True:
        if is_window_active('FallGuys_client'):
            if pyautogui.pixelMatchesColor(x1_offset[0], y1_offset[0], rgb1[0], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[0], y2_offset[0], rgb2[0], tolerance=2) \
                and pyautogui.pixelMatchesColor(x1_offset[1], y1_offset[1], rgb1[1], tolerance=2): # 检测到挂机提醒
                pyautogui.press('=')
                print('{} 检测到挂机，已自动处理'.format(time.strftime("%H:%M:%S", time.localtime())))
                time.sleep(1)
            else:
                time.sleep(3)
        else:
            time.sleep(1)

# ======回车跳过动画======
def func2():
    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [40, 90, 70, 1610, 1040, 1000, 2160, 180, 1000, 1840, 110]
    y1 = [80, 100, 150, 1200, 100, 790, 870, 74, 780, 800, 760]
    rgb1 = [
        (254, 106, 0), (36, 29, 53), (34, 34, 38), (188, 0, 130), 
        (255, 208, 68), (38, 198, 236), (255, 255, 255), (192, 157, 62), 
        (38, 198, 236), (255, 255, 255), (189, 188, 189)
    ]
    x2 = [3600, 1000, 3400, 1810, 3100, 2130, 3000, 2400, 2130, 2480, 3580]
    y2 = [2070, 800, 2150, 830, 1980, 900, 1300, 1200, 860, 1060, 2080]
    rgb2 = [
        (49, 49, 49), (50, 201, 235), (28, 28, 28), (34, 35, 38), 
        (48, 194, 227), (255, 255, 255), (42, 176, 209), (42, 176, 209), 
        (255, 255, 255), (42, 176, 209), (49, 49, 49)
    ]
    # 变化坐标
    x1_offset = calc_x_offset(x1)
    y1_offset = calc_y_offset(y1)
    x2_offset = calc_x_offset(x2)
    y2_offset = calc_y_offset(y2)

    while True:
        if is_window_active('FallGuys_client'):
            if(
            pyautogui.pixelMatchesColor(x1_offset[0], y1_offset[0], rgb1[0], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[0], y2_offset[0], rgb2[0], tolerance=2)       # 捧杯动画
            or pyautogui.pixelMatchesColor(x1_offset[1], y1_offset[1], rgb1[1], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[1], y2_offset[1], rgb2[1], tolerance=2)    # 季票奖励
            # or pyautogui.pixelMatchesColor(x1_offset[2], y1_offset[2], rgb1[2], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[2], y2_offset[2], rgb2[2], tolerance=2)    # 经验奖励
            or pyautogui.pixelMatchesColor(x1_offset[3], y1_offset[3], rgb1[3], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[3], y2_offset[3], rgb2[3], tolerance=2)    # 启动页面
            # or pyautogui.pixelMatchesColor(x1_offset[4], y1_offset[4], rgb1[4], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[4], y2_offset[4], rgb2[4], tolerance=2)    # 大厅准备
            # or pyautogui.pixelMatchesColor(x1_offset[5], y1_offset[5], rgb1[5], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[5], y2_offset[5], rgb2[5], tolerance=2)    # 匹配退出至菜单
            or pyautogui.pixelMatchesColor(x1_offset[6], y1_offset[6], rgb1[6], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[6], y2_offset[6], rgb2[6], tolerance=2)    # 商店刷新
            or pyautogui.pixelMatchesColor(x1_offset[7], y1_offset[7], rgb1[7], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[7], y2_offset[7], rgb2[7], tolerance=2)    # 键位绑定重置提醒
            or pyautogui.pixelMatchesColor(x1_offset[8], y1_offset[8], rgb1[8], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[8], y2_offset[8], rgb2[8], tolerance=2)    # 匹配已取消
            or pyautogui.pixelMatchesColor(x1_offset[9], y1_offset[9], rgb1[9], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[9], y2_offset[9], rgb2[9], tolerance=2)    # 匹配异常
            or pyautogui.pixelMatchesColor(x1_offset[10], y1_offset[10], rgb1[10], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[10], y2_offset[10], rgb2[10], tolerance=2) # 新版经验奖励
                ):
                pyautogui.press('enter')
            else:
                time.sleep(0.5)
        else:
            time.sleep(1)

# ======回合结束查看其他玩家ID======
def func3():
    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [900, 3600]
    y1 = [130, 2100]
    rgb1 = [(255, 38, 255)]
    x2 = [3390]
    y2 = [2070]
    rgb2 = [(49, 49, 49)]
    # 变化坐标
    x1_offset = calc_x_offset(x1)
    y1_offset = calc_y_offset(y1)
    x2_offset = calc_x_offset(x2)
    y2_offset = calc_y_offset(y2)

    while True:
        if is_window_active('FallGuys_client'):
            if pyautogui.pixelMatchesColor(x1_offset[0], y1_offset[0], rgb1[0], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[0], y2_offset[0], rgb2[0], tolerance=2): # 查看ID
                pyautogui.click(x=x1_offset[1], y=y1_offset[1]) # 点击右下角查看按钮
                time.sleep(20)
            else:
                time.sleep(1)
        else:
            time.sleep(1)

# ======防止长期卡在坠落页面======
def func4():
    statement = 0 # 定义匹配时长计数变量

    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [100]
    y1 = [2070]
    rgb1 = [(248, 248, 248)]
    x2 = [3500]
    y2 = [2100]
    rgb2 = [(28, 28, 28)]
    # 变化坐标
    x1_offset = calc_x_offset(x1)
    y1_offset = calc_y_offset(y1)
    x2_offset = calc_x_offset(x2)
    y2_offset = calc_y_offset(y2)

    while True:
        if is_window_active('FallGuys_client'):
            if pyautogui.pixelMatchesColor(x1_offset[0], y1_offset[0], rgb1[0], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[0], y2_offset[0], rgb2[0], tolerance=2): # 检测坠落页面
                statement = statement + 1
                time.sleep(5)
                if statement >= 24: # 等待n个五秒
                    pyautogui.press('esc')
                    time.sleep(1)
                    pyautogui.press('enter')                
                    statement = 0 # 检测到卡顿，自动退出，同时变量归零
                    print('匹配于{}卡住，已自动退出'.format(time.strftime("%H:%M:%S", time.localtime())))
            else:
                statement = 0
                time.sleep(1)
        else:
            time.sleep(1)

# ======Esc跳过动画======
def func5():
    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [60]
    y1 = [100]
    rgb1 = [(34, 34, 38)]
    x2 = [3280]
    y2 = [1960]
    rgb2 = [(49, 49, 49)]
    # 变化坐标
    x1_offset = calc_x_offset(x1)
    y1_offset = calc_y_offset(y1)
    x2_offset = calc_x_offset(x2)
    y2_offset = calc_y_offset(y2)

    while True:
        if is_window_active('FallGuys_client'):
            if(
            pyautogui.pixelMatchesColor(x1_offset[0], y1_offset[0], rgb1[0], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[0], y2_offset[0], rgb2[0], tolerance=2) # 启动广告
                ):
                pyautogui.press('esc')
            else:
                time.sleep(1)
        else:
            time.sleep(1)

# ======自定义自动开始======
def func6():
    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [2760, 3300, 3100]
    y1 = [1800, 1800, 1800]
    rgb1 = [(48, 194, 227), (249, 53, 163)]
    x2 = [2180, 2180]
    y2 = [400, 400]
    rgb2 = [(49, 49, 49), (49, 49, 49)]
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
                pyautogui.click(x=x1_offset[1], y=y1_offset[1]) # 点击开始按键
                time.sleep(0.5)
            else:
                time.sleep(0.5)
        else:
            time.sleep(1)
            
if __name__ == "__main__":
    # time.sleep(3) # 等待3秒再启动，防误触
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '\n\n============　前言　============\n本脚本仅适用于PC端键鼠用户，请勿在\
程序执行过程中使用手柄\n当前仅对游戏内语言为简体中文的客户端测试过，其他语言暂未测试\n游戏过程中请将画面设置为全屏，目前暂无针对窗口化模式的适配\n\
\n============使用说明============\n本脚本包含以下功能：\n1、防止挂机掉线\n2、自动跳过夺冠动画、经验动画等\n3、每回合结束后自动打开其他玩家ID\n\
4、匹配超过2分钟后自动退出匹配\n\n============开始执行============')
    p1 = threading.Thread(target = func1)
    p2 = Process(target = func2)
    p3 = threading.Thread(target = func3)
    p4 = threading.Thread(target = func4)
    p5 = threading.Thread(target = func5)
    p6 = threading.Thread(target = func6)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    # p6.start()