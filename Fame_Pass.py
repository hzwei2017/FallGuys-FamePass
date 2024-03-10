# ======README======
# 适用每周专题：    适配生存休闲模式
# 适用屏幕比例：    全比例
# 适用分辨率：      全分辨率（原始坐标依据1920*1080分辨率编写）
# 最后编辑日期：    2024年02月22日
# 最后版本：        v5.6
# 
# 2023-11-26 | v3.1 | 1、关闭func3，将进入游戏检测和卡关检测合并，计数移给func1来判定
# 2023-11-27 | v3.2 | 2、将卡关检测时间从70s改成150s；删除以前的是否进入游戏检测
# 2023-11-30 | v4.0 | 4、将跳水和进入游戏检测合并
# 2023-12-02 | v4.1 | 5、把退出和回车合并；在大厅准备之前加入是否满级判定，并于满级后自动发送邮件通知
# 2023-12-03 | v4.2 | 6、启用git管理
# 2023-12-07 | v5.0 | 7、关闭git管理；将代码适配全分辨率、全比例屏幕
# 2023-12-15 | v5.1 | 8、多进程模式改为多线程模式，降低资源占用
# 2023-12-22 | v5.2 | 9、最后一次更新，由于糖豆人将每周专题自杀获得的经验降为20xp，所以该脚本失去意义了
# 2024-01-30 | v5.3 | 10、糖豆人恢复每周专题经验值
# 2024-01-31 | v5.4 | 11、加入季票等级平均执行效率变量，并监控该变量，在异常时发送邮件提醒
# 2024-02-22 | v5.5 | 12、修复监控脚本执行效率的bug；双倍经验周开始（2024-03-05 20:00结束）
# 2024-02-22 | v5.6 | 13、删除邮件装饰器和func4
# 2024-03-05 | v5.7 | 14、暂停func3；适配生存休闲模式；双倍经验结束
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
screen_gain = width/1920            # 计算放大比例
width_offset, height_offset = 0, 0
if width/height < 16/9:             # 屏幕为16:9标准比例
    height_offset = int((height-width/16*9)/2)
elif width/height > 16/9:           # 屏幕为带鱼屏这种宽比例
    width_offset = int((width-height/9*16)/2)
# print(screen_gain)

# ======建立日志文件夹======
def mkdir(path): 
	folder = os.path.exists(path) 
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
file = ".\\日志"
mkdir(file)

