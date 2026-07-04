from abc import ABC, abstractmethod
from ..utils import *

class Action(ABC):
    # @abstractmethod
    # def set_scope(self, scope: str):
        # pass
    @abstractmethod
    def execute(self):
        pass
    @abstractmethod
    def format(self, indent_count: int) -> str:
        pass
"""
class Action(ActionBase):
    # scope: str
    # def set_scope(self, scope: str):
        # self.scope = scope
    def execute(self):
        pass
    # def format(self, indent_count: int) -> str:
        # raise
 """
class Actions(Action):
    actions: list[Action]
    def __init__(self, actions: list[Action]):
        self.actions = actions
    def execute(self):
        for action in self.actions: action.execute()
    def format(self, indent_count):
        return f"\n{INDENT*indent_count}".join([a.format(indent_count) for a in self.actions])
