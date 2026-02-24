"""
场景 1：正常搜索歌曲并播放
验证在音乐 App 中搜索歌曲并成功播放。
"""

import time

import allure
import pytest

import config
from adb_utils import (
    get_current_activity,
    get_logcat,
    input_text,
    take_screenshot,
    tap,
)


@allure.epic("音乐 App 自动化测试")
@allure.feature("搜索与播放")
@allure.story("正常搜索歌曲并播放")
@allure.severity(allure.severity_level.CRITICAL)
class TestSearchAndPlay:
    """场景 1：正常搜索歌曲并播放。"""

    @allure.title("搜索歌曲并播放 - 验证播放界面和播放状态")
    @allure.description(
        "启动音乐 App，搜索指定歌曲，点击第一个搜索结果，"
        "验证是否进入播放界面并开始播放。"
    )
    def test_search_and_play_song(self, allure_screenshot):
        with allure.step("步骤 1：点击搜索框"):
            tap(config.SEARCH_BOX_X, config.SEARCH_BOX_Y)
            time.sleep(config.WAIT_SHORT)
            allure_screenshot("点击搜索框后")

        with allure.step(f"步骤 2：输入歌曲名称 '{config.TEST_SONG_NAME}'"):
            tap(config.SEARCH_INPUT_X, config.SEARCH_INPUT_Y)
            time.sleep(1)
            input_text(config.TEST_SONG_NAME)
            time.sleep(config.WAIT_SHORT)
            allure_screenshot("输入歌名后")

        with allure.step("步骤 3：点击搜索按钮"):
            tap(config.SEARCH_BTN_X, config.SEARCH_BTN_Y)
            time.sleep(config.WAIT_MEDIUM)
            allure_screenshot("搜索结果页面")

        with allure.step("步骤 4：点击第一个搜索结果"):
            tap(config.FIRST_RESULT_X, config.FIRST_RESULT_Y)
            time.sleep(config.WAIT_LONG)
            allure_screenshot("点击搜索结果后")

        with allure.step("步骤 5：验证 - 检查是否进入播放界面"):
            current_activity = get_current_activity()
            allure.attach(
                current_activity,
                name="当前 Activity",
                attachment_type=allure.attachment_type.TEXT,
            )
            # 播放界面的 Activity 通常包含 play/player 关键字
            play_keywords = ["play", "player", "Play", "Player", "Playing"]
            activity_match = any(kw in current_activity for kw in play_keywords)
            assert activity_match, (
                f"未进入播放界面，当前 Activity: {current_activity}"
            )

        with allure.step("步骤 6：验证 - 检查 MediaPlayer 播放日志"):
            log_output = get_logcat(tag="MediaPlayer")
            allure.attach(
                log_output,
                name="MediaPlayer 日志",
                attachment_type=allure.attachment_type.TEXT,
            )
            # 日志中应该包含 MediaPlayer 相关信息
            assert "MediaPlayer" in log_output or "media" in log_output.lower(), (
                "未检测到 MediaPlayer 播放日志"
            )
            allure_screenshot("播放中截图")
