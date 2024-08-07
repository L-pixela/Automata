from finiteAutomaton import FiniteAutomata
from graphviz import Digraph

class DFA(FiniteAutomata):
    # initialize the element of FA
    def __init__(self, states=None, alphabet=None, transitions=None, initial_state=None, final_states=None):
        super().__init__(states, alphabet, transitions, initial_state, final_states)
    # simulate the string of the FA if it's accept or not
    def simulate(self, string):
        current_state = self.initial_state
        for symbol in string:
            if symbol not in self.alphabet:
                return f"Invalid Alphabet: Symbol '{symbol}' not found in alphabet."
            next_state = next(iter(self.transitions[current_state].get(symbol, set())), None)
            if next_state is None:
                return False
            current_state = next_state
        return current_state in self.final_states
    # minimizing DFA function
    def minimize(self):
        def get_state_key(state_set):
            return frozenset(state_set)
        # Doing partitioning for the final state and non-final state
        final_states = {state for state in self.states if state in self.final_states}
        non_final_states = {state for state in self.states if state not in self.final_states}
        partitions = [final_states, non_final_states]
        # Doing iteration to get all of the new state 
        while True:
            new_partitions = []
            for partition in partitions:
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
        # start mapping to get the transition of the new states
        state_mapping = {}
        new_states = set()
        new_final_states = set()
        new_initial_state = None
        new_transitions = {}
        # Doing the iteration for the Partitioning to confirm the new state as respresentative
        for partition in partitions:
            representative = next(iter(partition))
            new_states.add(representative)
            if representative in self.final_states:
                new_final_states.add(representative)
            if self.initial_state in partition:
                new_initial_state = representative
            for state in partition:
                state_mapping[state] = representative
        # after the partitioning to find resperesentative state (new state), start to do iteration to find the transition for the new state
        for state in new_states:
            new_transitions[state] = {}
            for symbol in self.alphabet:
                next_state = next(iter(self.transitions[state].get(symbol, {None})), None)
                if next_state is not None:
                    new_transitions[state][symbol] = state_mapping[next_state]
        # after getting all of the element, update the new element to the DFA
        self.states = new_states
        self.final_states = new_final_states
        self.initial_state = new_initial_state
        self.transitions = new_transitions
