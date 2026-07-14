from abc import ABC, abstractmethod
from ..utils import *

class ParadoxObjectBase(ABC):
    @abstractmethod
    def format(self) -> str:
        """ 将P语言对象格式化为P语言代码 """
        pass
    @abstractmethod
    def localization(self, language: Language) -> str:
        """ 生成本地化文件 """
        pass

class ParadoxObject(ParadoxObjectBase):
    def format(self) -> str: raise
    def localization(self, language: Language) -> str: raise

