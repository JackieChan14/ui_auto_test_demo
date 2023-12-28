# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/9/13 16:49
@ Description: 支付品牌页面
"""
import re

from base import *


class PaymentBrandPage(BasePage):
	
	def __init__(self, page):
		super().__init__(page)
		self.page = self.page.frame(url=self.page.frames[-1].url)
		self.page.wait_for_timeout(1000)
	
	def add(self, payment_brand='', sure: bool = True):
		# 点击新增按钮(表格外按钮，不传is_list_button和index参数)
		self.data_operation(o_type='新增')
		# 在新增弹窗点击请选择的下拉框，选择支付品牌
		self.page.get_by_role("dialog", name="新增").get_by_placeholder("请选择").click()
		# 选择对应支付品牌选择点击
		expect(self.page.locator('//body/div[@class="el-select-dropdown el-popper"]')).to_have_attribute('x-placement', 'bottom-start')
		self.page.locator('//div[@x-placement="bottom-start"]').get_by_text(payment_brand).click()
		# 上传图片
		self.page.set_input_files('//input[@name="file"]', CommonUtils.ensure_path_sep('/image/captcha.png'))
		# 验证图片上传成功
		expect(self.page.locator('//ul[@class="el-upload-list el-upload-list--picture-card"]/li/img')).to_be_visible()
		# 点击确定/取消
		self.sure(click_sure=sure)
	
	def edit(self, index, payment_brand='', sure: bool = True):
		# payment_brand_text = self.get_list_text[index]['支付品牌']
		payment_brand_code = self.get_list_text[index]['支付品牌code']
		
		# 点击编辑按钮
		self.data_operation(o_type='编辑', index=index, is_list_button=True)
		
		# 验证支付品牌Code字段和选中的列表的支付品牌code字段的值相同
		expect(self.page.get_by_text('支付品牌Code：').locator('//../div[@class="el-form-item__content"]')).to_have_text(payment_brand_code)
		
		# 验证所选记录在列表的品牌logo字段图片内容和编辑弹窗内的logo字段图片内容相同
		self.assert_file_id(index=index)
		
		# 打开下拉框
		self.page.get_by_role("dialog", name="编辑").get_by_placeholder("请选择").click()
		
		# 验证下拉框被打开，即class属性包含is-focus
		expect(self.page.locator('//div[contains(@class, "el-select iptCss")]/div')).to_have_class(re.compile('(is-focus)+'))
		
		# 验证下拉框被打开，即下拉框元素多了一个x-placement=bottom-start属性
		expect(self.page.locator('//body/div[@class="el-select-dropdown el-popper"]')).to_have_attribute('x-placement', 'bottom-start')
		
		# 选择需要修改的支付品牌
		self.page.locator('//div[@x-placement="bottom-start"]').get_by_text(payment_brand).click()
		
		# assert self.page.locator('//li[contains(@class, "selected hover")]').text_content() == payment_brand_text
		
		# 删除当前已有的图片
		self.page.locator('//i[@class="el-icon-delete"]').click()
		
		# 上传新图片并点击确认/取消
		self.page.set_input_files('//input[@name="file"]', CommonUtils.ensure_path_sep('/image/captcha.png'))
		self.sure(click_sure=sure)
	
	def delete(self, index, sure: bool = True):
		super().delete(index=index, sure=sure)
