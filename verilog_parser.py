from lark import Lark
import new_grammar_edit_identifier

vparser = Lark(new_grammar_edit_identifier.grammar, parser="earley")
file_path = "~/gitview/basic_ip/debounce.v"
with open(file_path, "r") as f:
    text = f.read()
tree = vparser.parse(text)
print(tree.pretty())