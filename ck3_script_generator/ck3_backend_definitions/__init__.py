"""ck3_backend_definitions

这个模块储存了整个 CK3 脚本生成器的后端定义。里面的python对象和p语言的脚本对象是一一对应的。所有对象都拥有一个format方法，用于将Python对象格式化为P语言脚本代码字符串，参数为indent_count: int，代表格式化时的缩进数量，返回值为格式化后的字符串。
"""

