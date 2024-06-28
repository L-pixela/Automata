from finiteAutomaton import FiniteAutomata
from graphviz import Digraph


class DFA(FiniteAutomata):
    def __init__(self, states=None, alphabet=None, transitions=None, initial_state=None, final_states=None):
        super().__init__()
        if states is not None:
            self.states = states
        if alphabet is not None:
            self.alphabet = alphabet
        if transitions is not None:
            self.transitions = transitions
        if initial_state is not None:
            self.initial_state = initial_state
        if final_states is not None:
            self.final_states = final_states

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
    
    def draw_transition(self, filename = "fa2.gv"):
        dot = Digraph()

        for state in self.states:
            if state in self.final_states:
                dot.node(state, state, shape='doublecircle')
            else:
                dot.node(state, state)

        dot.node('', '', shape='point')
        dot.edge('', self.initial_state)

        for state, transitions in self.transitions.items():
            for symbol, next_state in transitions.items():
                dot.edge(state, next_state, label=symbol)

        dot.render(filename, format='png', cleanup=True)

