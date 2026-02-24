"""
场景 5：边播放边执行其他操作（多任务）
验证切换到其他 App 后音乐后台播放不中断，切换回来后播放界面正常。
"""

import time

import allure
import pytest

import config
from adb_utils import (
    check_media_playing,
    get_current_activity,
    get_logcat,
    input_text,
    is_process_running,
    press_home,
    start_app,
    start_browser,
    swipe,
    take_screenshot,
    tap,
)


@allure.epic("音乐 App 自动化测试")
@allure.feature("多任务")
@allure.story("边播放边执行其他操作")
@allure.severity(allure.severity_level.NORMAL)
class TestMultitask:
    """场景 5：边播放边执行其他操作（多任务）。"""

    @allure.title("多任务切换 - 验证后台播放与前台恢复")
    @allure.description(
        "播放歌曲后切换到浏览器操作，再切换回音乐 App，"
        "验证播放始终持续、进程存活、播放界面恢复。"
    )
    def test_multitask_keeps_playing(self, allure_screenshot):
        # 先搜索并播放歌曲
        with allure.step("前置操作：搜索并播放歌曲"):
            tap(config.SEARCH_BOX_X, config.SEARCH_BOX_Y)
            time.sleep(config.WAIT_SHORT)
            tap(config.SEARCH_INPUT_X, config.SEARCH_INPUT_Y)
            time.sleep(1)
            input_text(config.TEST_SONG_NAME)
            time.sleep(config.WAIT_SHORT)
            tap(config.SEARCH_BTN_X, config.SEARCH_BTN_Y)
            time.sleep(config.WAIT_MEDIUM)
            tap(config.FIRST_RESULT_X, config.FIRST_RESULT_Y)
            time.sleep(config.WAIT_LONG)
            allure_screenshot("歌曲播放中")

        with allure.step("步骤 1：按 Home 键回到桌面"):
            press_home()
            time.sleep(config.WAIT_SHORT)
            allure_screenshot("桌面")

        with allure.step("步骤 2：启动浏览器"):
            start_browser("http://www.example.com")
            time.sleep(config.WAIT_MEDIUM)
            allure_screenshot("浏览器页面")

        with allure.step("步骤 3：在浏览器中模拟操作"):
            # 模拟在浏览器中上下滑动
            swipe(540, 1200, 540, 600, duration=500)
            time.sleep(config.WAIT_SHORT)
            swipe(540, 600, 540, 1200, duration=500)
            time.sleep(config.WAIT_SHORT)
            allure_screenshot("浏览器操作中")

        with allure.step("步骤 4：验证 - 音乐 App 进程应在后台存活"):
            process_alive = is_process_running(config.MUSIC_PACKAGE)
            allure.attach(
                f"进程存活: {process_alive}",
                name="进程检查",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert process_alive, (
                f"音乐 App 进程 ({config.MUSIC_PACKAGE}) 已被终止"
            )

        with allure.step("步骤 5：验证 - 后台播放应继续"):
            is_playing_bg = check_media_playing()
            allure.attach(
                f"后台播放状态: {is_playing_bg}",
                name="后台播放检查",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert is_playing_bg, "切换到浏览器后音乐播放中断"

        with allure.step("步骤 6：切换回音乐 App"):
            start_app(config.MUSIC_PACKAGE, config.MUSIC_ACTIVITY)
            time.sleep(config.WAIT_MEDIUM)
            allure_screenshot("切回音乐 App")

        with allure.step("步骤 7：验证 - 回到播放界面"):
            current_activity = get_current_activity()
            allure.attach(
                current_activity,
                name="当前 Activity",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert config.MUSIC_PACKAGE in current_activity, (
                f"未回到音乐 App，当前 Activity: {current_activity}"
            )

        with allure.step("步骤 8：验证 - 播放应持续"):
            is_playing_fg = check_media_playing()
            log_output = get_logcat(tag="MediaPlayer")
            allure.attach(
                log_output,
                name="切回后日志",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                f"前台播放状态: {is_playing_fg}",
                name="前台播放检查",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert is_playing_fg, "切回音乐 App 后播放中断"
            allure_screenshot("最终播放状态截图")
