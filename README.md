# ADB + Allure 自动化测试框架

基于 **Python + pytest + allure** 的安卓音乐 App 自动化测试框架，通过 ADB 工具操控安卓手机/模拟器完成测试。

## 项目结构

```
adb_allure/
├── config.py                             # 配置文件（包名、坐标、等待时间等）
├── adb_utils.py                          # ADB 工具模块（封装常用 adb 命令）
├── conftest.py                           # pytest fixtures（setup/teardown、allure 截图）
├── pytest.ini                            # pytest 配置文件
├── requirements.txt                      # Python 依赖
├── Makefile                              # Make 构建文件（快捷命令）
├── tests/
│   ├── __init__.py
│   ├── test_01_search_and_play.py        # 场景1：正常搜索歌曲并播放
│   ├── test_02_add_to_favorites.py       # 场景2：添加歌曲到"我喜欢"并验证歌单
│   ├── test_03_call_interruption.py      # 场景3：播放过程中模拟来电中断
│   ├── test_04_screen_rotation.py        # 场景4：横竖屏切换时播放状态保持
│   └── test_05_multitask.py              # 场景5：边播放边执行其他操作（多任务）
├── title.png                             # 作业题目截图
└── README.md                             # 本文件
```

## 项目逻辑原理

### 整体架构

本项目采用 **分层架构**，由底层到上层依次为：

```
┌────────────────────────────────────────────┐
│           Allure 测试报告（HTML）            │  ← 可视化展示测试结果
├────────────────────────────────────────────┤
│         pytest 测试用例（tests/）            │  ← 编排测试场景和断言
├────────────────────────────────────────────┤
│       ADB 工具层（adb_utils.py）            │  ← 封装 adb 命令为 Python 函数
├────────────────────────────────────────────┤
│        配置层（config.py）                  │  ← 定义目标 App 和 UI 坐标
├────────────────────────────────────────────┤
│     ADB 命令行工具 → 安卓设备/模拟器        │  ← 实际执行操作的底层通道
└────────────────────────────────────────────┘
```

### 执行流程

每条测试用例的执行流程如下：

1. **conftest.py（setup）**：清除日志 → 停止音乐 App → 启动音乐 App → 等待加载完成
2. **测试用例（tests/）**：按步骤操作 App（点击、输入、滑动等）→ 验证结果（断言）
3. **conftest.py（teardown）**：截图附加到报告 → 恢复竖屏 → 停止 App → 按 Home 键

### 程序如何定位到目标音乐 App

**是的，程序通过 `config.py` 中的配置直接定位到你要测试的音乐软件。** 核心机制如下：

| 步骤 | 实现方式 | 对应代码 |
|------|---------|---------|
| **1. 指定目标 App** | 在 `config.py` 中配置包名和 Activity | `MUSIC_PACKAGE`、`MUSIC_ACTIVITY` |
| **2. 启动 App** | 通过 ADB 命令 `am start -n 包名/Activity` 启动 | `adb_utils.start_app()` |
| **3. 操作 App** | 通过 ADB 命令在屏幕坐标上点击/输入/滑动 | `adb_utils.tap()`、`input_text()` 等 |
| **4. 验证结果** | 通过 ADB 读取 Activity、日志、UI 树、媒体状态 | `get_current_activity()`、`check_media_playing()` 等 |
| **5. 停止 App** | 通过 ADB 命令 `am force-stop 包名` 停止 | `adb_utils.stop_app()` |

换句话说，程序**不是自动识别**手机上安装了什么音乐 App，而是需要你在 `config.py` 中**手动指定**要测试的 App 的包名和 Activity。默认配置的是网易云音乐（`com.netease.cloudmusic`），如果你要测试其他音乐 App（如 QQ 音乐、酷狗音乐等），需要修改 `config.py` 中的对应值。

### 如何获取目标 App 的包名和 Activity

```bash
# 方法 1：在设备上打开目标 App，然后运行以下命令查看当前前台 Activity
adb shell dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'

# 方法 2：列出设备上所有已安装的包名
adb shell pm list packages | grep -i music

# 方法 3：查看某个 App 的所有 Activity
adb shell dumpsys package com.xxx.xxx | grep -i activity
```

获取到包名和 Activity 后，修改 `config.py`：

```python
# 例如测试 QQ 音乐：
MUSIC_PACKAGE = "com.tencent.qqmusic"
MUSIC_ACTIVITY = "com.tencent.qqmusic.activity.AppStarterActivity"
```

> **注意**：更换 App 后，还需要根据新 App 的界面布局调整 `config.py` 中的坐标配置（搜索框、按钮等位置），因为不同 App 的 UI 布局不同。

## 环境要求

- Python 3.8+
- ADB 工具（已配置到系统 PATH）
- 安卓手机或模拟器（通过 USB 或网络连接）
- 被测音乐 App 已安装到设备上

