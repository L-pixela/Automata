class FiniteAutomata:
    # initialize the attributes
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.final_states = set()
    # initialize the input element of the user
    def get_user_input(self):
        self._get_states()
        self._get_alphabet()
        self._get_transitions()
        self._get_initial_state()
        self._get_final_states()
    # get number of states that user input 
    def _get_states(self):
        while True:
            try:
                num_states = int(input("Enter the number of states: "))
                if num_states <= 0:
                    raise ValueError("Number of states must be positive")
                break
            except ValueError:
                print("Invalid input. Please enter a positive integer.")

        for i in range(num_states):
            state = input(f"Enter state {i + 1}: ")
            self.states.add(state)
    # Get user input of alphabet
    def _get_alphabet(self):
        while True:
            alphabet_input = input("Enter the alphabet symbols (separated by spaces): ").split()
            if not alphabet_input:
                print("Invalid input. Please enter at least one alphabet symbol.")
            else:
                self.alphabet.update(alphabet_input)
                break
    # Get user input of the initial state
    def _get_initial_state(self):
        while True:
            initial_state = input("Enter the initial state: ")
            if initial_state not in self.states:
                print(f"Invalid initial state '{initial_state}'. Please enter a valid state from {self.states}.")
            else:
                self.initial_state = initial_state
                break
    # Get user input of the final state
    def _get_final_states(self):
        while True:
            final_state_input = input("Enter final states (separated by spaces): ").split()
            if not final_state_input:
                print("Invalid input. Please enter at least one final state.")
            else:
                for state in final_state_input:
                    if state not in self.states:
                        print(f"Invalid final state '{state}'. Please enter valid states from {self.states}.")
                    else:
                        self.final_states.add(state)
                break
    # Get user input of the transitions of the FA
    def _get_transitions(self):
        for state in self.states:
            self.transitions[state] = {}
            for symbol in self.alphabet:
                while True:
                    next_states = input(f"Enter next states for state '{state}' and symbol '{symbol}' (separated by spaces): ").split()
                    valid = all(next_state in self.states for next_state in next_states)
                    if not valid:
                        print(f"Invalid states in {next_states}. Please enter valid states from {self.states}.")
                    else:
                        self.transitions[state][symbol] = set(next_states)
                        break
    # Testing if the FA Designed is Deterministic or Non-Determinsitic
    def is_deterministic(self):
        for state in self.transitions:
            for symbol in self.transitions[state]:
                if len(self.transitions[state][symbol]) > 1:
                    return False
        return True
    # This simulate is raise to notify that the simulate method will be override by their subclasses (DFA or NFA) below
    def simulate(self, string):
        raise NotImplementedError("This method should be implemented by subclasses")

# This class inherit from FiniteAutomata and simulate the result inputted by the user, If the inputted is DFA 
class DFA(FiniteAutomata):
    def simulate(self, string):
        current_state = self.initial_state
        for symbol in string:
            if symbol not in self.alphabet:
                return f"Invalid Alphabet: Symbol '{symbol}' not found in alphabet."
            next_state = next(iter(self.transitions[current_state].get(symbol, set())))
            if next_state is None:
                return False  # No transition for current state and symbol
            current_state = next_state
        return current_state in self.final_states

# This class inherit from FiniteAutomata and simulate the result inputted by the user, If the inputted is NFA
class NFA(FiniteAutomata):
    def simulate(self, string):
        current_states = {self.initial_state}
        for symbol in string:
            if symbol not in self.alphabet:
                return f"Invalid Alphabet: Symbol '{symbol}' not found in alphabet."
            next_states = set()
            for state in current_states:
                next_states.update(self.transitions[state].get(symbol, set()))
            if not next_states:
                return False  # No transition for any current state and symbol
            current_states = next_states
        return any(state in self.final_states for state in current_states)


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
