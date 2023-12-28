# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/9/4 11:58
@ Description: pytest的conftest配置文件
"""
import os
import sys
import time

import allure
import pytest
from _pytest.terminal import TerminalReporter

from AutotestFrame import sync_playwright, log

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
_page = None


@pytest.fixture(scope='session')
def page():
	playwright = sync_playwright().start()
	browser = playwright.chromium.launch(headless=False if not sys.platform.lower().__eq__('linux') else True,
	                                     args=["--start-maximized"],
	                                     slow_mo=3000)
	if sys.platform.lower().__eq__('darwin') or sys.platform.lower().__eq__('linux'):
		context = browser.new_context(viewport={"width": 1920, "height": 1080})
	else:
		context = browser.new_context(no_viewport=True)
	global _page
	_page = context.new_page()
	yield _page
	
	_page.close()
	context.close()
	browser.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
	outcome = yield
	rep = outcome.get_result()
	if rep.when == "call" and rep.failed:
		mode = 'a' if os.path.exists('failure') else 'w'
		with open('failure', mode) as f:
			extra = f'{item.funcargs["tmpdir"]}' if 'tmpdir' in item.fixturenames else ''
			f.write(rep.nodeid + extra + '\t' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
		global _page
		if hasattr(_page, 'screenshot'):
			with allure.step('用例执行失败时，添加失败截图'):
				allure.attach(_page.screenshot(full_page=True), '异常截图', allure.attachment_type.PNG)
	
	function_name = item.function.__name__
	if rep.when == 'call':
		if rep.outcome == 'passed':
			log('info', f'用例{function_name}执行成功')
		if rep.outcome == 'failed':
			log('error', f'用例{function_name}执行失败')
		if rep.outcome == 'error':
			log('warning', f'用例{function_name}执行异常')
	
	if rep.outcome == 'skipped':
		log('warning', f'用例{function_name}跳过执行')


# yield item, call


def pytest_terminal_summary(terminalreporter: TerminalReporter):
	"""
	收集测试结果
	"""
	_PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
	_ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
	_FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
	_SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
	_TOTAL = getattr(terminalreporter, '_numcollected')
	_TIMES = time.time() - getattr(terminalreporter, '_sessionstarttime')
	log('info', f'用例总数：{_TOTAL}', is_file_out=False)
	log('info', f"成功用例数：{_PASSED}")
	log('error', f"失败用例数: {_FAILED}")
	log('warning', f"异常用例数: {_ERROR}")
	log('warning', f"跳过用例数: {_SKIPPED}")
	log('info', "用例执行时长: %.2f" % _TIMES + " s", is_file_out=False)
	try:
		_RATE = _PASSED / _TOTAL * 100
		log('info', "用例成功率: %.2f" % _RATE + " %", is_file_out=False)
	except ZeroDivisionError:
		log('info', "用例成功率: 0.00 %", is_file_out=False)
	finally:
		log('info', '本次用例执行完毕', is_file_out=False)
		log('info', '=' * 30, is_file_out=False)
