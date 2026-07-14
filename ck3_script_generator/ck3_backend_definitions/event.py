from itertools import chain
from typing import Any
from enum import StrEnum
from ..utils import *
from .action_base import *
from .paradox_object import *

class PortraitPos(StrEnum):
    """ 参考https://ck3.paradoxwikis.com/Event_modding#Portrait_Positions """
    left_portrait = "left_portrait"
    right_portrait = "right_portrait"
    lower_left_portrait = "lower_left_portrait"
    lower_center_portrait = "lower_center_portrait"
    lower_right_portrait = "lower_right_portrait"

class Portrait:
    """ 用来储存事件界面中显示的角色的相关数据 """
    portrait_pos: PortraitPos
    character: str
    animation: str|None
    def __init__(self, portrait_pos: PortraitPos, character: str, animation: str|None=None):
        self.portrait_pos = portrait_pos
        self.character = character
        self.animation = animation
    def format(self, indent_count: int) -> str:
        if self.animation is None:
            return f"{self.portrait_pos} = {self.character}"
        else:
            return curly_braces(indent_count, self.portrait_pos, [f"character = {self.character}", f"animation = {self.animation}"])

class Option:
    """ 用来储存事件选项的相关数据 """
    name: Localization
    action: Action|None
    # event_ref: int|str|None
    # localization: tuple[str, str]
    def __init__(self, name: LocalizedStr, action: list[Action]|Action|None=None):
        """
        Args:
            name (LocalizedStr): 选项名称，可以直接写本地化字符串
            action (list[Action] | Action | None): 选项会执行的操作，可以不填，默认为None，即不执行任何操作
        """
        self.name = name if isinstance(name, Localization) else Localization(name)
        # 初始化的时候直接就把list[Action]转化成Actions类了，这样就可以都作为一个单独的Action处理，非常方便
        self.action = Actions(action) if isinstance(action, list) else action
        # self.event_ref = event_ref
    def format(self, indent_count: int, event_key: str, option_key: str) -> str:
        self.name.set_key(f"{event_key}.option.{option_key}")
        contents = [f"name = {self.name.key}"]
        if self.action is not None:
            contents.append(self.action.format(indent_count+1))
        # self.localization = (full_option_key, self.name)
        return curly_braces(indent_count, "option", contents)

class EventType(StrEnum):
    """ 参考https://ck3.paradoxwikis.com/Event_modding#Flags """
    character_event = "character_event"
    letter_event = "letter_event"
    duel_event = "duel_event"
    none = "none"
    empty = "empty"

class Event:
    """ P语言的Event对象，必须被包裹在一个EventNamespace中使用，否则将没有name_space """
    index: str
    event_type: EventType
    theme: str
    portraits: list[Portrait]
    title: Localization
    description: Localization
    immediate: Action|None
    options: list[Option]
    orphan: bool
    hidden: bool
    others: list[str]

    # localizations: dict[str, Localization]
    def __init__(self, index: str, event_type: EventType, *, theme: str="default", portraits: Portrait|list[Portrait]=[],
                 title: LocalizedStr=Localization(ignore=True), description: LocalizedStr=Localization(ignore=True), immediate: list[Action]|Action|None=None,
                 options: list[Option]=[], orphan: bool=False, hidden: bool=False, others: list[str]=[]):
        """
        Args:
            index (int): 事件索引，被格式化填充到四位，例如1会被填充成0001。
            event_type (EventType): 事件类型。
            theme (str): 参考Crusader Kings III/game/common/event_themes/00_event_themes.txt
            portraits (Portrait | list[Portrait]): 出现在事件界面的头像列表
            title (LocalizedStr): 标题，可以直接写本地化字符串
            description (LocalizedStr): 事件内容描述，可以直接写本地化字符串
            immediate (list[Action] | Action | None): 事件会立即执行的Action，可以不填，默认为None，即不执行任何操作
            options (list[Option]): 事件选项
            orphan (bool): 事件Flag，让事件孤立发生
            hidden (bool): 事件Flag，让事件发生时对于玩家隐藏
            others (list[str]): 其他想要加入Event的P语言内容，会直接格式化在P语言字符串中
        """
        # self.name_space = name_space
        self.index = index
        self.event_type = event_type
        self.theme = theme
        self.portraits = [portraits] if isinstance(portraits, Portrait) else portraits
        self.title = title if isinstance(title, Localization) else Localization(title)
        self.description = description if isinstance(description, Localization) else Localization(description)
        self.immediate = Actions(immediate) if isinstance(immediate, list) else immediate
        self.options = options
        self.orphan = orphan
        self.hidden = hidden
        self.others = others

        # self.localizations = {}
    def option_format(self, event_key: str, o: Option, i: int) -> str:
        return o.format(1, event_key, chr(97+i))
    def format(self, name_space: str) -> str:
        # 构建P语言的key
        # event_key = f"{name_space}.{self.index:04d}"
        event_key = f"{name_space}.{self.index}"
        self.title.set_key(f"{event_key}.t")
        self.description.set_key(f"{event_key}.desc")
        return curly_braces(0, event_key, list(chain(
            ["orphan = yes"] if self.orphan else [],
            ["hidden = yes"] if self.hidden else [],
            [f"type = {self.event_type}", f"theme = {self.theme}"],
            [f"title = {self.title.key}"] if self.title.ignore == False else [],
            [f"desc = {self.description.key}"] if self.description.ignore == False else [],
            [""],
            [p.format(1) for p in self.portraits], [] if len(self.portraits) == 0 else [""],
            [] if self.immediate is None else [curly_braces(1, "immediate", [self.immediate.format(2)]), ""],
            [self.option_format(event_key, o, i) for i, o in enumerate(self.options)],
            self.others
        )))
    def trigger_event(self):
        pass

class EventNamespace(ParadoxObject):
    name_space: str
    events: dict[str, Event]
    other_localizations: list[Localization]
    def __init__(self, name_space: str, events: list[Event], other_localizations: list[Localization]=[]):
        self.name_space = name_space
        self.events = dict([(e.index, e) for e in events])
        self.other_localizations = other_localizations
    def format(self) -> str:
        return f"namespace = {self.name_space}\n\n"+"\n\n".join([e.format(self.name_space) for e in self.events.values()])
    def localization(self, language: Language) -> str:
        return localization_yml(language, list(chain(
            [l.get_localization_pair(language) for l in self.other_localizations],
            [kv for e in self.events.values() for kv in chain(
                [e.title.get_localization_pair(language)] if e.title.ignore == False else [], [e.description.get_localization_pair(language)] if e.description.ignore == False else [],
                [option.name.get_localization_pair(language) for option in e.options]
            )]
        )))
        # return [kv for e in self.events.values() for kv in list(e.localizations.items()).append([option.localization for option in e.options])]
    # def generate(self, event_path: str, localization_path: str):
    #     event_data = f"namespace = {self.name_space}\n\n"+"\n\n".join([e.format(self.name_space) for e in self.events.values()])
    #     localization_data = localization_yml([kv for e in self.events.values() for kv in list(e.localizations.items()).append([option.localization for option in e.options])])
    #     write_file(event_path, event_data)
    #     write_file(localization_path, localization_data)
