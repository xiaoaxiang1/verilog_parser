import re


def replace_braces(line):
    pattern = r'\{([^{}]*)\}'
    matches = re.findall(pattern, line)

    if matches:
        line = re.sub(pattern, r'(\1)*', line)
        return replace_braces(line)
    else:
        return line


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
        line = re.sub(r"\{\s*(\w+)\s*\}", r"\1*", line)
    
    if re.search(r'"\{"', line):
        line = re.sub(r'"\{"', r'"lbraces"', line)
	
    if re.search(r'"\}"', line):
        line = re.sub(r'"\}"', r'"rbraces"', line)
	
    line = replace_braces(line)

    if re.search(r'"lbraces"', line):
        line = re.sub(r'"lbraces"', '"{"', line)
	
    if re.search(r'"rbraces"', line):
        line = re.sub(r'"rbraces"', '"}"', line)

    new_grammar_line_list.append(line)

with open("./new_grammar_edit.py", "w+")  as f:
    f.writelines(new_grammar_line_list)
#print(new_grammar_line_list)
