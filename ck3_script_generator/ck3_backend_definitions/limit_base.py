from abc import ABC, abstractmethod
from ..utils import *

class LimitBase(ABC):
    # @abstractmethod
    # def set_scope(self, scope: str):
        # pass
    @abstractmethod
    def is_satisfied(self) -> bool:
        pass
    @abstractmethod
    def format(self, indent_count: int) -> str: pass

class Limit(LimitBase):
    """ 就是包装了一下，保证如果调用没有实现的execute和format方法时会报错。 """
    def is_satisfied(self) -> bool: raise
    def format(self, indent_count: int) -> str: raise

class LiteralLimit(Limit):
    limit: str
    def __init__(self, limit: str): self.limit = limit
    def is_satisfied(self) -> bool: return True
    def format(self, indent_count): return self.limit

class AND(Limit):
    limits: list[Limit]
    def __init__(self, limits: list[Limit]): self.limits = limits
    def is_satisfied(self): return all([limit.is_satisfied() for limit in self.limits])
    def format(self, indent_count): return curly_braces(indent_count, "AND", [limit.format(indent_count+1) for limit in self.limits])
class OR(Limit):
    limits: list[Limit]
    def __init__(self, limits: list[Limit]): self.limits = limits
    def is_satisfied(self): return any([limit.is_satisfied() for limit in self.limits])
    def format(self, indent_count): return curly_braces(indent_count, "OR", [limit.format(indent_count+1) for limit in self.limits])
class NOT(Limit):
    limit: Limit
    def __init__(self, limit: Limit): self.limit = limit
    def is_satisfied(self): return not self.limit.is_satisfied()
    def format(self, indent_count): return f"NOT = {{ {self.limit.format(indent_count)} }}"
