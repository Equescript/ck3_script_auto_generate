from abc import ABC, abstractmethod
from ..utils import *

class ActionBase(ABC):
    """ 所有P语言的操作在Python中对象的抽象基类。

    P语言中，各种操作都有着固定的格式，因此可以写出各种Action类来进行格式化。这里抽象出一个Action类来表示它们的共性，它是一个抽象基类（参见Python模块abc文档），无法被直接实例化，请使用它的子类。
    """
    @abstractmethod
    def execute(self):
        """ execute方法是我当时的一个设计想法：直接用python代码模拟P语言运行，以及时找出问题，不过暂时没有结果，现在可以忽略这个方法。 """
        pass
    @abstractmethod
    def format(self, indent_count: int) -> str: pass

class Action(ActionBase):
    """ 就是包装了一下，保证如果调用没有实现的execute和format方法时会报错。 """
    def execute(self): raise
    def format(self, indent_count: int) -> str: raise

class Actions(Action):
    """ 这个类表示一组Action的集合。format时直接将每个Action单独format之后再将字符串分行拼接。 """
    actions: list[Action]
    def __init__(self, actions: list[Action]):
        self.actions = actions
    def execute(self):
        for action in self.actions: action.execute()
    def format(self, indent_count):
        return f"\n{INDENT*indent_count}".join([a.format(indent_count) for a in self.actions])
