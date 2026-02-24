"""
配置文件：音乐 App 测试参数
根据实际测试设备和 App 修改以下配置。
"""

# 音乐 App 包名和主 Activity（示例为网易云音乐，请根据实际 App 替换）
MUSIC_PACKAGE = "com.netease.cloudmusic"
MUSIC_ACTIVITY = "com.netease.cloudmusic.activity.LoadingActivity"

# 浏览器包名（用于多任务场景）
BROWSER_PACKAGE = "com.android.browser"

# 坐标配置（根据设备分辨率调整，以下以 1080x1920 为例）
# 搜索框坐标
SEARCH_BOX_X = 540
SEARCH_BOX_Y = 120

# 搜索输入框坐标（点击搜索框后出现的输入框）
SEARCH_INPUT_X = 540
SEARCH_INPUT_Y = 120

# 搜索按钮坐标
SEARCH_BTN_X = 1000
SEARCH_BTN_Y = 120

# 第一个搜索结果坐标
FIRST_RESULT_X = 540
FIRST_RESULT_Y = 350

# 喜欢按钮坐标（播放界面中的爱心按钮）
LIKE_BTN_X = 270
LIKE_BTN_Y = 1600

# "我的"标签坐标（底部导航栏）
MY_TAB_X = 900
MY_TAB_Y = 1850

# "我喜欢的音乐"歌单入口坐标
MY_FAVORITE_X = 540
MY_FAVORITE_Y = 600

# 测试用歌曲名称
TEST_SONG_NAME = "hello"

# 模拟来电号码
FAKE_PHONE_NUMBER = "1234567890"

# 等待时间（秒）
WAIT_SHORT = 2
WAIT_MEDIUM = 5
WAIT_LONG = 8

# 截图保存路径（设备端）
DEVICE_SCREENSHOT_PATH = "/sdcard/screenshot.png"

# UI dump 路径（设备端）
DEVICE_UI_DUMP_PATH = "/sdcard/window_dump.xml"
