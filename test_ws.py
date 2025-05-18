from lark import Lark

grammar = """
?start: inst_name
inst_name: TOP_ID ( "." INST_ID )*
TOP_ID: ID
INST_ID: ID
ID: /[a-zA-Z_][a-zA-Z0-9_]*/
%import common.WS
%ignore WS
"""

parser = Lark(grammar, start='start')

# 合法用例（将被正确解析）
print(parser.parse("top.u1.u2").pretty())    # 通过
print(parser.parse("top.u1").pretty())       # 通过

# 非法用例（将抛出异常）
try:
    print(parser.parse("top . u1").pretty()) # 报错：点号周围有空格
except Exception as e:
    print(f"Expected error: {e}")

try:
    print(parser.parse("top. u1").pretty())  # 报错
except Exception as e:
    print(f"Expected error: {e}")