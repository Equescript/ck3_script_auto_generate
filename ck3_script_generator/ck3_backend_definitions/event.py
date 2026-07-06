from itertools import chain
from typing import Any
from enum import StrEnum
from ..utils import *
from .action_base import *

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
    animation: str
    def __init__(self, portrait_pos: PortraitPos, character: str, animation: str):
        self.portrait_pos = portrait_pos
        self.character = character
        self.animation = animation
    def format(self, indent_count: int) -> str:
        return curly_braces(indent_count, self.portrait_pos, [
            f"character = {self.character}",
            f"animation = {self.animation}",
        ])

class Option:
    """ 用来储存事件选项的相关数据 """
    name: LocalizedStr
    action: Action|None
    # event_ref: int|str|None
    localization: tuple[str, str]
    def __init__(self, name: LocalizedStr, action: list[Action]|Action|None=None):
        """
        Args:
            name (LocalizedStr): 选项名称，可以直接写本地化字符串
            action (list[Action] | Action | None): 选项会执行的操作，可以不填，默认为None，即不执行任何操作。
        """
        self.name = name
        # 初始化的时候直接就把list[Action]转化成Actions类了，这样就可以都作为一个单独的Action处理，非常方便
        self.action = Actions(action) if isinstance(action, list) else action
        # self.event_ref = event_ref
    def format(self, indent_count: int, event_key: str, option_key: str) -> str:
        full_option_key = f"{event_key}.option.{option_key}"
        contents = [f"name = {full_option_key}"]
        if self.action is not None:
            contents.append(self.action.format(indent_count+1))
        self.localization = (full_option_key, self.name)
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
    index: int
    event_type: EventType
    theme: str
    title: LocalizedStr
    description: LocalizedStr
    portraits: list[Portrait]
    options: list[Option]

    localizations: dict[str, str]
    def __init__(self, index: int, event_type: EventType, theme: str, portraits: list[Portrait], title: LocalizedStr, description: LocalizedStr, options: list[Option]):
        """
        Args:
            index (int): 事件索引，被格式化填充到四位，例如1会被填充成0001。
            event_type (EventType): 事件类型。
            theme (str): 参考https://ck3.paradoxwikis.com/Event_modding#Themes
            portraits (list[Portrait]): 出现在事件界面的头像列表
            title (LocalizedStr): 标题，可以直接写本地化字符串
            description (LocalizedStr): 事件内容描述，可以直接写本地化字符串
            options (list[Option]): 事件选项
        """
        # self.name_space = name_space
        self.index = index
        self.event_type = event_type
        self.theme = theme
        self.title = title
        self.description = description
        self.portraits = portraits
        self.options = options

        self.localizations = {}
    def option_format(self, event_key: str, o: Option, i: int) -> str:
        return o.format(1, event_key, chr(97+i))
    def format(self, name_space: str) -> str:
        # 构建P语言的key
        event_key = f"{name_space}.{self.index:04d}"
        event_title_key = f"{event_key}.t"
        event_desc_key = f"{event_key}.desc"
        # 生成localization键值对
        self.localizations[event_title_key] = self.title
        self.localizations[event_desc_key] = self.description
        return curly_braces(0, event_key, list(chain([
            f"type = {self.event_type}",
            f"theme = {self.theme}",
            f"title = {event_title_key}",
            f"desc = {event_desc_key}",
            ], [""],
            [p.format(1) for p in self.portraits], [""],
            [self.option_format(event_key, o, i) for i, o in enumerate(self.options)]
        )))
    def trigger_event(self):
        pass

class EventNamespace:
    name_space: str
    events: dict[int, Event]
    def __init__(self, name_space: str, events: list[Event]):
        self.name_space = name_space
        self.events = dict([(e.index, e) for e in events])
    def format(self) -> str:
        return f"namespace = {self.name_space}\n\n"+"\n\n".join([e.format(self.name_space) for e in self.events.values()])
    def localization(self) -> str:
        return localization_yml(DEFAULT_LOCALIZATION_TARGET, [kv for e in self.events.values() for kv in chain(e.localizations.items(), [option.localization for option in e.options])])
        # return [kv for e in self.events.values() for kv in list(e.localizations.items()).append([option.localization for option in e.options])]
    # def generate(self, event_path: str, localization_path: str):
    #     event_data = f"namespace = {self.name_space}\n\n"+"\n\n".join([e.format(self.name_space) for e in self.events.values()])
    #     localization_data = localization_yml([kv for e in self.events.values() for kv in list(e.localizations.items()).append([option.localization for option in e.options])])
    #     write_file(event_path, event_data)
    #     write_file(localization_path, localization_data)
