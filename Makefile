.PHONY: install check test test-one report report-static clean help

# 默认目标：显示帮助
help:
	@echo "ADB + Allure 自动化测试框架"
	@echo ""
	@echo "用法: make <目标>"
	@echo ""
	@echo "可用目标:"
	@echo "  install        安装 Python 依赖"
	@echo "  check          检查 ADB 设备连接"
	@echo "  test           执行全部测试"
	@echo "  test-one F=<文件> 执行指定测试文件，例如: make test-one F=tests/test_01_search_and_play.py"
	@echo "  report         运行测试并启动 Allure 在线报告（浏览器自动打开）"
	@echo "  report-static  运行测试并生成静态 Allure HTML 报告"
	@echo "  clean          清理测试产物（allure-results、allure-report、截图等）"
	@echo "  help           显示本帮助信息"

# 安装 Python 依赖
install:
	pip install -r requirements.txt

# 检查 ADB 设备连接
check:
	adb devices

# 执行全部测试
test:
	pytest

# 执行指定测试文件，用法: make test-one F=tests/test_01_search_and_play.py
test-one:
	pytest $(F)

# 运行测试并启动 Allure 在线报告
report:
	pytest || true
	allure serve allure-results

# 运行测试并生成静态 Allure HTML 报告
report-static:
	pytest || true
	allure generate allure-results -o allure-report --clean
	@echo "静态报告已生成到 allure-report/ 目录"
	@echo "运行 'allure open allure-report' 查看报告"

# 清理测试产物
clean:
	rm -rf allure-results allure-report .pytest_cache
	rm -f screenshot*.png teardown_screenshot.png step_screenshot.png window_dump.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
