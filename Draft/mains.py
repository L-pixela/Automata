from FA5 import FiniteAutomata
from NFA import NFA
from DFA import DFA

if __name__ == "__main__":
    fa = FiniteAutomata()
    fa.get_user_input()

    if fa.is_deterministic():
        automaton = DFA()
        automaton.__dict__.update(fa.__dict__)
        fa_type = "Deterministic"
        fa_short = "DFA"
    else:
        automaton = NFA()
        automaton.__dict__.update(fa.__dict__)
        fa_type = "Non-Deterministic"
        fa_short = "NFA"

    dot = automaton.to_dot()
    dot.render('finite_automaton', format='png', view=True)

    print(f"Your FA type is {fa_type}.")

    while True:
        string = input(f"Enter a string to simulate with the {fa_type} (enter 'exit' to quit): ")
        if string.lower() == 'exit':
            break
        result = automaton.simulate(string)

        if isinstance(result, str):
            print(result)
        else:
            if result:
                print(f"String '{string}' is accepted by the {fa_short}.")
            else:
                print(f"String '{string}' is rejected by the {fa_short}.")
