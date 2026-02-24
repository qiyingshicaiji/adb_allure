"""
场景 4：横竖屏切换时播放状态保持
验证切换屏幕方向后播放不中断。
"""

import time

import allure
import pytest

import config
from adb_utils import (
    check_media_playing,
    get_logcat,
    input_text,
    set_screen_orientation,
    take_screenshot,
    tap,
)


@allure.epic("音乐 App 自动化测试")
@allure.feature("屏幕旋转")
@allure.story("横竖屏切换时播放状态保持")
@allure.severity(allure.severity_level.NORMAL)
class TestScreenRotation:
    """场景 4：横竖屏切换时播放状态保持。"""

    @allure.title("屏幕旋转 - 验证播放不中断")
    @allure.description(
        "播放歌曲过程中切换横屏再切回竖屏，"
        "验证播放过程不中断。"
    )
    def test_rotation_keeps_playing(self, allure_screenshot):
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
            allure_screenshot("竖屏播放中")

        with allure.step("步骤 1：切换为横屏"):
            set_screen_orientation(landscape=True)
            time.sleep(config.WAIT_SHORT)
            allure_screenshot("横屏截图")

        with allure.step("步骤 2：验证 - 横屏时播放应继续"):
            is_playing_landscape = check_media_playing()
            log_landscape = get_logcat(tag="MediaPlayer")
            allure.attach(
                log_landscape,
                name="横屏时日志",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                f"横屏播放状态: {is_playing_landscape}",
                name="横屏播放检查",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert is_playing_landscape, "横屏切换后播放中断"

        with allure.step("步骤 3：切换回竖屏"):
            set_screen_orientation(landscape=False)
            time.sleep(config.WAIT_SHORT)
            allure_screenshot("竖屏截图")

        with allure.step("步骤 4：验证 - 竖屏恢复后播放应继续"):
            is_playing_portrait = check_media_playing()
            log_portrait = get_logcat(tag="MediaPlayer")
            allure.attach(
                log_portrait,
                name="竖屏恢复后日志",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                f"竖屏播放状态: {is_playing_portrait}",
                name="竖屏播放检查",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert is_playing_portrait, "竖屏恢复后播放中断"
            allure_screenshot("验证完成截图")
