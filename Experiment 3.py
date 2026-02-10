# Simple NFA to DFA conversion (subset construction)

from collections import defaultdict

# NFA definition
nfa = {
    'A': {'0': ['A', 'B'], '1': ['A']},
    'B': {'1': ['C']},
    'C': {}
}

start_state = {'A'}
alphabet = ['0', '1']

dfa = {}
unmarked = [start_state]

while unmarked:
    state = unmarked.pop()
    state_name = tuple(sorted(state))
    dfa[state_name] = {}

    for symbol in alphabet:
        next_state = set()
        for s in state:
            if symbol in nfa[s]:
                next_state.update(nfa[s][symbol])

        next_name = tuple(sorted(next_state))
        dfa[state_name][symbol] = next_name

        if next_name not in dfa and next_state not in unmarked:
            unmarked.append(next_state)

# Print DFA
print("DFA Transitions:")
for state in dfa:
    for symbol in dfa[state]:
        print(f"{state} --{symbol}--> {dfa[state][symbol]}")
