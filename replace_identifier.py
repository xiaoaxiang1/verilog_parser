import re

with open("./new_grammar_edit.py", "r") as f:
    grammar_line_list = f.readlines()


identifier_list = []
identifier_ptn = re.compile(r"^([a-z0-9_]+_identifier) : IDENTIFIER([\s#]$)")
for i, line in enumerate(grammar_line_list):
    if identifier_ptn.search(line):
        identifier_list.append(identifier_ptn.search(line)[1])
        print(identifier_ptn.search(line)[1])

new_grammar_line_list = []
for i, line in enumerate(grammar_line_list):
    idf_in_line = [bool(re.search(r"\b"+idf+r"\b", line)) for idf in identifier_list]
    if any(idf_in_line):
        idf_matched = []
        for idf, matched in zip(identifier_list, idf_in_line):
            if matched:
                idf_matched.append(idf)
        old_line = "# " + line
        for idf in idf_matched:
            line = re.sub(r"\b"+idf+r"\b", "IDENTIFIER", line)
        
        new_grammar_line_list.append(old_line)
        new_grammar_line_list.append(line)
    else:
        new_grammar_line_list.append(line)
        
            
with open("./new_grammar_edit_identifier.py", "w+")  as f:
    f.writelines(new_grammar_line_list)