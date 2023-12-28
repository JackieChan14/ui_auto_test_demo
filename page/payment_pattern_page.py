# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/9/5 17:51
@ Description: 支付方式页面
"""

from base import *


class PaymentPatternPage(BasePage):
	
	def __init__(self, page):
		super().__init__(page)
		self.page = self.page.frame(url=self.page.frames[-1].url)
		self.page.wait_for_timeout(1000)