# ======配置日志记录器======
log_file = datetime.datetime.now().strftime("%Y-%m-%d.log")  # 根据当前日期生成日志文件名
logging.basicConfig(filename='./日志/'+log_file, filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s', encoding='utf-8')  # fliemode参数a为追加模式，w为覆写模式

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

# ======func1  进入游戏检测及自动跳水======
def func1():
    ave_lever = None # 定义平均等级变量，初始化前的值为 None
    start_time = time.time()
    frequency, statement = 0, 0 # 定义进入游戏轮数和卡顿检测变量
    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [1771, 997]
    y1 = [1017, 510]
    rgb1 = [(28, 28, 28), (253, 112, 88)]
    x2 = [53]
    y2 = [1034]
    rgb2 = [(248, 248, 249)]
    # 变化坐标
    x1_offset = calc_x_offset(x1)
    y1_offset = calc_y_offset(y1)
    x2_offset = calc_x_offset(x2)
    y2_offset = calc_y_offset(y2)
    while True:
        if is_window_active('FallGuys_client'):
            if pyautogui.pixelMatchesColor(x1_offset[0], y1_offset[0], rgb1[0], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[0], y2_offset[0], rgb2[0], tolerance=2):   # 坠落页面计时
                statement = statement + 1
                time.sleep(5)
                if statement >= 12: # 等待n个五秒
                    pyautogui.press('esc')
                    statement = 0 # 检测到卡顿，自动退出，同时变量归零
                    message = '卡住了'
                    logging.warning(message)    # 打印输出并保存到日志文件
                    # print(message)              # 在控制台输出
            elif pyautogui.pixelMatchesColor(x1_offset[1], y1_offset[1], rgb1[1], tolerance=2):
                statement = 0 # 成功进入游戏，归零变量
                frequency = frequency + 1
                level_count = round(frequency*215/12000, 2)
                total_seconds = time.time() - start_time
                minutes, seconds = divmod(total_seconds, 60)
                ave_lever = round(level_count*60*60/(int(minutes)*60 + int(seconds)), 3)
                message = "第{:03d}次进入，累计{:0.2f}级，已执行{:0.2f}小时，平均{:0.3f}级/小时".format(frequency, level_count, minutes/60, ave_lever)
                logging.info(message)   # 打印输出并保存到日志文件
                print(message, end='\r')          # 在控制台输出
                time.sleep(0.4)
                # pyautogui.press('t') # 视角归正
                pyautogui.keyDown('s')
                time.sleep(0.6)
                # pyautogui.keyDown('w')
                pyautogui.press('space')
                time.sleep(0.6)
                pyautogui.press('space')
                # pyautogui.keyUp('w')
                time.sleep(0.6)
                pyautogui.press('space')
                # time.sleep(7)
                # pyautogui.keyUp('w')
                time.sleep(10)
            else:
                time.sleep(0.4)
        else:
            time.sleep(1)

# ======func2  退出+回车======
def func2():
    # 录入原始x1, y1, rgb1, x2, y2, rgb2
    x1 = [60, 1560, 323, 880, 300, 483, 918, 20, 484, 257, 520, 1000, 55]
    y1 = [900, 1040, 18, 450, 320, 444, 388, 60, 235, 765, 48, 510, 380]
    rgb1 = [(49, 49, 49), (49, 49, 49), (34, 34, 38), (50, 201, 235), (49, 202, 236), (38, 198, 236), (255, 255, 255), (34, 34, 38), (119, 211, 238), (255, 255, 255), (255, 208, 68), (0, 182, 254), (189, 188, 189)]
    x2 = [1650, 1816, 1450, 1200, 1639, 1300, 1005, 1797, 952, 850, 1550, 1665, 1790]
    y2 = [1038, 1039, 1000, 125, 400, 550, 600, 1046, 267, 40, 1000, 1035, 1040]
    rgb2 = [(49, 49, 49), (49, 49, 49), (50, 201, 235), (255, 255, 255), (255, 255, 255), (42, 176, 209), (188, 0, 130), (49, 49, 49), (255, 255, 255), (0, 70, 236), (48, 194, 227), (49, 49, 49), (49, 49, 49)]
    # 变化坐标
    x1_offset = calc_x_offset(x1)
    y1_offset = calc_y_offset(y1)
    x2_offset = calc_x_offset(x2)
    y2_offset = calc_y_offset(y2)
    while True:
        if is_window_active('FallGuys_client'):
            if(
            pyautogui.pixelMatchesColor(x1_offset[2], y1_offset[2], rgb1[2], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[2], y2_offset[2], rgb2[2], tolerance=2)       # 启动广告页面
            or pyautogui.pixelMatchesColor(x1_offset[0], y1_offset[0], rgb1[0], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[0], y2_offset[0], rgb2[0], tolerance=2)    # 局内观战退出
            or pyautogui.pixelMatchesColor(x1_offset[1], y1_offset[1], rgb1[1], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[1], y2_offset[1], rgb2[1], tolerance=2)    # 淘汰结算退出（适配40人和60人两种结算页面）
            or pyautogui.pixelMatchesColor(x1_offset[3], y1_offset[3], rgb1[3], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[3], y2_offset[3], rgb2[3], tolerance=2)    # 局内退出菜单页
            or pyautogui.pixelMatchesColor(x1_offset[4], y1_offset[4], rgb1[4], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[4], y2_offset[4], rgb2[4], tolerance=2)    # 举报玩家列表
            or pyautogui.pixelMatchesColor(x1_offset[11], y1_offset[11], rgb1[11], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[11], y2_offset[11], rgb2[11], tolerance=2) # 出局啦横幅
                ):
                pyautogui.keyUp('s') # 结束func1的pyautogui.keyDown('s')
                pyautogui.press('esc')
                time.sleep(0.5)
            elif(
            pyautogui.pixelMatchesColor(x1_offset[5], y1_offset[5], rgb1[5], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[5], y2_offset[5], rgb2[5], tolerance=2)       # 淘汰观战视角退出节目+登录失败+匹配时退出确认
            or pyautogui.pixelMatchesColor(x1_offset[6], y1_offset[6], rgb1[6], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[6], y2_offset[6], rgb2[6], tolerance=2)    # 启动页面
            # or pyautogui.pixelMatchesColor(x1_offset[7], y1_offset[7], rgb1[7], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[7], y2_offset[7], rgb2[7], tolerance=2)    # 经验动画
            or pyautogui.pixelMatchesColor(x1_offset[8], y1_offset[8], rgb1[8], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[8], y2_offset[8], rgb2[8], tolerance=2)    # 季票奖励页面
            or pyautogui.pixelMatchesColor(x1_offset[10], y1_offset[10], rgb1[10], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[10], y2_offset[10], rgb2[10], tolerance=2)    # 大厅准备
            or pyautogui.pixelMatchesColor(x1_offset[12], y1_offset[12], rgb1[12], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[12], y2_offset[12], rgb2[12], tolerance=2)    # 新版经验动画
                ):
                pyautogui.press('enter')
                time.sleep(0.2)
            elif pyautogui.pixelMatchesColor(x1_offset[9], y1_offset[9], rgb1[9], tolerance=2) and pyautogui.pixelMatchesColor(x2_offset[9], y2_offset[9], rgb2[9], tolerance=2): # 设置页面
                time.sleep(5)
                pyautogui.press('esc')
            else:
                time.sleep(0.5)
        else:
            time.sleep(1)

if __name__ == "__main__":
    ticks = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # time.sleep(3) # 等待3秒再启动，防误触
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '\n\n============　前言　============\n本脚本仅适用于PC端键鼠用户，请勿在\
程序执行过程中使用手柄\n当前仅对游戏内语言为简体中文的客户端测试过，其他语言暂未测试\n游戏过程中请将画面设置为全屏，目前暂无针对窗口化模式的适配\n\
\n============使用说明============\n本脚本包含以下功能：\n1、自动进入游戏并跳水\n2、匹配超过1分钟后自动退出匹配\n3、自动跳过夺冠动画、经验动画等\n\
\n============开始执行============\n请回到游戏，选择每周专题模式，随后程序将自动执行')
    logging.info('开始执行 - 挂季票\n------------------------------------------------------------------------------------------------') # 打印输出并保存到日志文件
    p1 = threading.Thread(target = func1)
    p2 = threading.Thread(target = func2)
    p1.start()
    p2.start()