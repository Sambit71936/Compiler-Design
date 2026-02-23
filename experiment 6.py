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


def first_of_sequence(seq, first_sets, grammar):
    result = set()
    if not seq:
        result.add("ε")
        return result
    for sym in seq:
        if sym in grammar:
            result.update(x for x in first_sets[sym] if x != "ε")
            if "ε" in first_sets[sym]:
                continue
            return result
        else:
            result.add(sym)
            return result
    result.add("ε")
    return result


def build_parse_table(grammar, first_sets, follow_sets):
    table = {}
    conflicts = []
    for nt in grammar:
        table[nt] = {}
    for nt, prods in grammar.items():
        for prod in prods:
            first_alpha = first_of_sequence(prod, first_sets, grammar)
            for terminal in sorted(x for x in first_alpha if x != "ε"):
                if terminal in table[nt]:
                    conflicts.append((nt, terminal, table[nt][terminal], prod))
                table[nt][terminal] = prod
            if "ε" in first_alpha:
                for terminal in sorted(follow_sets[nt]):
                    if terminal in table[nt]:
                        conflicts.append((nt, terminal, table[nt][terminal], prod))
                    table[nt][terminal] = prod
    return table, conflicts


def format_table(table):
    lines = []
    for nt in table:
        for term in table[nt]:
            prod = table[nt][term]
            rhs = "ε" if not prod else " ".join(prod)
            lines.append(f"M[{nt}, {term}] = {nt} -> {rhs}")
    return lines


def parse_input(table, start_symbol, grammar, tokens):
    stack = ["$", start_symbol]
    input_tokens = tokens + ["$"]
    index = 0

    print("\nStack Trace:")
    while True:
        stack_str = " ".join(stack)
        remaining = " ".join(input_tokens[index:])
        top = stack[-1]
        current = input_tokens[index]

        if top == current == "$":
            print(f"{stack_str:30} | {remaining:30} | ACCEPT")
            return True
        if top not in grammar:
            if top == current:
                print(f"{stack_str:30} | {remaining:30} | match {current}")
                stack.pop()
                index += 1
            else:
                print(f"{stack_str:30} | {remaining:30} | ERROR: expected {top}")
                return False
        else:
            if current in table[top]:
                prod = table[top][current]
                rhs = "ε" if not prod else " ".join(prod)
                print(f"{stack_str:30} | {remaining:30} | {top} -> {rhs}")
                stack.pop()
                for sym in reversed(prod):
                    if sym != "ε":
                        stack.append(sym)
            else:
                print(f"{stack_str:30} | {remaining:30} | ERROR: no rule for {top} with {current}")
                return False


def run_predictive_parser():
    print("\n--- LL(1) PREDICTIVE PARSER ---\n")
    print("Enter productions (one per line). Example:")
    print("E -> T E'")
    print("E' -> + T E' | ε")
    print("Type 'exit' to stop grammar input.\n")

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

    first_sets = compute_first_sets(grammar)
    follow_sets = compute_follow_sets(grammar, start_symbol, first_sets)
    table, conflicts = build_parse_table(grammar, first_sets, follow_sets)

    if conflicts:
        print("\nConflicts found (not LL(1)):")
        for nt, term, old_prod, new_prod in conflicts:
            old_rhs = "ε" if not old_prod else " ".join(old_prod)
            new_rhs = "ε" if not new_prod else " ".join(new_prod)
            print(f"M[{nt}, {term}] conflict: {nt} -> {old_rhs} / {nt} -> {new_rhs}")
    else:
        print("\nParsing table:")
        print("\n".join(format_table(table)))

    print("\nEnter input string tokens separated by spaces (e.g., id + id * id).")
    input_line = input(">> ").strip()
    if not input_line:
        print("No input provided.")
        return
    tokens = input_line.split()
    parse_input(table, start_symbol, grammar, tokens)


if __name__ == "__main__":
    run_predictive_parser()
