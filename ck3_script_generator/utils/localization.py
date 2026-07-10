""" 默认的描述语言会是中文，因此可以在编写Python的P语言对象时直接在需要localization键值对的地方使用中文字符串值，格式化会自动生成对应的localization key，并生成本地化翻译文件 """

from typing import TypeAlias
from enum import StrEnum

class Language(StrEnum):
    Chinese = "simp_chinese"
    English = "english"

DEFAULT_LOCALIZATION_TARGET = Language.Chinese

class Localization:
    _key: str
    """ key是由script generator自动设置的，在编写生成脚本时无需手动设置 """
    chinese: str
    english: str
    def __init__(self, *, chinese: str, english: str=""):
        self._key = None
        self.chinese = chinese
        self.english = english
    @property
    def key(self) -> str:
        return self._key
    def get_localization(self, language: Language) -> str:
        match language:
            case Language.Chinese: return self.chinese
            case Language.English: return self.english
    def get_localization_pair(self, language: Language) -> tuple[str, str]:
        return (self._key, self.get_localization(language))
    @classmethod
    def from_LocalizedStr(cls, s: 'LocalizedStr') -> 'Localization':
        if isinstance(s, Localization):
            return s
        else:
            """ 默认本地化语言是中文 """
            return Localization(chinese=s)

LocalizedStr: TypeAlias = str|Localization
""" 本地化文本，可以直接填写默认的本地化语言即中文，也可以填写Localization实现多语言本地化 """

def localization_yml(language: Language, localization: list[tuple[str, str]]) -> str:
    return f"l_{language}:"+"".join([f"\n {k}: \"{v.replace("\n", "\\n")}\"" for k, v in localization])
