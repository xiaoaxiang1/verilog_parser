import re

with open("./new_grammar.py", "r") as f:
    grammar_line_list = f.readlines()

new_grammar_line_list = []
for i, line in enumerate(grammar_line_list):
    if i == 0:
        new_grammar_line_list.append(line)
        continue

    if line.startswith("# A."):
        new_grammar_line_list.append(line)
        continue

    if re.search(r"\{\s*(\w+)\s*\}", line):
        new_line = re.sub(r"\{\s*(\w+)\s*\}", r"\1*", line)
    elif re.search(r"")

