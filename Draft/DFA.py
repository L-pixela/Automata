from FA5 import FiniteAutomata

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
