import re

class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}
        self.is_final = False

    def add_transition(self, symbol, next_state):
        self.transitions[symbol] = next_state

    def is_accepted(self, input_string):
        current_state = self
        for char in input_string:
            if char not in current_state.transitions:
                return False
            current_state = current_state.transitions[char]
        return current_state.is_final

class FiniteAutomata:
    def __init__(self):
        self.states = {}
        self.start_state = None

    def add_state(self, state):
        self.states[state.name] = state

    def set_start_state(self, state_name):
        self.start_state = self.states[state_name]

    def simulate(self, input_string):
        current_state = self.start_state
        for char in input_string:
            if char not in current_state.transitions:
                return False
            current_state = current_state.transitions[char]
        return current_state.is_final

# # Example usage
fa = FiniteAutomata()

# Create states
q0 = State('q0')
q1 = State('q1')
q2 = State('q2')
q3 = State('q3')

# Add transitions
q0.add_transition('0', q1)
q0.add_transition('1', q0)
q1.add_transition('0', q2)
q1.add_transition('1', q1)
q2.add_transition('0', q3)
q2.add_transition('1', q2)
q3.add_transition('0', q3)
q3.add_transition('1', q3)
q3.is_final = True

# Add states to the finite automata
fa.add_state(q0)
fa.add_state(q1)
fa.add_state(q2)
fa.add_state(q3)

# Set the start state
fa.set_start_state('q0')

# Simulate the finite automata
print(fa.simulate('10101'))  # True
print(fa.simulate('1010'))   # False

# # Example usage
# fa = FiniteAutomata()

# # Create states
# q0 = State('q0')
# q1 = State('q1')
# q2 = State('q2')
# q3 = State('q3')

# # Add transitions
# q0.add_transition('0', q0)
# q0.add_transition('1', q1)
# q1.add_transition('0', q2)
# q1.add_transition('1', q1)
# q2.add_transition('0', q2)
# q2.add_transition('1', q3)
# q3.add_transition('0', q3)
# q3.add_transition('1', q3)
# q3.is_final = True

# # Add states to the finite automata
# fa.add_state(q0)
# fa.add_state(q1)
# fa.add_state(q2)
# fa.add_state(q3)

# # Set the start state
# fa.set_start_state('q0')

# # Simulate the finite automata
# print(fa.simulate('101001'))  # True
# print(fa.simulate('1010'))   # True