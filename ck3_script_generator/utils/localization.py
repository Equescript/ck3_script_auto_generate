""" 默认的描述语言会是中文，因此可以在编写Python的P语言对象时直接在需要localization键值对的地方使用中文字符串值，格式化会自动生成对应的localization key，并生成本地化翻译文件 """

from typing import TypeAlias
from enum import StrEnum

class Language(StrEnum):
    simp_chinese = "simp_chinese"
    english = "english"

DEFAULT_LOCALIZATION_TARGET = Language.simp_chinese

class Localization:
    ignore: bool
    _key: str
    """ key是由script generator自动设置的，在编写生成脚本时无需手动设置 """
    simp_chinese: str
    english: str
    def __init__(self, default: str="", *, key: str="", cn: str="", en: str="", ignore: bool=False):
        """
        Args:
            default (str): 默认的本地化文本，如果其他语言的本地化文本为空，那么它会被替换为default
            key (str): 本地化键名，默认情况下脚本会自动生成键值对，这个键名会覆盖掉原本的自动生成键名，允许你使用自定义键名
            cn (str): simp_chinese语言本地化文本
            en (str): english语言本地化文本
            ignore(bool): 默认为False，设置为True会让脚本忽略这个本地化，从而不生成相应的键值对
        """
        self.ignore = ignore
        self._key = key
        self.simp_chinese = default if cn == "" else cn
        self.english = default if en == "" else en
    @property
    def key(self) -> str:
        return self._key
    def set_key(self, key: str):
        if self._key == "":
            self._key = key
    def get_localization(self, language: Language) -> str:
        match language:
            case Language.simp_chinese: return self.simp_chinese
            case Language.english: return self.english
    def get_localization_pair(self, language: Language) -> tuple[str, str]:
        return (self._key, self.get_localization(language))
    @classmethod
    def from_LocalizedStr(cls, s: 'LocalizedStr') -> 'Localization':
        if isinstance(s, Localization):
            return s
        else:
            """ 默认本地化语言是中文 """
            return Localization(cn=s)

LocalizedStr: TypeAlias = str|Localization
""" 本地化文本，可以直接填写默认的本地化语言即中文，也可以填写Localization实现多语言本地化 """

def localization_yml(language: Language, localization: list[tuple[str, str]]) -> str:
    return f"l_{language}:"+"".join([f"\n {k}: \"{v.replace("\n", "\\n")}\"" for k, v in localization])
