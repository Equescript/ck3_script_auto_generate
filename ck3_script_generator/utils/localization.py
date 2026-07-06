""" 默认的描述语言会是中文，因此可以在编写Python的P语言对象时直接在需要localization键值对的地方使用中文字符串值，格式化会自动生成对应的localization key，并生成本地化翻译文件 """

from typing import TypeAlias
from enum import StrEnum

class Localization:
    english: str
    chinese: str
    def __init__(self, english: str, chinese: str):
        self.english = english
        self.chinese = chinese

LocalizedStr: TypeAlias = str|Localization
""" 本地化文本，可以直接填写默认的本地化语言即中文，也可以填写Localization实现多语言本地化 """

class Language(StrEnum):
    English = "english"
    Chinese = "simp_chinese"

DEFAULT_LOCALIZATION_TARGET = Language.Chinese

def localization_yml(language: Language, localization: list[tuple[str, str]]) -> str:
    return f"l_{language}:"+"".join([f"\n {k}: \"{v.replace("\n", "\\n")}\"" for k, v in localization])