## 快速开始

```bash
# 1. 安装依赖
make install

# 2. 检查设备连接
make check

# 3. 修改 config.py 中的配置（包名、坐标等）

# 4. 执行全部测试
make test

# 5. 生成并查看 Allure 报告
make report
```

## 安装依赖

```bash
pip install -r requirements.txt
# 或
make install
```

## 配置说明

在运行测试前，需要根据实际设备和 App 修改 `config.py` 中的配置：

| 配置项 | 说明 |
|--------|------|
| `MUSIC_PACKAGE` | 音乐 App 包名 |
| `MUSIC_ACTIVITY` | 音乐 App 主 Activity |
| `SEARCH_BOX_X/Y` | 搜索框坐标 |
| `SEARCH_BTN_X/Y` | 搜索按钮坐标 |
| `FIRST_RESULT_X/Y` | 第一个搜索结果坐标 |
| `LIKE_BTN_X/Y` | 喜欢按钮坐标 |
| `TEST_SONG_NAME` | 测试用歌曲名称 |

> **提示**：可通过 `adb shell uiautomator dump /sdcard/ui.xml` 导出界面布局，或使用 Android SDK 的 **uiautomatorviewer** 工具获取元素坐标。

## 运行测试

### 确认设备连接

```bash
adb devices
# 或
make check
```

### 执行全部测试

```bash
pytest
# 或
make test
```

### 执行指定场景

```bash
# 仅运行场景 1
pytest tests/test_01_search_and_play.py
# 或
make test-one F=tests/test_01_search_and_play.py

# 仅运行场景 3
pytest tests/test_03_call_interruption.py
# 或
make test-one F=tests/test_03_call_interruption.py
```

### 生成 Allure 报告

```bash
# 运行测试并在浏览器中打开报告
make report

# 或生成静态报告
make report-static

# 也可手动执行：
pytest
allure serve allure-results
# 或
allure generate allure-results -o allure-report --clean
allure open allure-report
```

### 清理测试产物

```bash
make clean
```

## 测试场景说明

### 场景 1：正常搜索歌曲并播放
- 启动音乐 App → 点击搜索 → 输入歌名 → 搜索 → 点击结果 → 验证播放
- **验证点**：当前 Activity 包含播放页面关键字；MediaPlayer 日志确认播放

### 场景 2：添加歌曲到"我喜欢"并验证歌单
- 播放歌曲 → 点击喜欢 → 返回 → 进入我喜欢歌单 → 查找歌曲
- **验证点**：通过 `uiautomator dump` + XML 解析验证歌曲名存在

### 场景 3：播放过程中模拟来电中断
- 播放歌曲 → 模拟来电广播 → 验证暂停 → 模拟挂断 → 验证恢复
- **验证点**：来电时 media_session 状态为暂停；挂断后恢复播放

### 场景 4：横竖屏切换时播放状态保持
- 播放歌曲 → 横屏 → 验证播放 → 竖屏 → 验证播放
- **验证点**：旋转前后 media_session 播放状态始终为播放中

### 场景 5：边播放边执行其他操作（多任务）
- 播放歌曲 → Home → 打开浏览器 → 操作 → 回到音乐 App → 验证
- **验证点**：进程存活、后台持续播放、回到前台播放正常

## ADB 工具模块 (adb_utils.py)

封装了以下常用操作：

| 函数 | 说明 |
|------|------|
| `run_adb(command)` | 执行 adb 命令 |
| `start_app(package, activity)` | 启动 App |
| `stop_app(package)` | 强制停止 App |
| `tap(x, y)` | 点击坐标 |
| `input_text(text)` | 输入文字 |
| `press_key(keycode)` | 模拟按键 |
| `swipe(x1, y1, x2, y2)` | 滑动操作 |
| `get_current_activity()` | 获取当前 Activity |
| `get_logcat(tag)` | 获取设备日志 |
| `take_screenshot(path)` | 截图 |
| `dump_ui(path)` | 导出 UI 树 |
| `find_text_in_ui(text)` | UI 中搜索文字 |
| `set_screen_orientation(landscape)` | 设置屏幕方向 |
| `broadcast_phone_state(state)` | 模拟来电/挂断 |
| `check_media_playing()` | 检查是否播放中 |
| `check_media_paused()` | 检查是否暂停 |
| `is_process_running(package)` | 检查进程是否存活 |

## Makefile 目标一览

| 目标 | 说明 |
|------|------|
| `make help` | 显示帮助信息 |
| `make install` | 安装 Python 依赖 |
| `make check` | 检查 ADB 设备连接 |
| `make test` | 执行全部测试 |
| `make test-one F=<文件>` | 执行指定测试文件 |
| `make report` | 运行测试并启动 Allure 在线报告 |
| `make report-static` | 运行测试并生成静态 Allure HTML 报告 |
| `make clean` | 清理测试产物 |
