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
        current_states = {self.initial_state}

        for symbol in string:
            if symbol not in self.alphabet:
                return f"Invalid Alphabet: Symbol '{symbol}' not found in the alphabet."

            next_states = set()
            for state in current_states:
                if state in self.transitions and symbol in self.transitions[state]:
                    next_states.update(self.transitions[state][symbol])

            current_states = next_states

        return any(state in self.final_states for state in current_states)
    
    def draw_transition(self, filename="fa2.gv"):
            dot = Digraph()

            # Add nodes for all states
            for state in self.states:
                if state == self.initial_state:
                    dot.node(state, state, shape='doublecircle' if state in self.final_states else 'circle', peripheries='2')
                else:
                    dot.node(state, state, shape='doublecircle' if state in self.final_states else 'circle')

            # Add a point node for initial transition
            dot.node('', '', shape='point')
            dot.edge('', self.initial_state)

            # Add edges for transitions
            for state, transitions in self.transitions.items():
                for symbol, next_state in transitions.items():
                    dot.edge(state, next_state, label=str(symbol))

            dot.render(filename, format='png', cleanup=True)

    def minimize(self):
        def get_state_key(state_set):
            return frozenset(state_set)

        # Step 1: Initialize the partitions
        final_states = {state for state in self.states if state in self.final_states}
        non_final_states = {state for state in self.states if state not in self.final_states}
        partitions = [final_states, non_final_states]

        # Step 2: Refine the partitions
        while True:
            new_partitions = []
            for partition in partitions:
                # Split partition based on distinguishability
                split_dict = {}
                for state in partition:
                    key = tuple(get_state_key(self.transitions[state].get(symbol, {None})) for symbol in self.alphabet)
                    if key not in split_dict:
                        split_dict[key] = set()
                    split_dict[key].add(state)
                new_partitions.extend(split_dict.values())
            if len(new_partitions) == len(partitions):
                break
            partitions = new_partitions

        # Step 3: Merge equivalent states
        state_mapping = {}
        new_states = set()
        new_final_states = set()
        new_initial_state = None
        new_transitions = {}

        for partition in partitions:
            representative = next(iter(partition))
            new_states.add(representative)
            if representative in self.final_states:
                new_final_states.add(representative)
            if self.initial_state in partition:
                new_initial_state = representative
            for state in partition:
                state_mapping[state] = representative

        for state in new_states:
            new_transitions[state] = {}
            for symbol in self.alphabet:
                next_state = next(iter(self.transitions[state].get(symbol, {None})))
                if next_state is not None:
                    new_transitions[state][symbol] = state_mapping[next_state]

        self.states = new_states
        self.final_states = new_final_states
        self.initial_state = new_initial_state
        self.transitions = new_transitions

    # def draw_transition(self, filename = "fa2.gv"):
    #     dot = Digraph()

    #     for state in self.states:
    #         if state in self.final_states:
    #             dot.node(state, state, shape='doublecircle')
    #         else:
    #             dot.node(state, state)

    #     dot.node('', '', shape='point')
    #     dot.edge('', self.initial_state)

    #     for state, transitions in self.transitions.items():
    #         for symbol, next_state in transitions.items():
    #             dot.edge(state, next_state, label=symbol)

    #     dot.render(filename, format='png', cleanup=True)