from .action_base import *
from .limit_base import *
from itertools import chain

class Interaction:
    key: str
    name: str
    description: str
    category: str
    # icon: str
    # interface_priority
    options: list[str]
    is_shown: Limit
    on_accept: Action
    on_decline: Action|None
    auto_accept: Limit|bool
    ai_accept: Limit|None
    def __init__(self, key: str, name: str, description: str, category: str, options: list[str], is_shown: Limit,
                 on_accept: Action, on_decline: Action|None=None, auto_accept: Limit|bool=True, ai_accept: Limit|None=None):
        self.key = key
        self.name = name
        self.description = description
        self.category = category
        self.options = options
        self.is_shown = is_shown
        self.on_accept = on_accept
        self.on_decline = on_decline
        self.auto_accept = auto_accept
        self.ai_accept = ai_accept
    def format(self, indent_count: int) -> str:
        contents = list(chain([
            f"desc = {self.key}_desc",
            f"category = {self.category}"
        ], self.options,
        ["", curly_braces(indent_count+1, "is_shown", [self.is_shown.format(indent_count+2)])],
        ["", curly_braces(indent_count+1, "on_accept", [self.on_accept.format(indent_count+2)])],
        ["", curly_braces(indent_count+1, "on_decline", [self.on_decline.format(indent_count+2)])] if self.on_decline is not None else [],
        ["", curly_braces(indent_count+1, "auto_accept", [self.auto_accept.format(indent_count+2)])] if isinstance(self.auto_accept, Limit) else ["", f"auto_accept = {"yes" if self.auto_accept else "no"}"],
        ["", curly_braces(indent_count+1, "ai_accept", [self.ai_accept.format(indent_count+2)])] if self.ai_accept is not None else [],
        ))
        return curly_braces(indent_count, self.key, [content for content in contents if content is not None])
