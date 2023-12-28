# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/8/30 11:41
@ Description:
"""

from base import BasePage


class MainPage(BasePage):
	
	def open_menu(self, hover_menu, click_menu):
		self.page.locator(f'//span[text()="{hover_menu}"]').first.hover()
		self.page.locator(f'//span[text()="{click_menu}"]').first.click()
