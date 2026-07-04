INDENT = "    "

def curly_braces(indent_count: int, prefix: str, contents: list[str], add_line_feed_for_conetents: bool=True) -> str:
    """ 将字符串格式化为p语言脚本的常用花括号格式 """
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
