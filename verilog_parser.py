from lark import Lark
import new_grammar_edit

vparser = Lark(new_grammar_edit.grammar, parser="lalr")
file_path = "~/gitview/basic_ip/debounce.v"
with open(file_path, "r") as f:
    text = f.read()
tree = vparser.parse(text)
print(tree.pretty())