def parse_grammar(lines):
    grammar = {}
    start_symbol = None
    for raw in lines:
        if "->" not in raw:
            continue
        lhs, rhs = raw.split("->", 1)
        lhs = lhs.strip()
        if start_symbol is None:
            start_symbol = lhs
        parts = [p.strip() for p in rhs.split("|")]
        if lhs not in grammar:
            grammar[lhs] = []
        for part in parts:
            if part == "" or part == "ε" or part.lower() == "epsilon":
                grammar[lhs].append([])
            else:
                grammar[lhs].append(part.split())
    return grammar, start_symbol


def compute_first_sets(grammar):
    first = {nt: set() for nt in grammar}

    changed = True
    while changed:
        changed = False
        for nt, prods in grammar.items():
            for prod in prods:
                if not prod:
                    if "ε" not in first[nt]:
                        first[nt].add("ε")
                        changed = True
                    continue
                all_nullable = True
                for sym in prod:
                    if sym in grammar:
                        before = len(first[nt])
                        first[nt].update(x for x in first[sym] if x != "ε")
                        if len(first[nt]) != before:
                            changed = True
                        if "ε" not in first[sym]:
                            all_nullable = False
                            break
                    else:
                        if sym not in first[nt]:
                            first[nt].add(sym)
                            changed = True
                        all_nullable = False
                        break
                if all_nullable:
                    if "ε" not in first[nt]:
                        first[nt].add("ε")
                        changed = True
    return first


def compute_follow_sets(grammar, start_symbol, first):
    follow = {nt: set() for nt in grammar}
    follow[start_symbol].add("$")

    changed = True
    while changed:
        changed = False
        for nt, prods in grammar.items():
            for prod in prods:
                for i, sym in enumerate(prod):
                    if sym not in grammar:
                        continue
                    trailer = set()
                    nullable_suffix = True
                    for next_sym in prod[i + 1:]:
                        if next_sym in grammar:
                            trailer.update(x for x in first[next_sym] if x != "ε")
                            if "ε" in first[next_sym]:
                                continue
                            nullable_suffix = False
                            break
                        else:
                            trailer.add(next_sym)
                            nullable_suffix = False
                            break
                    before = len(follow[sym])
                    follow[sym].update(trailer)
                    if len(follow[sym]) != before:
                        changed = True
                    if nullable_suffix:
                        before = len(follow[sym])
                        follow[sym].update(follow[nt])
                        if len(follow[sym]) != before:
                            changed = True
    return follow


def format_sets(sets):
    lines = []
    for nt in sets:
        items = ", ".join(sorted(sets[nt]))
        lines.append(f"{nt}: {{ {items} }}")
    return lines


def run_first_follow():
    print("\n--- FIRST and FOLLOW SETS ---\n")
    print("Enter productions (one per line). Example:")
    print("E -> T E'")
    print("E' -> + T E' | ε")
    print("Type 'exit' to stop input.\n")

    lines = []
    while True:
        line = input(">> ").strip()
        if line.lower() == "exit":
            break
        if line:
            lines.append(line)

    grammar, start_symbol = parse_grammar(lines)
    if not grammar:
        print("No grammar entered.")
        return

    first = compute_first_sets(grammar)
    follow = compute_follow_sets(grammar, start_symbol, first)

    print("\nFIRST sets:")
    print("\n".join(format_sets(first)))
    print("\nFOLLOW sets:")
    print("\n".join(format_sets(follow)))


if __name__ == "__main__":
    run_first_follow()
