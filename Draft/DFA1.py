from FA import FiniteAutomata
from graphviz import Digraph

class DFA(FiniteAutomata):

    def __init__(self, states=None, alphabet=None, transitions=None, initial_state=None, final_states=None):
        super().__init__(states, alphabet, transitions, initial_state, final_states)

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

    def minimize(self):
        def get_state_key(state_set):
            return frozenset(state_set)

        final_states = {state for state in self.states if state in self.final_states}
        non_final_states = {state for state in self.states if state not in self.final_states}
        partitions = [final_states, non_final_states]

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
                next_state = next(iter(self.transitions[state].get(symbol, {None})), None)
                if next_state is not None:
                    new_transitions[state][symbol] = state_mapping[next_state]

        self.states = new_states
        self.final_states = new_final_states
        self.initial_state = new_initial_state
        self.transitions = new_transitions


    # def minimize(self):
    #     def get_state_key(state_set):
    #         return frozenset(state_set)

    #     final_states = {state for state in self.states if state in self.final_states}
    #     non_final_states = {state for state in self.states if state not in self.final_states}
    #     partitions = [final_states, non_final_states]

    #     while True:
    #         new_partitions = []
    #         for partition in partitions:
    #             split_dict = {}
    #             for state in partition:
    #                 key = tuple(get_state_key(self.transitions[state].get(symbol, None)) for symbol in self.alphabet)
    #                 if key not in split_dict:
    #                     split_dict[key] = set()
    #                 split_dict[key].add(state)
    #             new_partitions.extend(split_dict.values())
    #         if len(new_partitions) == len(partitions):
    #             break
    #         partitions = new_partitions

    #     minimized_states = {get_state_key(partition) for partition in partitions}
    #     minimized_transitions = {}
    #     minimized_initial_state = next(get_state_key(partition) for partition in partitions if self.initial_state in partition)
    #     minimized_final_states = {get_state_key(partition) for partition in partitions if partition & self.final_states}

    #     for partition in partitions:
    #         state_key = get_state_key(partition)
    #         representative_state = next(iter(partition))
    #         minimized_transitions[state_key] = {}
    #         for symbol in self.alphabet:
    #             if representative_state in self.transitions and symbol in self.transitions[representative_state]:
    #                 target_partition = next(p for p in partitions if self.transitions[representative_state][symbol] in p)
    #                 minimized_transitions[state_key][symbol] = get_state_key(target_partition)

    #     return DFA(states=minimized_states, alphabet=self.alphabet, transitions=minimized_transitions,
    #                initial_state=minimized_initial_state, final_states=minimized_final_states)
