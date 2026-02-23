def run_semantic():
    import re

    print("\n--- PHASE 3: SEMANTIC ANALYSIS ---\n")

    symbol_table = set()

    print("Enter statements one by one.")
    print("Type 'exit' to stop.\n")

    lines = []
    while True:
        line = input(">> ").strip()
        if line.lower() == "exit":
            break
        if line:
            lines.append(line)

    for line in lines:
        line = line.strip()

        if line.startswith("int"):
            var = line.split()[1]
            symbol_table.add(var)
            print("Declared:", var)

        elif "=" in line:
            lhs, rhs = line.split("=")
            lhs = lhs.strip()

            if lhs not in symbol_table:
                print("ERROR:", lhs, "not declared")
            else:
                print("OK:", line)

    print("Symbol Table:", symbol_table)


if __name__ == "__main__":
    run_semantic()
