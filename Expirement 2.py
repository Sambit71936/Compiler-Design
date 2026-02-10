# Simple Regex to NFA (Thompson's Construction)

class State:
    def __init__(self):
        self.t = {}      # symbol transitions
        self.e = []      # epsilon transitions


class NFA:
    def __init__(self, s, f):
        self.start = s
        self.final = f


def symbol_nfa(ch):
    s, f = State(), State()
    s.t[ch] = [f]
    return NFA(s, f)


def concat(nfa1, nfa2):
    nfa1.final.e.append(nfa2.start)
    return NFA(nfa1.start, nfa2.final)


def union(nfa1, nfa2):
    s, f = State(), State()
    s.e = [nfa1.start, nfa2.start]
    nfa1.final.e.append(f)
    nfa2.final.e.append(f)
    return NFA(s, f)


def star(nfa):
    s, f = State(), State()
    s.e = [nfa.start, f]
    nfa.final.e = [nfa.start, f]
    return NFA(s, f)


# -------- Example --------
# Regex: a*
nfa = star(symbol_nfa('a'))

print("Start state:", id(nfa.start))
print("Final state:", id(nfa.final))
