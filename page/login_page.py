# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/8/30 9:23
@ Description:
"""

from base import CommonUtils, BasePage, expect


class LoginPage(BasePage):
	
	def do_login(self, username, password):
		image_path = CommonUtils.ensure_path_sep('/image/captcha.png')
		self.page.goto('https://xxx.xxx.xxx')
		
		captcha_img = self.page.locator('.el-input-group__append').screenshot(path=image_path)
		captcha = CommonUtils.image_to_string(captcha_img)
		
		self.page.get_by_placeholder('账号').fill(username)
		self.page.get_by_placeholder('密码').fill(password)
		self.page.get_by_placeholder('验证码').fill(captcha)
		
		self.page.locator('.btnBox').click()
		
		expect(self.page).to_have_url('https://xxx.xxx.xxx')
