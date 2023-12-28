# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/9/4 17:45
@ Description: 测试登录界面
"""
import allure
import pytest

from AutotestFrame import *

# MainPage的初始化实例对象，用于主菜单页的菜单切换
mp = None


@allure.epic('支付管理系统')
@allure.feature('支付方式管理')
class TestLogin:
	
	@pytest.mark.run(order=1)
	@allure.story('执行登录操作')
	@allure.title('登录')
	def test_login(self, page):
		lp = LoginPage(page)
		lp.do_login('username', 'password')
	
	@pytest.mark.run(order=2)
	@allure.story('进入主页')
	@allure.title('主页')
	def test_menu(self, page):
		global mp
		# 因为其他页面的page在实例化时已经切换到iframe内部了，只有mp页面的page在iframe之外，所以必须单独用mp的page进行菜单切换
		mp = MainPage(page)
	
	@pytest.mark.run(order=5)
	@pytest.mark.flaky(rerun=3, rerun_delay=5)
	@allure.story('修改状态和增删改查')
	@allure.title('短路路由界面')
	@pytest.mark.skip('跳过当前用例')
	def test_short_route(self, page):
		global mp
		getattr(mp, 'open_menu')('支付管理', '短路路由')
		
		srp = ShortRoutePage(page)
		
		srp.change_state(index=0, sure=False)
		
		srp.add(sure=False)
		srp.edit(index=0, sure=False)
		srp.delete(index=1, sure=False)
		srp.view(index=2, sure=False)
		
		srp.assert_state("启用")
		
		path = CommonUtils.ensure_path_sep('/test_data/srp_list.yml')
		YamlUtils.write_yaml(srp.get_list_text, file_path=path)
		AssertUtils.is_true(srp.get_list_text.__eq__(YamlUtils.read_yaml(file_path=path)), "断言失败")
	
	# getattr(mp, 'switch_tab')('支付方式管理')
	
	@pytest.mark.run(order=3)
	@pytest.mark.flaky(rerun=3, rerun_delay=5)
	@allure.story('修改状态并筛选状态')
	@allure.title('支付方式管理界面')
	@pytest.mark.skip('跳过当前用例')
	def test_payment_pattern_page(self, page):
		global mp
		getattr(mp, 'open_menu')('支付管理', '支付方式管理')
		
		ppp = PaymentPatternPage(page)
		ppp.change_state(index=0, sure=False)
		
		ppp.assert_state("禁用")
	
	@pytest.mark.run(order=4)
	@pytest.mark.flaky(rerun=3, rerun_delay=5)
	@allure.story('新增支付品牌')
	@allure.title('支付品牌管理界面')
	def test_payment_brand_page(self, page):
		global mp
		getattr(mp, 'open_menu')('支付管理', '支付品牌管理')
		
		pbp = PaymentBrandPage(page)
		# 新增微信支付的品牌并点击取消
		pbp.add(payment_brand='微信支付', sure=False)
		pbp.edit(payment_brand='银联云闪付', index=0, sure=False)


def teardown_module():
	log('info', '测试用例执行完毕\n', is_file_out=False)
