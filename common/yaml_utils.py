# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/9/4 16:44
@ Description: 对yaml文件的操作进行封装的工具类，包括读和写
"""
from typing import Sequence

import yaml


class YamlUtils:
	@staticmethod
	def read_yaml(file_path: str, encoding: str = 'utf-8') -> Sequence:
		"""
		读取yaml文件的数据并返回
		:param file_path: yaml文件路径
		:param encoding: 文件编码，默认utf-8
		:return: 读取的yaml文件内容
		"""
		with open(file_path, mode='r', encoding=encoding) as f:
			data = yaml.safe_load(f)
		return data
	
	@staticmethod
	def write_yaml(data: Sequence, file_path: str, encoding: str = 'utf-8', is_append: bool = False):
		"""
		将指定数据写入yaml文件
		:param data: 需要写入的数据
		:param file_path: 需要写入的yaml文件路径
		:param encoding: 文件编码，默认utf-8
		:param is_append: 是否追加写的标识，默认为覆盖写，开启后可以实现追加写
		:return: None
		"""
		with open(file_path, mode='a' if is_append else 'w', encoding=encoding) as f:
			"""
			allow_unicode: 允许使用stream的编码(当前stream为f，编码为传入的encoding，默认utf-8)
			default_flow_style: 默认的yaml格式，False时则为自定义，如保留注释等
			sort_keys: 按照key的首字母ASCII码顺序排列，设置为False时，则取消默认排列，按照传入的第一个参数data本身的顺序写入
			"""
			yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
