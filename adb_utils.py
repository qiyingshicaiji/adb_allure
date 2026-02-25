"""
ADB 工具模块：封装常用的 adb 命令操作。
"""

import os
import subprocess
import time
import xml.etree.ElementTree as ET


def run_adb(command):
    """
    执行 adb 命令并返回输出。

    Args:
        command: adb 命令字符串（不需要包含 'adb' 前缀）

    Returns:
        命令的标准输出字符串
    """
    full_command = f"adb {command}"
    result = subprocess.run(
        full_command, shell=True, capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip()


def start_app(package, activity):
    """
    启动指定 App。

    Args:
        package: 包名
        activity: Activity 名称
    """
    run_adb(f"shell am start -n {package}/{activity}")


def stop_app(package):
    """
    强制停止指定 App。

    Args:
        package: 包名
    """
    run_adb(f"shell am force-stop {package}")


def tap(x, y):
    """
    点击屏幕指定坐标。

    Args:
        x: 横坐标
        y: 纵坐标
    """
    run_adb(f"shell input tap {x} {y}")


def input_text(text):
    """
    输入文字。

    Args:
        text: 要输入的文本
    """
    run_adb(f"shell input text '{text}'")


def press_key(keycode):
    """
    模拟按键事件。

    常用 keycode:
        3  - HOME
        4  - BACK
        187 - APP_SWITCH (最近任务)

    Args:
        keycode: Android KeyEvent 代码
    """
    run_adb(f"shell input keyevent {keycode}")


def press_back():
    """按返回键。"""
    press_key(4)


def press_home():
    """按 Home 键。"""
    press_key(3)


def swipe(x1, y1, x2, y2, duration=500):
    """
    滑动操作。

    Args:
        x1, y1: 起始坐标
        x2, y2: 结束坐标
        duration: 滑动持续时间（毫秒）
    """
    run_adb(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")


def get_current_activity():
    """
    获取当前前台 Activity 名称。

    Returns:
        当前 Activity 的完整名称字符串
    """
    output = run_adb("shell dumpsys window windows")
    for line in output.splitlines():
        if "mCurrentFocus" in line or "mFocusedApp" in line:
            return line.strip()
    return ""


def get_logcat(tag=None, lines=100):
    """
    获取设备日志。

    Args:
        tag: 日志标签过滤（如 "MediaPlayer"）
        lines: 获取最近的日志行数

    Returns:
        日志文本
    """
    if tag:
        output = run_adb(f"shell logcat -d -t {lines} | grep -i {tag}")
    else:
        output = run_adb(f"shell logcat -d -t {lines}")
    return output


def clear_logcat():
    """清除设备日志缓存。"""
    run_adb("shell logcat -c")


def take_screenshot(local_path="screenshot.png"):
    """
    截取设备屏幕截图并保存到本地。

    Args:
        local_path: 本地保存路径

    Returns:
        本地截图文件路径
    """
    device_path = "/sdcard/screenshot.png"
    run_adb(f"shell screencap -p {device_path}")
    run_adb(f"pull {device_path} {local_path}")
    run_adb(f"shell rm {device_path}")
    return local_path


def dump_ui(local_path="window_dump.xml"):
    """
    导出当前界面 UI 树并保存到本地。

    Args:
        local_path: 本地保存路径

    Returns:
        本地 XML 文件路径
    """
    device_path = "/sdcard/window_dump.xml"
    run_adb(f"shell uiautomator dump {device_path}")
    run_adb(f"pull {device_path} {local_path}")
    run_adb(f"shell rm {device_path}")
    return local_path


def find_text_in_ui(text, local_path="window_dump.xml"):
    """
    在 UI dump 的 XML 中搜索是否存在包含指定文字的节点。

    Args:
        text: 要搜索的文字
        local_path: UI dump XML 文件路径

    Returns:
        bool: 是否找到
    """
    dump_ui(local_path)
    try:
        tree = ET.parse(local_path)
        root = tree.getroot()
        for node in root.iter("node"):
            node_text = node.get("text", "")
            if text in node_text:
                return True
    except ET.ParseError:
        return False
    finally:
        if os.path.exists(local_path):
            os.remove(local_path)
    return False


def is_process_running(package):
    """
    检查指定包名的进程是否在运行。

    Args:
        package: 包名

    Returns:
        bool: 进程是否存在
    """
    output = run_adb(f"shell pidof {package}")
    return len(output.strip()) > 0


def set_screen_orientation(landscape=False):
    """
    设置屏幕方向。

    Args:
        landscape: True 为横屏，False 为竖屏
    """
    # 先关闭自动旋转
    run_adb("shell settings put system accelerometer_rotation 0")
    rotation = 1 if landscape else 0
    run_adb(f"shell settings put system user_rotation {rotation}")


def broadcast_phone_state(state, number=""):
    """
    发送电话状态广播，模拟来电/挂断。

    通过 am broadcast 发送 PHONE_STATE Intent 来模拟来电状态变更。
    注意：这只是广播级别的模拟，不会触发系统来电 UI 或音频焦点抢占。
    App 必须自身监听 PHONE_STATE 广播才会响应。
    在 Android 9+ 上，该广播可能因权限限制被系统忽略。
    如需更真实的模拟，可在模拟器上使用 `adb emu gsm call <号码>`。

    Args:
        state: 电话状态 (RINGING, IDLE, OFFHOOK)
        number: 来电号码（仅 RINGING 状态需要）
    """
    cmd = f"shell am broadcast -a android.intent.action.PHONE_STATE --es state {state}"
    if number and state == "RINGING":
        cmd += f" --es incoming_number {number}"
    run_adb(cmd)


def start_browser(url="http://www.example.com"):
    """
    启动浏览器并打开指定 URL。

    Args:
        url: 要打开的网址
    """
    run_adb(f"shell am start -a android.intent.action.VIEW -d {url}")


def check_media_playing():
    """
    通过 dumpsys 检查是否有媒体正在播放。

    Returns:
        bool: 是否有媒体播放中
    """
    output = run_adb("shell dumpsys media_session")
    # 检查播放状态关键字
    return "state=PlaybackState {state=3" in output  # state=3 表示播放中


def check_media_paused():
    """
    通过 dumpsys 检查媒体是否暂停。

    Returns:
        bool: 是否暂停
    """
    output = run_adb("shell dumpsys media_session")
    return "state=PlaybackState {state=2" in output  # state=2 表示暂停
