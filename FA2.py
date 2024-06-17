class DFA:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  # Dictionary mapping (state, symbol) to next state
        self.initial_state = initial_state
        self.final_states = set(final_states)  # Convert final states to a set for faster lookup

    def simulate(self, string):
        current_state = self.initial_state
        for symbol in string:
            if symbol not in self.alphabet:
                return "Invalid Alphabet: Symbol '{}' not found in alphabet.".format(symbol)
            next_state = self.transitions.get((current_state, symbol))
            if next_state is None:
                return False  # No transition for current state and symbol
            current_state = next_state
        return current_state in self.final_states

# Example usage
states = ["q0", "q1", "q2"]
alphabet = {"0", "1"}
transitions = {
    ("q0", "0"): "q1",
    ("q0", "1"): "q2",
    ("q1", "0"): "q1",
    ("q1", "1"): "q2",
    ("q2", "0"): "q0",
    ("q2", "1"): "q1",
}
initial_state = "q0"
final_states = ["q2"]




dfa = DFA(states, alphabet, transitions, initial_state, final_states)

string = "101x"  # Invalid symbol 'x'
result = dfa.simulate(string)

if isinstance(result, str):  # Check for invalid alphabet message
    print(result)
else:
    if result:
        print(f"String '{string}' is accepted by the DFA.")
    else:
        print(f"String '{string}' is rejected by the DFA.")