from graphviz import Digraph

class FiniteAutomata:
    # initializing the states,alphabet, transitions, initial_state, and final_states
    def __init__(self, states=None, alphabet=None, transitions=None, initial_state=None, final_states=None):
        self.states = states or set()
        self.alphabet = alphabet or set()
        self.transitions = transitions or {}
        self.initial_state = initial_state
        self.final_states = final_states or set()
    # Initializing the functions of getting the user input
    def get_user_input(self):
        self._get_states()
        self._get_alphabet()
        self._get_transitions()
        self._get_initial_state()
        self._get_final_states()
    # getting states input function
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
    # getting alphabet input function
    def _get_alphabet(self):
        while True:
            alphabet_input = input("Enter the alphabet symbols (separated by spaces): ").split()
            if not alphabet_input:
                print("Invalid input. Please enter at least one alphabet symbol.")
            else:
                self.alphabet.update(alphabet_input)
                break
    # getting initial states input function 
    def _get_initial_state(self):
        while True:
            initial_state = input("Enter the initial state: ")
            if initial_state not in self.states:
                print(f"Invalid initial state '{initial_state}'. Please enter a valid state from {self.states}.")
            else:
                self.initial_state = initial_state
                break
    # getting final states input function
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
    # getting transitions input function
    def _get_transitions(self):
        for state in self.states:
            self.transitions[state] = {}
            for symbol in self.alphabet:
                while True:
                    display_symbol = 'epsilon' if symbol == 'e' else symbol
                    next_states = input(f"Enter next states for state '{state}' and symbol '{display_symbol}' (separated by spaces): ").split()
                    if 'e' in next_states:
                        next_states.remove('e')
                        next_states.add('')
                    valid = all(next_state in self.states for next_state in next_states)
                    if not valid:
                        print(f"Invalid states in {next_states}. Please enter valid states from {self.states}.")
                    else:
                        self.transitions[state][symbol] = set(next_states)
                        break
    # Testing if the FA is deterministic or not function
    def is_deterministic(self):
        if 'e' in self.alphabet:
            return False
        for state in self.transitions:
            for symbol in self.transitions[state]:
                if len(self.transitions[state][symbol]) > 1:
                    return False
        return True
    # Testing the string of the FA if it is deterministic, it will simulate as dfa else nfa
    def simulate(self, string):
        raise NotImplementedError("This method should be implemented by subclasses")
    # for converting state to string when we want to draw the graphviz
    def _state_to_string(self, state):
        if isinstance(state, frozenset):
            return ",".join(sorted(state))
        return state
    # function for drawing the FA and visualizing it 
    def to_dot(self):
        dot = Digraph()
        dot.attr(rankdir='LR', size='8,5')
        dot.node('fake', shape='point')
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state, shape='circle')
        dot.edge('fake', self._state_to_string(self.initial_state))
        for state in self.transitions:
            state_str = self._state_to_string(state)
            for symbol in self.transitions[state]:
                for next_state in self.transitions[state][symbol]:
                    dot.edge(state_str, self._state_to_string(next_state), label=symbol)
        return dot
    # function for drawing the FA when FA is converted or minimized
    def draw_transition(self):
                dot = Digraph()

                # Add nodes for all states
                for state in self.states:
                    if state == self.initial_state:
                        dot.node(state, state, shape='doublecircle' if state in self.final_states else 'circle')
                    else:
                        dot.node(state, state, shape='doublecircle' if state in self.final_states else 'circle')

                # Add a point node for initial transition
                dot.node('', '', shape='point')
                dot.edge('', self.initial_state)

                # Add edges for transitions
                for state, transitions in self.transitions.items():
                    for symbol, next_state in transitions.items():
                        dot.edge(state, next_state, label=str(symbol))

                return dot