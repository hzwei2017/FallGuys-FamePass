# ======README======
# 适用每周专题：    探索
# 适用屏幕比例：    全比例
# 适用分辨率：      全分辨率（原始坐标依据1920*1080分辨率编写）
# 最后编辑日期：    2024年06月16日
# 最后版本：        v6.1
# 
# 2023-11-26 | v3.1 | 1、关闭func3；将进入游戏检测和卡关检测合并，计数移给func1来判定
# 2023-11-27 | v3.2 | 2、将卡关检测时间从70s改成150s；删除以前的是否进入游戏检测
# 2023-11-30 | v4.0 | 3、将跳水和进入游戏检测合并
# 2023-12-02 | v4.1 | 4、把退出和回车合并；在大厅准备之前加入是否满级判定，并于满级后自动发送邮件通知
# 2023-12-03 | v4.2 | 5、启用git管理
# 2023-12-07 | v5.0 | 6、关闭git管理；将代码适配全分辨率、全比例屏幕
# 2023-12-15 | v5.1 | 7、多进程模式改为多线程模式以降低资源占用
# 2023-12-22 | v5.2 | 8、由于糖豆人将每周专题获得的经验降为20xp，所以该脚本失去意义了
# 2024-01-30 | v5.3 | 9、糖豆人恢复每周专题经验值
# 2024-01-31 | v5.4 | 10、加入季票等级平均执行效率变量，并监控该变量，在异常时发送邮件提醒
# 2024-02-22 | v5.5 | 11、修复监控脚本执行效率的bug；双倍经验日开始（2024-03-05 20:00结束）
# 2024-02-22 | v5.6 | 12、删除邮件装饰器和func4
# 2024-03-05 | v5.7 | 13、暂停func3；适配生存休闲模式；双倍经验日结束
# 2024-03-13 | v5.8 | 14、适配混合生存赛；更改func1中经验值计算方式
# 2024-03-22 | v5.9 | 15、适配重力蜂窝迷环试炼
# 2024-04-18 | v6.0 | 16、双倍经验日开始（2024-04-30 20:00结束）
# 2024-06-16 | v6.1 | 17、探索模式的新挂季票方案
# 
# ======README======

import threading
import time
import logging
import datetime
from functools import wraps
import os
try:
    import pyautogui
except ImportError:  # 如果没有安装pyautogui，则自动安装
    import os
    os.system('pip install pyautogui')
    os.system('pip install pyscreeze==0.1.28')
    import pyautogui
import pygetwindow as gw

# ======适配全比例、全分辨率屏幕======
width, height = pyautogui.size()    # 获取当前屏幕分辨率
# print("屏幕分辨率为：{}x{}".format(width, height))
screen_gain = width / 1920  # 计算放大比例
width_offset, height_offset = 0, 0
if width / height < 16 / 9:  # 屏幕为16:10这种窄比例
    height_offset = int((height - width / 16 * 9) / 2)
elif width / height > 16 / 9:  # 屏幕为带鱼屏这种宽比例
    width_offset = int((width - height / 9 * 16) / 2)

# ======建立日志文件夹======
def mkdir(path): 
	folder = os.path.exists(path) 
	if not folder:                  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)       #makedirs 创建文件时如果路径不存在会创建这个路径
file = ".\\日志"
mkdir(file)

# ======配置日志记录器======
log_file = datetime.datetime.now().strftime("%Y-%m-%d.log")  # 根据当前日期生成日志文件名
logging.basicConfig(filename='./日志/'+log_file, filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S', encoding='utf-8')  # fliemode参数a为追加模式，w为覆写模式

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


# ======进入游戏检测及自动跳水======
def func1():
    ave_lever = None # 定义平均等级变量，初始化前的值为 None
    start_time = time.time()
    frequency, statement = 0, 0 # 定义进入游戏轮数和卡顿检测变量
    round_experience = 400 #每局获得经验值
    xp_per_level = 12000 # 升一级所需经验值

    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [130, 130]
    y1 = [80, 220]
    rgb1 = [(49, 49, 49), (49, 49, 49)]
    x2 = [210, 220]
    y2 = [33, 169]
    rgb2 = [(255, 255, 253), (254, 255, 253)]
    # 变化坐标
    x1_offset = calc_x_offset(x1)
    y1_offset = calc_y_offset(y1)
    x2_offset = calc_x_offset(x2)
    y2_offset = calc_y_offset(y2)

    while True:
            if (
            pyautogui.pixelMatchesColor(x1_offset[0], y1_offset[0], rgb1[0], tolerance=4) and pyautogui.pixelMatchesColor(x2_offset[0], y2_offset[0], rgb2[0], tolerance=4)     # 适用竞速模式
            or pyautogui.pixelMatchesColor(x1_offset[1], y1_offset[1], rgb1[1], tolerance=4) and pyautogui.pixelMatchesColor(x2_offset[1], y2_offset[1], rgb2[1], tolerance=4)  # 适用生存模式
            ):
                statement = 0  # 成功进入游戏，归零变量
                frequency += 1
                level_count = frequency * round_experience / xp_per_level
                total_seconds = time.time() - start_time
                ave_lever = frequency * round_experience / total_seconds * 3600 / xp_per_level
                # message = "第{:03d}次进入，累计{:0.2f}级，已执行{:0.2f}小时，平均{:0.3f}级/小时".format(frequency, level_count, total_seconds / 3600, ave_lever)
                message = "{:03d}：累计{:0.2f}级、{:0.2f}小时、{:0.3f}级/小时".format(frequency, level_count, total_seconds / 3600, ave_lever)
                logging.info(message)       # 打印输出并保存到日志文件
                print(message, end='\r')    # 在控制台输出
                # time.sleep(1)
                pyautogui.keyDown('r')
                time.sleep(3)
                pyautogui.keyUp('r')
                time.sleep(10)
            else:
                statement = 0
                time.sleep(1)

# ======退出+回车======
def func2():
    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [380]
    y1 = [920]
    rgb1 = [(66, 79, 173)]
    x2 = [1560]
    y2 = [1000]
    rgb2 = [(230, 167, 51)]
    # 变化坐标
    x1_offset = calc_x_offset(x1)
    y1_offset = calc_y_offset(y1)
    x2_offset = calc_x_offset(x2)
    y2_offset = calc_y_offset(y2)

    while True:
        if is_window_active('FallGuys_client'):
            if pyautogui.pixelMatchesColor(x1_offset[0], y1_offset[0], rgb1[0], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[0], y2_offset[0], rgb2[0], tolerance=2): # 检测大厅
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)
            else:
                time.sleep(1)
        else:
            time.sleep(1)

if __name__ == "__main__":
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '\n\n============　前言　============\n本脚本仅适用于PC端键鼠用户，请勿在\
程序执行过程中使用手柄\n当前仅对游戏内语言为简体中文的客户端测试过，其他语言暂未测试\n游戏过程中请将画面设置为全屏，目前暂无针对窗口化模式的适配\n\
\n============开始执行============\n请回到游戏，选择探索模式，随后程序将自动执行')
    logging.info('开始执行 - 挂季票\n' + '-' * 96) # 保存至日志文件
    p1 = threading.Thread(target = func1)
    p2 = threading.Thread(target = func2)
    p1.start()
    p2.start()