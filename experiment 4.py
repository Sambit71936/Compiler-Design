def parse_grammar(lines):
    grammar = {}
    for raw in lines:
        if "->" not in raw:
            continue
        lhs, rhs = raw.split("->", 1)
        lhs = lhs.strip()
        parts = [p.strip() for p in rhs.split("|")]
        if lhs not in grammar:
            grammar[lhs] = []
        for part in parts:
            if part == "" or part == "ε" or part.lower() == "epsilon":
                grammar[lhs].append([])
            else:
                grammar[lhs].append(part.split())
    return grammar


def format_grammar(grammar):
    lines = []
    for lhs in grammar:
        alts = []
        for prod in grammar[lhs]:
            if not prod:
                alts.append("ε")
            else:
                alts.append(" ".join(prod))
        lines.append(f"{lhs} -> " + " | ".join(alts))
    return lines


def eliminate_direct_left_recursion(grammar):
    new_grammar = {}
    for lhs, prods in grammar.items():
        alpha = []
        beta = []
        for prod in prods:
            if prod and prod[0] == lhs:
                alpha.append(prod[1:])
            else:
                beta.append(prod)
        if not alpha:
            new_grammar[lhs] = prods
            continue
        lhs_prime = lhs + "'"
        while lhs_prime in grammar or lhs_prime in new_grammar:
            lhs_prime += "'"
        new_grammar[lhs] = []
        for b in beta:
            new_grammar[lhs].append(b + [lhs_prime])
        new_grammar[lhs_prime] = []
        for a in alpha:
            new_grammar[lhs_prime].append(a + [lhs_prime])
        new_grammar[lhs_prime].append([])
    return new_grammar


def left_factor(grammar):
    changed = True
    new_grammar = {k: [p[:] for p in v] for k, v in grammar.items()}
    while changed:
        changed = False
        for lhs in list(new_grammar.keys()):
            prods = new_grammar[lhs]
            if len(prods) < 2:
                continue
            prefix_map = {}
            for prod in prods:
                key = prod[0] if prod else "ε"
                prefix_map.setdefault(key, []).append(prod)
            factored = False
            for key, group in prefix_map.items():
                if key == "ε" or len(group) < 2:
                    continue
                factored = True
                changed = True
                lhs_prime = lhs + "_F"
                while lhs_prime in new_grammar:
                    lhs_prime += "_F"
                new_prods = []
                for prod in prods:
                    if prod in group:
                        continue
                    new_prods.append(prod)
                new_prods.append([key, lhs_prime])
                new_grammar[lhs] = new_prods
                new_grammar[lhs_prime] = []
                for prod in group:
                    suffix = prod[1:]
                    new_grammar[lhs_prime].append(suffix)
                break
            if factored:
                break
    return new_grammar


def run_transformations():
    print("\n--- GRAMMAR TRANSFORMATIONS ---\n")
    print("Enter productions (one per line). Example:")
    print("E -> E + T | T")
    print("Type 'exit' to stop input.\n")

    lines = []
    while True:
        line = input(">> ").strip()
        if line.lower() == "exit":
            break
        if line:
            lines.append(line)

    grammar = parse_grammar(lines)

    while True:
        print("\nChoose an option:")
        print("1. Eliminate direct left recursion")
        print("2. Left factoring")
        print("3. Both (recursion then factoring)")
        print("4. Show current grammar")
        print("5. Exit")
        choice = input(">> ").strip()

        if choice == "1":
            grammar = eliminate_direct_left_recursion(grammar)
            print("\nAfter Left Recursion Elimination:")
            print("\n".join(format_grammar(grammar)))
        elif choice == "2":
            grammar = left_factor(grammar)
            print("\nAfter Left Factoring:")
            print("\n".join(format_grammar(grammar)))
        elif choice == "3":
            grammar = eliminate_direct_left_recursion(grammar)
            grammar = left_factor(grammar)
            print("\nAfter Both Transformations:")
            print("\n".join(format_grammar(grammar)))
        elif choice == "4":
            print("\nCurrent Grammar:")
            print("\n".join(format_grammar(grammar)))
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    run_transformations()
