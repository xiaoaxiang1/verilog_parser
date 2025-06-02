from lark import Lark

grammar = """
start : INTEGER | DECIMAL
INTEGER : /[0-9]+/
DECIMAL.2: INTEGER ( "." INTEGER )* //# Will be matched before INTEGER
%import common.WS
%ignore WS
"""

parser = Lark(grammar, start='start')

# 合法用例（将被正确解析）
print(parser.parse("1.1").pretty())    # 通过
print(parser.parse("2.2.3").pretty())       # 通过

# 非法用例（将抛出异常）
#try:
#    print(parser.parse("top . u1").pretty()) # 报错：点号周围有空格
#except Exception as e:
#    print(f"Expected error: {e}")
#
#try:
#    print(parser.parse("top. u1").pretty())  # 报错
#except Exception as e:
#    print(f"Expected error: {e}")