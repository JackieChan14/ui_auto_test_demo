# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/9/22 14:42
@ Description: 断言工具类
"""
import re
from typing import Union, Sequence, Text, Optional


class AssertUtils:
	
	@staticmethod
	def is_true(value: bool, message: str = '不能为False'):
		"""value为假则抛出异常"""
		if not value:
			raise AssertionError(message)
	
	@staticmethod
	def is_false(value: bool, message: str = '不能为True'):
		"""value为真则抛出异常"""
		if value:
			raise AssertionError(message)
	
	@staticmethod
	def is_null(value: object, message: str = '内容必须为空'):
		"""value非空则抛出异常"""
		if value is not None:
			raise AssertionError(message)
	
	@staticmethod
	def not_null(value: object, message: str = '内容不能为空'):
		"""value为空则抛出异常"""
		if value is None:
			raise AssertionError(message)
	
	@classmethod
	def not_blank(cls, value: Optional[Union[str, Sequence, Text, set]], message: str = '内容不能为零长度对象'):
		"""value为零长度对象(包括空元组，空列表，空字典，空集合，空字符串等)，则抛出异常"""
		cls.not_null(value, 'value值为None')
		if len(value) == 0:
			raise AssertionError(message)
	
	@staticmethod
	def is_type(value: object, v_type: type, message: str = '传入的值不是对应类型'):
		"""value不为v_type类型，则抛出异常"""
		if not isinstance(value, v_type):
			raise AssertionError(message)
	
	@staticmethod
	def is_match_regular(value: str, v_pattern: re.Pattern, message: str = '传入的值不满足正则'):
		"""value不满足v_pattern正则，则抛出异常"""
		if not re.match(v_pattern, value):
			raise AssertionError(message)


if __name__ == '__main__':
	AssertUtils.is_match_regular("13883380496", re.compile(r'^1[3-9]\d{9}$'), '传入的值不满足正则111')
	AssertUtils.is_true(1 <= 2, "断言失败")
