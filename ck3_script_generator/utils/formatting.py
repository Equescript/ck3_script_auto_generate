INDENT = "    "

def curly_braces(indent_count: int, prefix: str, contents: list[str], add_line_feed_for_conetents: bool=True) -> str:
    """
    将字符串格式化为p语言脚本的常用花括号格式。

    Args:
        indent_count (int): 控制开头缩进的数量。0代表无缩写。
        prefix (str): 前缀。
        contents (list[str]): 花括号里的具体内容，list中的每一个str都代表一行。
        add_line_feed_for_conetents (bool): 是否在每一行后都添加换行，设置成false的话就会被压缩到一行。
    Returns:
        str: 格式化后的p语言字符串。

    Examples:
        >>> curly_braces(0, "key", ["str1", "str1"])
        'key = {\\n    str1\\n    str1\\n}'
        key = {
            str1
            str2
        }
    """
    indent = INDENT * indent_count
    # if add_line_feed_for_conetents:
    #     contents = "".join(["\n" if ignore_empty_line and content=="" else f"{indent}{INDENT}{content}\n" for content in contents])
    # else:
    #     contents = "".join(["\n" if ignore_empty_line and content=="\n" else f"{indent}{INDENT}{content}" for content in contents])
    if add_line_feed_for_conetents:
        contents_joined = "".join([f"{indent}{INDENT}{content}\n" for content in contents])
    else:
        contents_joined = "".join([f"{indent}{INDENT}{content}" for content in contents])
    return f"{prefix} = {{\n{contents_joined}{indent}}}"


def localization_yml(localization: list[tuple[str, str]]) -> str:
    return "l_simp_chinese:\n "+"\n ".join([f"{k}: \"{v.replace("\n", "\\n")}\"" for k, v in localization])
