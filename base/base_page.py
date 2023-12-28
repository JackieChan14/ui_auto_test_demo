# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/8/24 17:45
@ Description:
"""
import re
from typing import Sequence, Literal

from playwright.sync_api import Page, expect

from common.assert_utils import AssertUtils
from common.common_utils import CommonUtils


class BasePage:
	
	def __init__(self, page: Page):
		self.page = page
		# 表格表头xpath
		self.list_th = '//thead[@class="has-gutter"]/tr/th[not(contains(@class, "is-hidden") or contains(@class, "gutter"))]'
		# 表格body的xpath
		self.list_td = '//div[contains(@class,"is-scrolling-none")]/table/tbody/tr/td[not(contains(@class, "is-hidden"))]'
	
	def get_text(self, content: str, index: int = 0) -> str:
		"""
		根据文字获取文本
		:param content: 需要获取的文字，模糊搜索
		:param index: 索引，默认为0，表示取第一个定位到的元素
		:return:
		"""
		_locator = self.page.get_by_text(content, exact=False)
		_count = _locator.count()
		if _count == 0:
			raise ValueError('定位路径未找到元素')
		elif _count == 1:
			return _locator.text_content()
		else:
			return _locator.nth(index).text_content()
	
	@property
	def get_list_text(self) -> Sequence[dict[str, str]]:
		"""
		获取当前表格内容
		:return: 按照[{表头1：内容1},{表头2：内容2},{表头3：内容3}, ...]的格式返回表格内容
		"""
		
		ths_count = self.page.locator(self.list_th).count()
		tds_count = self.page.locator(self.list_td).count()
		
		th_text = [self.page.locator(self.list_th).nth(th_count).text_content() for th_count in range(ths_count)]
		td_text = [self.page.locator(self.list_td).nth(td_count).text_content() for td_count in range(tds_count)]
		
		return CommonUtils.zip_th_td(th_text, td_text)
	
	def get_list_image(self, index) -> str:
		"""
		获取列表图片的url
		:param index: 列表行数索引，从0开始
		:return: 列表图片字段的file_id
		"""
		image_path = '//tbody/tr/td[not(contains(@class, "is-hidden"))]/div/div/img'
		image_url = self.page.locator(image_path).nth(index).get_attribute('src')
		file_id = re.findall(re.compile('(?<=fileId=)[A-Z0-9]+(?=&)'), image_url)[0]
		return file_id
	
	def sure(self, click_sure: bool):
		"""
		二次确认弹窗的操作（主要用于新增，编辑，删除，查看等操作最后一步的确认和取消操作）
		:param click_sure: 是否确认，True表示确认，False表示取消
		:return: None
		"""
		if click_sure:
			self.page.get_by_role('button', name="确定").click()
		else:
			self.page.get_by_role('button', name="取消").click()
	
	def data_operation(self, o_type: str, index: int = 0, *, is_list_button: bool = False):
		"""
		表格操作封装，将对表格的增删改查或者其他定制化操作统一封装，通过index和is_list_button决定对表格的哪一行进行操作
		:param o_type: 操作内容的文本，如新增，编辑，删除等，根据每个表格差异定制化
		:param index: 操作内容的对象索引，如对表格的第二条数据进行编辑，则o_type="编辑", index=1, is_list_button=True; 表格外的元素则可以不传index
		:param is_list_button: 是否为表格内的按钮，True时需要传index，如新增就不是表格内按钮，编辑、删除就是表格内按钮(与索引强关联)
		:return:
		"""
		_locator = None
		if is_list_button:
			_locator = self.page.locator(f'//tbody/tr/td[not(contains(@class, "is-hidden"))]/div/button/span[text()="{o_type}"]')
		else:
			_locator = self.page.locator(f'//span[text()="{o_type}"]')
		_count = _locator.count()
		# 没有定位到操作文本时
		if _count == 0:
			raise ValueError(f'不能进行{o_type}操作')
		# 只定位到一个操作文本时，如表格外按钮或者当表格只有一条数据时适用
		elif _count == 1:
			_locator.click()
		# 定位到的操作文本大于1，即表格数据大于1时，操作表格内按钮适用，需要传index，确定对哪一行的数据操作
		else:
			_locator.nth(index).click()
	
	def add(self, sure: bool = True):
		"""
		新增操作，表格外按钮，不传index
		:param sure: 是否确定
		:return:
		"""
		self.data_operation(o_type='新增')
		self.sure(click_sure=sure)
	
	def edit(self, index, sure: bool = True):
		"""
		编辑操作，表格内按钮，需要传index确定对哪条数据操作
		:param index: 需要编辑的数据行数(索引)
		:param sure: 是否确定
		:return:
		"""
		self.data_operation(o_type='编辑', index=index, is_list_button=True)
		self.sure(click_sure=sure)
	
	def delete(self, index, sure: bool = True):
		"""
		删除操作，表格内按钮，需要传index确定对哪条数据操作
		:param index: 需要删除的数据行数(索引)
		:param sure: 是否确定
		:return:
		"""
		self.data_operation(o_type='删除', index=index, is_list_button=True)
		self.sure(click_sure=sure)
	
	def view(self, index, sure: bool = True):
		"""
		查看操作，表格内按钮，需要传index确定对哪条数据操作
		:param index: 需要查看的数据行数(索引)
		:param sure: 是否确定
		:return:
		"""
		self.data_operation(o_type='查看', index=index, is_list_button=True)
		self.sure(click_sure=sure)
	
	def choose_state(self, state: Literal["启用", "禁用"]):
		"""
		状态查询框，选择启用或者禁用输入查询框
		:param state: 需要查询的状态
		:return:
		"""
		if state not in ('启用', '禁用'):
			raise ValueError('state参数值错误')
		
		self.page.get_by_placeholder('状态').click()
		self.page.locator(f'//span[text()="{state}"]').click()
	
	def change_state(self, *, index, sure: bool = True):
		"""
		修改状态
		:param index: 对第几行的数据修改状态(从0开始)
		:param sure: 是否确认
		:return:
		"""
		# 反查状态字段所在的列数，不存在则抛出异常
		state_col = self.get_col_by_th_text('状态')
		if state_col == 0:
			raise ValueError('列表不存在状态字段')
		now_state = self.get_state(index=index)
		if now_state == "禁用":
			self.page.locator(f'//tbody/tr/td[not(contains(@class,"is-hidden"))][{state_col}]').nth(index).click()
			self.sure(click_sure=sure)
			now_state2 = self.get_state(index=index)
			if sure:
				assert now_state2 == "启用"
			else:
				assert now_state2 == "禁用"
		elif now_state == "启用":
			self.page.locator(f'//tbody/tr/td[not(contains(@class,"is-hidden"))][{state_col}]').nth(index).click()
			self.sure(click_sure=sure)
			now_state2 = self.get_state(index=index)
			if sure:
				assert now_state2 == "禁用"
			else:
				assert now_state2 == "启用"
	
	def get_state(self, *, index) -> Literal["启用", "禁用"]:
		"""
		获取当前列表状态字段的值
		:param index: 对第几行的数据获取状态(从0开始)
		:return: 状态值：启用/禁用
		"""
		# 反查状态字段所在的列数，不存在则抛出异常
		state_col = self.get_col_by_th_text('状态')
		AssertUtils.is_false(state_col == 0, '列表不存在状态字段')
		
		try:
			# 状态值元素(div)存在aria-checked=true属性则返回启用，没有则返回禁用
			expect(self.page.locator(f'//tbody/tr/td[not(contains(@class,"is-hidden"))][{state_col}]/div/div')
			       .nth(index)).to_have_attribute('aria-checked', 'true')
			return "启用"
		except AssertionError:
			return "禁用"
	
	def get_col_by_th_text(self, col_name: str) -> int:
		"""
		通过表头字段反查该字段的列数
		:param col_name: 表头字段名
		:return: 该字段名在表格中的列数，没有查到则返回0，可以用于调用者抛出异常的判断根据
		"""
		col = 0
		ths_count = self.page.locator(self.list_th).count()
		for th_count in range(ths_count):
			if self.page.locator(self.list_th).nth(th_count).text_content() == col_name:
				col = th_count.__invert__().__neg__()  # 等价于col = th_count + 1
				break
		return col
	
	def assert_state(self, state: Literal["启用", "禁用"]):
		"""
		断言状态(以启用举例)
		:param state: 筛选的状态：启用/禁用
		:return:
		"""
		
		AssertUtils.is_true(state in ('启用', '禁用'), 'state参数值错误')
		
		# 自动反查状态字段所在的列数，不存在则抛出异常，并在筛选状态之前，对列表的每行数据获取状态值并加入state_list中
		list_length_before_choose = self.get_list_text.__len__()
		state_list = [self.get_state(index=i) for i in range(list_length_before_choose)]
		
		# 筛选(启用)状态
		self.choose_state(state)
		
		# 筛选启用状态之后，获取当前列表的数据行数
		list_length_after_choose = self.get_list_text.__len__()
		
		# 断言：筛选之前state_list中的启用的数量 和 筛选状态为启用之后的数据行数 相等
		AssertUtils.is_true(state_list.count(state) == list_length_after_choose, '前后状态不同')
	
	def assert_file_id(self, index: int):
		"""
		断言编辑弹窗图片和列表对应字段图片id是否相同
		:type index: 列表行数索引，从0开始
		:return:
		"""
		# 返回当前列表上img标签的图片的id
		list_image_src = self.get_list_image(index=index)
		
		# 验证编辑弹窗已经打开
		expect(self.page.get_by_role(role='dialog', name='编辑')).to_be_visible()
		
		# 在弹窗里找到对应的图片元素，将其的src属性保存下来
		edit_src = self.page.get_by_role(role='dialog', name='编辑').locator('//img').get_attribute('src')
		
		# 用正则取出fileId=之后的字符串，即图片的id
		edit_image_src = re.findall(re.compile('(?<=fileId=)[A-Z0-9]+'), edit_src)[0]
		
		# 断言两个id完全相同
		AssertUtils.is_true(list_image_src == edit_image_src, "id不同")
	
	def switch_tab(self, tab_name):
		"""
		切换顶部tab页，用MainPage的实例对象调用
		:param tab_name: tab页面关键字
		:return:
		"""
		self.page.get_by_role(role='tab', exact=False).filter(has_text=tab_name).click()
