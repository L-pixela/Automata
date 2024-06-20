from finiteAutomaton import FiniteAutomata
from nfa import NFA
from dfa import DFA


if __name__ == "__main__":
    fa = FiniteAutomata()
    fa.get_user_input()

    if fa.is_deterministic():
        automaton = DFA()
        automaton.__dict__.update(fa.__dict__)
        fa_type = "Deterministic"
        short_fa = "DFA"
    else:
        automaton = NFA()
        automaton.__dict__.update(fa.__dict__)
        fa_type = "Non-Deterministic"
        short_fa = "NFA"

    dot = automaton.to_dot()
    dot.render('finite_automaton', format='png', view=True)

    print(f"Your FA Type is {fa_type}.")
    
    while True:
        
        string = input(f"Enter a string to simulate with the {fa_type} (enter 'exit' to quit): ")
        if string.lower() == 'exit':
            break
        result = automaton.simulate(string)

        if isinstance(result, str):
            print(result)
        else:
            if result:
                print(f"String '{string}' is accepted by the {short_fa}.")
            else:
                print(f"String '{string}' is rejected by the {short_fa}.")
