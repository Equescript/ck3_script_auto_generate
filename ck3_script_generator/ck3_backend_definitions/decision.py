from .action_base import Action
from ..utils import *

class Decision:
    key: str
    name: str
    tooltip: str
    description: str
    effect_tooltip: str
    confirm: str
    picture: str
    effect: Action
    def __init__(self, key: str, name: str, tooltip: str, description: str, effect_tooltip: str, confirm: str, picture: str, effect: Action):
        self.key = key
        self.name = name
        self.tooltip = tooltip
        self.description = description
        self.effect_tooltip = effect_tooltip
        self.confirm = confirm
        self.picture = picture
        self.effect = effect
    def format(self, indent_count: int) -> str:
        return curly_braces(indent_count, self.key, [])
