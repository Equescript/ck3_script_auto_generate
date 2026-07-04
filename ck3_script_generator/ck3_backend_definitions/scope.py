from typing import TypeAlias
from .action_base import Action
from .limit_base import Limit
from .context import CONTXET
from ..utils import *

ScopeContent: TypeAlias = Action|Limit

class Scope(Action, Limit):
    scope: str
    content: ScopeContent
    def __init__(self, scope: str, content: ScopeContent):
        self.scope = scope
        self.content = content
    def is_satisfied(self):
        parent_scope = CONTXET.set_scope(self.scope)
        result = self.content.is_satisfied() if isinstance(self.content, Limit) else True
        CONTXET.scope = parent_scope
        return result
    def execute(self):
        parent_scope = CONTXET.set_scope(self.scope)
        if isinstance(self.content, Action): self.content.execute()
        CONTXET.scope = parent_scope
    def format(self, indent_count: int) -> str:
        return curly_braces(indent_count, self.scope, [self.content.format(indent_count+1)])

