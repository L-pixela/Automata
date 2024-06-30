import os
from FA5 import FiniteAutomata
from NFA import NFA
from DFA import DFA
from time import sleep

def generate_unique_filename(base_name, extension):
    index = 1
    while os.path.exists(f"{base_name}_{index}.{extension}"):
        index += 1
    return f"{base_name}_{index}.{extension}"

def display_menu():
    print('\n===== Menu =====')
    print('1. Visualize Your FA Design')
    print('2. Test if  FA is Deterministic or not')
    print('3. Test if a string is accepted by FA')
    print('4. Construct an equivalent DFA from NFA')
    print('5. Minimize a DFA')
    print('0. Exit')
    print('==================')

if __name__ == "__main__":
    fa = FiniteAutomata()
    fa.get_user_input()

    automaton = None
    fa_type = ""
    fa_short = ""

    while True:
        sleep(2)
        os.system('cls')
        display_menu()
        choice = input("Choose an option: ")

        match choice:

            case '1':
                if automaton:
                    dot = automaton.to_dot()
                    filename = generate_unique_filename('finite_automaton', 'png')
                    dot.render(filename, format='png', view=True)
                    print(f"Rendered FA graph saved as {filename}")
                else:
                    print("Please determine the FA type first (Option 2).")
                sleep(3)

            case '2':
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
                print(f"Your FA type is {fa_type}.")
                sleep(1)

            case '3':
                if automaton:
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
                else:
                    print("Please determine the FA type first (Option 1).")
                sleep(1)

            case '4':
                if automaton and isinstance(automaton, NFA):
                    dfa = automaton.convert_to_dfa()
                    dfa_dot = dfa.to_dot()
                    dfa_filename = generate_unique_filename('dfa_from_nfa', 'png')
                    dfa_dot.render(dfa_filename, format='png', view=True)
                    print(f"Converted DFA graph saved as {dfa_filename}")
                    automaton = dfa
                    fa_type = "Deterministic"
                    fa_short = "DFA"
                else:
                    print("Please provide an NFA for conversion.")
                sleep(1)

            case '5':
                if automaton and isinstance(automaton, DFA):
                    automaton.minimize()
                    minimized_dfa_dot = automaton.to_dot()
                    minimized_dfa_filename = generate_unique_filename('minimized_dfa', 'png')
                    minimized_dfa_dot.render(minimized_dfa_filename, format='png', view=True)
                    print(f"Minimized DFA graph saved as {minimized_dfa_filename}")
                else:
                    print("Please provide a DFA for minimization (Option 1 or 3).")
                sleep(1)

            case '0':
                print("Exiting...")
                sleep(2)
                os.system('cls')
                break

            case _:
                print("Invalid option. Please choose a valid option from the menu.")