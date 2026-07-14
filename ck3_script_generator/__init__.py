from .ck3_backend_definitions import *
from .utils import *

import os

class GenerationConfig:
    root_dir: str
    localization_languages: list[Language]
    file_prefix: str
    file_postfix: str
    def __init__(self, root_dir: str, languages: list[Language], file_prefix: str="", file_postfix: str="") -> None:
        self.root_dir = root_dir
        self.localization_languages = languages
        self.file_prefix = file_prefix
        self.file_postfix = file_postfix
    def write_file(self, local_path: str, paradox_object: ParadoxObject, enable_prefix: bool=True, enable_postfix: bool=True):
        basename_splits = os.path.basename(local_path).split('.')
        assert len(basename_splits) == 2
        filename = f"{self.file_prefix if enable_prefix else ""}{basename_splits[0]}{self.file_postfix if enable_postfix else ""}.{basename_splits[1]}"
        localpath = os.path.join(os.path.dirname(local_path), filename)
        path = os.path.join(self.root_dir, localpath)
        write_file(path, paradox_object.format())
    def write_localization(self, local_path: str, paradox_object: ParadoxObject, enable_prefix: bool=True, enable_postfix: bool=True):
        basename_splits = os.path.basename(local_path).split('.')
        assert len(basename_splits) == 2
        filename = f"{self.file_prefix if enable_prefix else ""}{basename_splits[0]}{self.file_postfix if enable_postfix else ""}.{basename_splits[1]}"
        localpath = os.path.join(os.path.dirname(local_path), filename)
        for language in self.localization_languages:
            path = os.path.join(os.path.join(self.root_dir, f"localization/{language}"), localpath)
            write_file(path, paradox_object.localization(language))
