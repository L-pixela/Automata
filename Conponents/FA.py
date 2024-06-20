class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}
        self.is_final = False

    def add_transition(self, symbol, state):
        self.transitions[symbol] = state

class FiniteAutomata:
    def __init__(self):
        self.states = {}
        self.start_state = None

    def add_state(self, state):
        self.states[state.name] = state

    def set_start_state(self, state_name):
        if state_name in self.states:
            self.start_state = self.states[state_name]
        else:
            raise ValueError("Start state not found.")

    def simulate(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol in current_state.transitions:
                current_state = current_state.transitions[symbol]
            else:
                return False
        return current_state.is_final  # Return True only if the final state is accepting

# Example usage
fa = FiniteAutomata()

# Create states
q0 = State('q0')
q1 = State('q1')
q2 = State('q2')
q3 = State('q3')

# Add transitions
q0.add_transition('0', q0)
q0.add_transition('1', q1)
q1.add_transition('0', q2)
q1.add_transition('1', q1)
q2.add_transition('0', q2)
q2.add_transition('1', q3)
q3.add_transition('0', q3)
q3.add_transition('1', q3)
q3.is_final = True

# Add states to the finite automaton
fa.add_state(q0)
fa.add_state(q1)
fa.add_state(q2)
fa.add_state(q3)

# Set the start state
fa.set_start_state('q0')

# Simulate the finite automaton
print(fa.simulate('101001'))  # False
print(fa.simulate('1010'))   # True
