from itertools import chain
from typing import Any
from ..utils import *
from .action_base import *

class Portrait:
    portrait_type: str
    character: str
    animation: str
    def __init__(self, portrait_type: str, character: str, animation: str):
        self.portrait_type = portrait_type
        self.character = character
        self.animation = animation
    def format(self, indent_count: int) -> str:
        return curly_braces(indent_count, self.portrait_type, [
            f"character = {self.character}",
            f"animation = {self.animation}",
        ])

class Option:
    description: str
    action: Action|None
    # event_ref: int|str|None
    def __init__(self, description: str, action: list[Action]|Action|None=None):
        self.description = description
        self.action = Actions(action) if isinstance(action, list) else action
        # self.event_ref = event_ref
    def format(self, indent_count: int, event_key: str, option_key: str) -> tuple[str, str]:
        full_option_key = f"{event_key}.option.{option_key}"
        contents = [f"name = {full_option_key}"]
        if self.action is not None:
            contents.append(self.action.format(indent_count+1))
        return curly_braces(indent_count, "option", contents), full_option_key

class Event:
    name_spcae: str
    index: int
    event_type: str
    theme: str
    title: str
    description: str
    portraits: list[Portrait]
    options: list[Option]

    localizations: dict[str, str]
    def __init__(self, name_spcae: str, index: int, event_type: str, theme: str, portraits: list[Portrait], title: str, description: str, options: list[Option]):
        self.name_spcae = name_spcae
        self.index = index
        self.event_type = event_type
        self.theme = theme
        self.title = title
        self.description = description
        self.portraits = portraits
        self.options = options

        self.localizations = {}
    def option_format(self, event_key: str, o: Option, i: int) -> str:
        option_format, option_key = o.format(1, event_key, chr(97+i))
        self.localizations[option_key] = o.description
        return option_format
    def format(self) -> str:
        event_key = f"{self.name_spcae}.{self.index:04d}"
        event_title_key = f"{event_key}.t"
        event_desc_key = f"{event_key}.desc"
        self.localizations[event_title_key] = self.title
        self.localizations[event_desc_key] = self.description
        contents = list(chain([
            f"type = {self.event_type}",
            f"theme = {self.theme}",
            f"title = {event_title_key}",
            f"desc = {event_desc_key}",
            ], [""],
            [p.format(1) for p in self.portraits], [""],
            [self.option_format(event_key, o, i) for i, o in enumerate(self.options)]
        ))
        return curly_braces(0, event_key, contents)
    def trigger_event(self):
        pass

class EventNamespace:
    name_space: str
    events: dict[int, Event]
    def __init__(self, name_space: str, events: list[Event]):
        self.name_space = name_space
        self.events = dict([(e.index, e) for e in events])
    def format(self) -> str:
        return f"namespace = {self.name_space}\n\n"+"\n\n".join([e.format() for e in self.events.values()])
    def generate(self, event_path: str, localization_path: str):
        event_data = f"namespace = {self.name_space}\n\n"+"\n\n".join([e.format() for e in self.events.values()])
        localization_data = localization_yml([kv for e in self.events.values() for kv in e.localizations.items()])
        write_file(event_path, event_data)
        write_file(localization_path, localization_data)
