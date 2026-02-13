import re

def syntax_analyzer(statement):
    # remove extra spaces
    statement = statement.strip()

    # grammar: id = id op id | id = id op number | id = number
    pattern = r'^[a-zA-Z_]\w*\s*=\s*([a-zA-Z_]\w*|\d+)(\s*[+\-*/]\s*([a-zA-Z_]\w*|\d+))?$'

    if re.match(pattern, statement):
        print(f"VALID SYNTAX   : {statement}")
    else:
        print(f"INVALID SYNTAX : {statement}")

# Read input file
with open("input.txt", "r") as file:
    lines = file.readlines()

print("SYNTAX ANALYSIS RESULT:\n")

for line in lines:
    if line.strip():  # ignore empty lines
        syntax_analyzer(line)
