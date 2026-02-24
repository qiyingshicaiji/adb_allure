"""
场景 2：添加歌曲到"我喜欢"并验证歌单
验证将播放中的歌曲添加到"我喜欢"歌单，并确认歌曲出现在歌单中。
"""

import time

import allure
import pytest

import config
from adb_utils import (
    find_text_in_ui,
    input_text,
    press_back,
    take_screenshot,
    tap,
)


@allure.epic("音乐 App 自动化测试")
@allure.feature("收藏功能")
@allure.story("添加歌曲到我喜欢并验证歌单")
@allure.severity(allure.severity_level.CRITICAL)
class TestAddToFavorites:
    """场景 2：添加歌曲到"我喜欢"并验证歌单。"""

    @allure.title("收藏歌曲 - 验证歌曲出现在我喜欢歌单中")
    @allure.description(
        "搜索并播放歌曲后，点击喜欢按钮收藏歌曲，"
        "然后进入我喜欢歌单验证歌曲是否添加成功。"
    )
    def test_add_song_to_favorites(self, allure_screenshot):
        # 先搜索并播放歌曲（复用场景 1 的操作步骤）
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

        with allure.step("步骤 1：点击喜欢按钮收藏歌曲"):
            tap(config.LIKE_BTN_X, config.LIKE_BTN_Y)
            time.sleep(config.WAIT_SHORT)
            allure_screenshot("点击喜欢按钮后")

        with allure.step("步骤 2：返回主界面"):
            press_back()
            time.sleep(1)
            press_back()
            time.sleep(1)
            press_back()
            time.sleep(config.WAIT_SHORT)
            allure_screenshot("返回主界面")

        with allure.step("步骤 3：进入'我的'页面"):
            tap(config.MY_TAB_X, config.MY_TAB_Y)
            time.sleep(config.WAIT_MEDIUM)
            allure_screenshot("我的页面")

        with allure.step("步骤 4：进入'我喜欢的音乐'歌单"):
            tap(config.MY_FAVORITE_X, config.MY_FAVORITE_Y)
            time.sleep(config.WAIT_MEDIUM)
            allure_screenshot("我喜欢的音乐歌单")

        with allure.step("步骤 5：验证 - 在歌单中查找歌曲名称"):
            found = find_text_in_ui(config.TEST_SONG_NAME)
            allure.attach(
                f"搜索歌曲名: {config.TEST_SONG_NAME}\n找到: {found}",
                name="UI 查找结果",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert found, (
                f"在我喜欢歌单中未找到歌曲 '{config.TEST_SONG_NAME}'"
            )
            allure_screenshot("验证结果截图")
