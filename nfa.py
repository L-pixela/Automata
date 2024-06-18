from finiteAutomaton import FiniteAutomata

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