"""
pytest conftest.py：提供公共 fixtures 和 allure 配置。
"""

import os
import time

import allure
import pytest

import config
from adb_utils import (
    clear_logcat,
    press_home,
    set_screen_orientation,
    start_app,
    stop_app,
    take_screenshot,
)


@pytest.fixture(scope="session", autouse=True)
def check_device_connection():
    """会话级 fixture：检查 adb 设备连接。"""
    import subprocess

    result = subprocess.run(
        "adb devices", shell=True, capture_output=True, text=True, timeout=10
    )
    devices = result.stdout.strip().splitlines()
    # 第一行是 "List of devices attached"，之后每行是一个设备
    connected = [line for line in devices[1:] if line.strip().endswith("\tdevice") or "\tdevice\t" in line]
    if not connected:
        pytest.skip("未检测到 adb 设备连接，跳过所有测试")


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    每条测试用例前后的通用 setup / teardown。
    - 测试前：清除 logcat 日志，启动音乐 App。
    - 测试后：截图附加到 allure 报告，停止音乐 App，恢复竖屏。
    """
    # ---- Setup ----
    clear_logcat()
    stop_app(config.MUSIC_PACKAGE)
    time.sleep(config.WAIT_SHORT)
    start_app(config.MUSIC_PACKAGE, config.MUSIC_ACTIVITY)
    time.sleep(config.WAIT_LONG)

    yield

    # ---- Teardown ----
    try:
        screenshot_path = take_screenshot("teardown_screenshot.png")
        if os.path.exists(screenshot_path):
            allure.attach.file(
                screenshot_path,
                name="测试结束截图",
                attachment_type=allure.attachment_type.PNG,
            )
            os.remove(screenshot_path)
    except Exception:
        pass

    # 恢复竖屏
    set_screen_orientation(landscape=False)
    stop_app(config.MUSIC_PACKAGE)
    press_home()


@pytest.fixture()
def allure_screenshot():
    """
    提供一个可调用的截图 fixture，随时将截图附加到 allure 报告。
    """

    def _take(name="步骤截图"):
        try:
            path = take_screenshot("step_screenshot.png")
            if os.path.exists(path):
                allure.attach.file(
                    path,
                    name=name,
                    attachment_type=allure.attachment_type.PNG,
                )
                os.remove(path)
        except Exception:
            pass

    return _take
