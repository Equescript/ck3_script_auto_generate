from typing import Any
from ..utils import *
from .context import CONTXET
from .limit import Limit
from .action_base import *

class LiteralAction(Action):
    action: str
    def __init__(self, action: str):
        self.action = action
    def execute(self):
        pass
    def format(self, indent_count):
        return self.action

class SetVariableAction(Action):
    variable: str
    value: Any
    def __init__(self, variable: str, value):
        self.variable = variable
        self.value = value
    def execute(self):
        CONTXET.scope.variables[self.variable] = self.value
    def format(self, indent_count):
        return curly_braces(indent_count, "set_variable", [f"name = {self.variable}", f"value = {self.value}"])

class ChangeVariableAction(Action):
    variable: str
    operation: str
    value: Any
    def __init__(self, variable: str, operation: str, value: Any):
        self.variable = variable
        self.operation = operation
        self.value = value
    def execute(self):
        match self.operation:
            case "add": CONTXET.scope.variables[self.variable] += self.value
            case "multiply": CONTXET.scope.variables[self.variable] *= self.value
            case _: raise
    def format(self, indent_count):
        return curly_braces(indent_count, "change_variable", [f"name = {self.variable}", f"{self.operation} = {self.value}"])

class RemoveVariableAction(Action):
    variable: str
    def __init__(self, variable: str):
        self.variable = variable
    def execute(self):
        del CONTXET.scope.variables[self.variable]
    def format(self, indent_count):
        return f"remove_variable = {self.variable}"

class TriggerEventAction(Action):
    event_key: str
    def __init__(self, event_key: str):
        self.event_key = event_key
    def execute(self):
        CONTXET.trigger_event(self.event_key)
    def format(self, indent_count):
        return f"trigger_event = {self.event_key}"

class If(Action):
    if_limit: Limit
    if_action: Action
    else_if: list[tuple[Limit, Action]]
    else_action: Action|None
    def __init__(self, if_limit: Limit, if_action: Action, else_if: list[tuple[Limit, Action]]=[], else_action: Action|None=None):
        self.if_limit = if_limit
        self.if_action = if_action
        self.else_if = else_if
        self.else_action = else_action
    def execute(self):
        if self.if_limit.is_satisfied():
            self.if_action.execute()
        else:
            for limit, action in self.else_if:
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
        for limit, action in self.else_if:
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
