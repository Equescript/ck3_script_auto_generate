from typing import Any
from .event import EventNamespace

class Variable:
    key_name: str
    value: Any
    def __init__(self, key_name: str, value: Any) -> None:
        self.key_name = key_name
        self.value = value

class ScopeContext:
    variables: dict[str, Any]
    def __init__(self, variables: dict[str, Any]) -> None:
        self.variables = variables

class Context:
    """ 来自早期设计想法：直接用python代码模拟P语言运行，以及时找出问题，现在这个想法过于复杂，已经被放弃，可以忽略这个方法。 """
    scope: ScopeContext
    event_namespace: dict[str, EventNamespace]
    next_event_key: str|None
    # def set_variable()
    def initialize(self, scope: ScopeContext):
        self.scope = scope
    def set_scope(self, scope: str) -> ScopeContext:
        parent_scope = self.scope
        self.scope = get_scope(scope)
        return parent_scope
    def compare(self, lhs: str, relation: str, rhs: str) -> bool:
        return True
    # def get_compare_value(self, v: str) -> Any:
        # CONTXET.scope.variables[v].value
    def trigger_event(self, event_key: str):
        self.next_event_key = event_key
    def execute(self):
        if self.next_event_key is not None:
            event_key_parts = self.next_event_key.split(".")
            self.event_namespace[event_key_parts[0]].events[int(event_key_parts[1])]
            self.next_event_key = None
# scope:actor
CONTXET: Context = Context()

def bool_to_yes(b: bool) -> str:
    return "yes" if b else "no"

def scope_character(is_male: bool) -> ScopeContext:
    return ScopeContext({
        "is_male": bool_to_yes(is_male),
        "is_female": bool_to_yes(not is_male)
    })

SCOPES: dict[str, ScopeContext] = {
    "scope:actor": scope_character(True),
    "scope:recipient": scope_character(False),
}

def get_scope(scope: str) -> ScopeContext:
    return SCOPES[scope]