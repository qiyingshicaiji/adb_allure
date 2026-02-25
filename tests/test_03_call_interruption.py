"""
场景 3：播放过程中模拟来电中断
验证来电时播放暂停、挂断后播放自动恢复。

本场景通过 ADB 广播（am broadcast）发送 PHONE_STATE 状态变更来模拟来电，
而非真正拨打电话。该广播仅测试 App 对 PHONE_STATE 广播的监听与响应能力。
真实来电会经过系统 Telephony 框架并通过 AudioFocus 机制强制暂停音频，
覆盖范围更广。详见 README.md 中"模拟来电 vs 真实来电"说明。
"""

import time

import allure
import pytest

import config
from adb_utils import (
    broadcast_phone_state,
    check_media_paused,
    check_media_playing,
    get_logcat,
    input_text,
    take_screenshot,
    tap,
)


@allure.epic("音乐 App 自动化测试")
@allure.feature("中断恢复")
@allure.story("播放过程中模拟来电中断")
@allure.severity(allure.severity_level.CRITICAL)
class TestCallInterruption:
    """场景 3：播放过程中模拟来电中断。"""

    @allure.title("来电中断 - 验证播放暂停与自动恢复")
    @allure.description(
        "播放歌曲过程中模拟来电，验证播放暂停；"
        "挂断后验证播放自动恢复。"
    )
    def test_call_interruption_and_resume(self, allure_screenshot):
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
            allure_screenshot("歌曲播放中 - 来电前")

        with allure.step("步骤 1：模拟来电（RINGING）"):
            broadcast_phone_state("RINGING", config.FAKE_PHONE_NUMBER)
            time.sleep(config.WAIT_MEDIUM)
            allure_screenshot("模拟来电中")

        with allure.step("步骤 2：验证 - 来电期间播放应暂停"):
            log_during_call = get_logcat(tag="MediaPlayer")
            allure.attach(
                log_during_call,
                name="来电期间日志",
                attachment_type=allure.attachment_type.TEXT,
            )
            is_paused = check_media_paused()
            is_not_playing = not check_media_playing()
            allure.attach(
                f"暂停状态: {is_paused}, 非播放状态: {is_not_playing}",
                name="播放状态检查",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert is_paused or is_not_playing, "来电期间播放未暂停"

        with allure.step("步骤 3：模拟挂断电话（IDLE）"):
            broadcast_phone_state("IDLE")
            time.sleep(config.WAIT_MEDIUM)
            allure_screenshot("挂断后")

        with allure.step("步骤 4：验证 - 挂断后播放应自动恢复"):
            log_after_call = get_logcat(tag="MediaPlayer")
            allure.attach(
                log_after_call,
                name="挂断后日志",
                attachment_type=allure.attachment_type.TEXT,
            )
            is_playing = check_media_playing()
            allure.attach(
                f"播放恢复状态: {is_playing}",
                name="恢复状态检查",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert is_playing, "挂断后播放未自动恢复"
            allure_screenshot("播放恢复后截图")
