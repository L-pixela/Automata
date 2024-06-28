from finiteAutomaton import FiniteAutomata
from nfa import NFA
from dfa import DFA


if __name__ == "__main__":
    fa = FiniteAutomata()
    # fa.get_user_input()

    # fa.states = ('q0', 'q1', 'q2')
    # fa.alphabet = {'0', '1','e'}
    # fa.transitions = {
    #     'q0' : {'e': {'q1'}},
    #     'q1' : {'1': {'q2'}},
    # }
    # fa.initial_state = 'q0'
    # fa.final_states = {'q2'}

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

    print(f"Your FA Type is {fa_type}.")

    if fa_type == "Non-Deterministic":
        dfa = automaton.convert_to_dfa()
        print("Converted to DFA.")
        dfa.draw_transition()
    
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
