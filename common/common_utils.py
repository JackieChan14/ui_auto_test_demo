# _*_coding:utf-8_*_
"""
@ Author:陈金泉
@ Date:2023/8/30 9:24
@ Description:
"""
import os
from functools import wraps
from typing import Union, Text, Optional, Sequence

from PIL.Image import Image
from ddddocr import DdddOcr

from common.excel_utils import NewExcelReader


class CommonUtils:
	# 全局路径设置为当前项目的根目录
	base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	
	@classmethod
	def ensure_path_sep(cls, path: Text) -> Text:
		"""
		绝对路径追加地址
		:param path: 需要追加的地址
		:return: 与base_path连接组成的实际地址(绝对路径表示)
		"""
		"""兼容windows和linux的路径格式"""
		if "/" in path:
			path = os.sep.join(path.split("/"))
		
		if "\\" in path:
			path = os.sep.join(path.split("\\"))
		return cls.base_path + path
	
	@staticmethod
	def image_to_string(image: Union[Image, bytes]) -> str:
		"""
		验证码图片的ocr识别
		:param image: 图片对象，可以支持Image对象或者流式的bytes对象
		:return: ocr识别出的验证码字符串
		"""
		if isinstance(image, (Image, bytes)):
			return DdddOcr(show_ad=False).classification(image)
		else:
			raise TypeError('图片对象类型错误')
	
	@staticmethod
	def singleton(func):
		"""
		单例装饰器，被其修饰的函数会返回单例对象
		:param func: 被修饰的函数
		:return: 语法糖修饰，则会返回同名函数，该函数已经具有生成单例对象的功能
		"""
		__instance = dict()
		
		@wraps(func)
		def wrapper(*args, **kwargs):
			if func not in __instance:
				__instance[func] = func(*args, **kwargs)
			return __instance[func]
		
		return wrapper
	
	@staticmethod
	def get_reader(file_path='') -> Optional[NewExcelReader]:
		"""
		excel的读取方法，目前暂时用不上
		:param file_path: excel的文件地址
		:return: NewExcelReader的实例对象
		"""
		if not os.path.isfile(file_path):
			raise FileNotFoundError('%s is not a file' % file_path)
		
		if file_path.endswith('.xlsx'):
			reader = NewExcelReader()
			reader.open_excel(file_path=file_path)
			return reader
	
	@staticmethod
	def zip_th_td(th: Sequence[str], td: Sequence[str]) -> Sequence[dict[str, str]]:
		"""
		将td的列表按照th的长度截取并分别和th打包成列表返回
		:param th: th定位xpath，表头列表
		:param td: td定位xpath，内容列表
		:return: [{表头：内容}, {表头：内容}, ...]的列表
		"""
		length = th.__len__()
		if length == 0:
			return []
		else:
			l = [td[i: i + length] for i in range(0, td.__len__(), length)]
			return [dict(zip(th, j)) for j in l]
