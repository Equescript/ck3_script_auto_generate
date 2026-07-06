INDENT = "    "

def curly_braces(indent_count: int, prefix: str, contents: list[str], add_line_feed_for_conetents: bool=True) -> str:
    """
    将字符串格式化为p语言脚本的常用花括号格式。

    Args:
        indent_count (int): 控制开头缩进的数量。0代表无缩写。
        prefix (str): 前缀。
        contents (list[str]): 花括号里的具体内容，list中的每一个str都代表一行，注意这些str被假定没有前缀和后缀的缩进空格。
        add_line_feed_for_conetents (bool): 是否在每一行后都添加换行，设置成false的话就会被压缩到一行。
    Returns:
        str: 格式化后的p语言字符串。

    Examples:
        >>> curly_braces(0, "key", ["str1", "str2"])
        'key = {\\n        str1\\n        str2\\n    }'
        p语言中显示为：
        key = {
                str1
                str2
            }
        注意第一行的key之前没有缩进，这是为了方便嵌套格式化，参考函数的contents参数
    """
    indent = INDENT * indent_count
    if add_line_feed_for_conetents:
        contents_joined = "\n"+"".join([f"{indent}{INDENT}{content}\n" for content in contents])+indent
    else:
        contents_joined = "".join([f"{INDENT}{content}" for content in contents])+INDENT
    return f"{prefix} = {{{contents_joined}}}"

if __name__ == "__main__":
    print(curly_braces(1, "key", ["str1", "str2"], False))
