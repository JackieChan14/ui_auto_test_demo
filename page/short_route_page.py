# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/8/30 11:49
@ Description: 短路路由界面
"""
from base import *


class ShortRoutePage(BasePage):
	
	def __init__(self, page):
		super().__init__(page)
		self.page = self.page.frame(url=self.page.frames[-1].url)
	
	# self.page = self.page.frame_locator('iframe >> nth=1')
	
	def add(self, sure: bool = True):
		super().add(sure)
	
	def edit(self, index, sure: bool = True):
		super().edit(index, sure)
	
	def delete(self, index, sure: bool = True):
		super().delete(index, sure)
	
	def view(self, index, sure: bool = True):
		super().data_operation(o_type='查看详情', index=index, is_list_button=True)
		super().sure(click_sure=sure)
