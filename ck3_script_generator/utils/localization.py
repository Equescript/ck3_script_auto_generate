from typing import TypeAlias



class Localization:
    chinese: str
    english: str
    def __init__(self, chinese: str, english: str=""):
        self.chinese = chinese
        self.english = english

L: TypeAlias = Localization
