from typing import Any, Literal
from ..utils import *
from .context import CONTXET
from .limit import Limit
from .action_base import *

class LiteralAction(Action):
    """ 这个表示一个字面意义的Action。

    换句话说，如果你想写一个不属于生成脚本类的Action，就可以直接使用它。它不会对你输入的字符串做任何处理直接输出，等效于直接在P语言脚本里写代码。
    """
    action: str
    def __init__(self, action: str):
        self.action = action
    def execute(self):
        pass
    def format(self, indent_count):
        return self.action

class SetVariableAction(Action):
    """ 设置变量的Action。

    格式化后的形式为：
    >>> SetVariableAction("var_a", "value_b").format(0)
    set_variable = {
        name = var_a
        value = value_b
    }
    """
    variable_name: str
    value: Any
    def __init__(self, variable_name: str, value: str|int|float|Any):
        """
        Args:
            variable_name (str): 变量名。
            value (Any): 可以接受字符串，数字等常见类型，但对于自定义类型，它必须已经实现__format__方法，以便被格式化为字符串的一部分。
        """
        self.variable_name = variable_name
        self.value = value
    def execute(self):
        CONTXET.scope.variables[self.variable_name] = self.value
    def format(self, indent_count):
        return curly_braces(indent_count, "set_variable", [f"name = {self.variable_name}", f"value = {self.value}"])

ADD = "+"
class ChangeVariableAction(Action):
    """ 修改变量的Action。P语言只支持加法和乘法。

    格式化后的形式为：
    >>> ChangeVariableAction("var_a", "*", 3).format(0)
    change_variable = {
        name = var_a
        multiply = 3
    }
    """
    variable_name: str
    operation: str
    value: Any
    def __init__(self, variable_name: str, operation: Literal['+', '*'], value: Any):
        """
        Args:
            variable_name (str): 变量名。
            operation: (Literal['+', '*']): 运算类型，由于P语言限制，只支持加法和乘法。
            value (Any): 可以接受字符串，数字等常见类型，但对于自定义类型，它必须已经实现__format__方法，以便被格式化为字符串的一部分。
        """
        self.variable_name = variable_name
        self.operation = operation
        self.value = value
    def execute(self):
        match self.operation:
            case "add": CONTXET.scope.variables[self.variable_name] += self.value
            case "multiply": CONTXET.scope.variables[self.variable_name] *= self.value
            case _: raise
    def format(self, indent_count):
        return curly_braces(indent_count, "change_variable", [f"name = {self.variable_name}", f"{self.operation} = {self.value}"])

class RemoveVariableAction(Action):
    """ 移除变量的Action。

    格式化后的形式为：
    >>> RemoveVariableAction("var_a").format(0)
    remove_variable = var_a
    """
    variable_name: str
    def __init__(self, variable_name: str):
        self.variable_name = variable_name
    def execute(self):
        del CONTXET.scope.variables[self.variable_name]
    def format(self, indent_count):
        return f"remove_variable = {self.variable_name}"

class TriggerEventAction(Action):
    """ 触发事件的Action。

    格式化后的形式为：
    >>> TriggerEventAction("event.001").format(0)
    trigger_event = event.001
    """
    event_key: str
    def __init__(self, event_key: str):
        self.event_key = event_key
    def execute(self):
        CONTXET.trigger_event(self.event_key)
    def format(self, indent_count):
        return f"trigger_event = {self.event_key}"

class If(Action):
    """ 带条件判断的Action。 """
    if_limit: Limit
    if_action: Action
    else_if_limit_actions: list[tuple[Limit, Action]]
    else_action: Action|None
    def __init__(self, if_limit: Limit, if_action: Action, else_if_limit_actions: list[tuple[Limit, Action]]=[], else_action: Action|None=None):
        self.if_limit = if_limit
        self.if_action = if_action
        self.else_if_limit_actions = else_if_limit_actions
        self.else_action = else_action
    def execute(self):
        if self.if_limit.is_satisfied():
            self.if_action.execute()
        else:
            for limit, action in self.else_if_limit_actions:
                if limit.is_satisfied():
                    action.execute()
                    return
            if self.else_action is not None: self.else_action.execute()
    def format(self, indent_count):
        branches = []
        branches.append(curly_braces(indent_count, "if", [
            curly_braces(indent_count+1, "limit", [self.if_limit.format(indent_count+2)]),
            self.if_action.format(indent_count+1),
        ]))
        for limit, action in self.else_if_limit_actions:
            branches.append(curly_braces(indent_count, "else_if", [
                curly_braces(indent_count+1, "limit", [limit.format(indent_count+2)]),
                action.format(indent_count+1),
            ]))
        if self.else_action is not None: branches.append(curly_braces(indent_count, "else", [self.else_action.format(indent_count+1)]))
        return Actions([LiteralAction(branch) for branch in branches]).format(indent_count)

class Effect(Action):
    key: str
    action: Action
    def __init__(self, key: str, action: list[Action]|Action):
        self.key = key
        self.action = Actions(action) if isinstance(action, list) else action
    def execute(self):
        self.action.execute()
    def format(self, indent_count):
        return curly_braces(0, self.key, [self.action.format(indent_count+1)])
    def __call__(self, *args, **kwds):
        return EffectCall(self)

class EffectCall(Action):
    effect: Effect
    def __init__(self, effect: Effect) -> None:
        self.effect = effect
    def execute(self):
        self.effect.execute()
    def format(self, indent_count: int) -> str:
        return f"{self.effect.key} = yes"
