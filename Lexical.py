import re

# Step 1: Define token categories
KEYWORDS = {"int", "float", "if", "else", "while", "return"}
OPERATORS = {"+", "-", "*", "/", "=", ">", "<"}
DELIMITERS = {";", ",", "(", ")", "{", "}"}

print("Enter the source code (end input with an empty line):")

# Step 2: Take multi-line input from user
lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line)

code = "\n".join(lines)

print("\nLEXICAL ANALYSIS OUTPUT:\n")

# Step 3: Split code into tokens using regex
tokens = re.findall(r"[A-Za-z_]\w*|\d+|\S", code)

# Step 4: Classify each token
for token in tokens:
    if token in KEYWORDS:
        print(f"{token:<10} → KEYWORD")
    elif token in OPERATORS:
        print(f"{token:<10} → OPERATOR")
    elif token in DELIMITERS:
        print(f"{token:<10} → DELIMITER")
    elif token.isdigit():
        print(f"{token:<10} → NUMBER")
    else:
        print(f"{token:<10} → IDENTIFIER")
