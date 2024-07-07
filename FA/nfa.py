from finiteAutomaton import FiniteAutomata
from dfa import DFA
from dfa import DFA
import graphviz

class NFA(FiniteAutomata):

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if state in self.transitions and 'e' in self.transitions[state]:
                for epsilon_state in self.transitions[state]['e']:
                    if epsilon_state not in closure:
                        closure.add(epsilon_state)
                        stack.append(epsilon_state)
        return frozenset(closure)

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            if state in self.transitions and 'e' in self.transitions[state]:
                for epsilon_state in self.transitions[state]['e']:
                    if epsilon_state not in closure:
                        closure.add(epsilon_state)
                        stack.append(epsilon_state)
        return frozenset(closure)

        
    def simulate(self, string):
        current_states = self.epsilon_closure({self.initial_state})
        for symbol in string:
            if symbol not in self.alphabet:
                return f"Invalid Alphabet: Symbol '{symbol}' not found in alphabet."
            next_states = set()
            for state in current_states:
                next_states.update(self.transitions[state].get(symbol, set()))
            epsilon_closure_next = set()
            for state in next_states:
                epsilon_closure_next.update(self.epsilon_closure({state}))
            current_states = epsilon_closure_next
            epsilon_closure_next = set()
            for state in next_states:
                epsilon_closure_next.update(self.epsilon_closure({state}))

            current_states = epsilon_closure_next
        return any(state in self.final_states for state in current_states)

    def convert_to_dfa(self):
        dfa_states = set()
        dfa_transitions = {}
        dfa_initial_state = frozenset(self.epsilon_closure({self.initial_state}))
        dfa_final_states = set()
        unprocessed_states = [dfa_initial_state]
        state_mapping = {dfa_initial_state: 'q0'}
        next_state_index = 1

        while unprocessed_states:
            current_states = unprocessed_states.pop(0)
            dfa_state_name = state_mapping[current_states]
            dfa_states.add(dfa_state_name)

            if any(state in self.final_states for state in current_states):
                dfa_final_states.add(dfa_state_name)

            for symbol in self.alphabet:
                if symbol == 'e':
                    continue
                next_states = set()
                for state in current_states:
                    if state in self.transitions and symbol in self.transitions[state]:
                        next_states.update(self.transitions[state][symbol])

                epsilon_closure_next = frozenset(self.epsilon_closure(next_states))
                if epsilon_closure_next not in state_mapping:
                    state_mapping[epsilon_closure_next] = f'q{next_state_index}'
                    unprocessed_states.append(epsilon_closure_next)
                    next_state_index += 1

                current_dfa_state = state_mapping[current_states]
                next_dfa_state = state_mapping[epsilon_closure_next]
                if current_dfa_state not in dfa_transitions:
                    dfa_transitions[current_dfa_state] = {}
                dfa_transitions[current_dfa_state][symbol] = next_dfa_state

        dfa_alphabet = {symbol for symbol in self.alphabet if symbol != 'e'}
        return DFA(states=dfa_states, alphabet=dfa_alphabet, transitions=dfa_transitions, initial_state='q0', final_states=dfa_final_states)


    def convert_to_dfa(self):
        # Initialize the DFA states and transitions
        dfa_states = set()
        dfa_transitions = {}

        # Compute the epsilon-closure of the initial state of the NFA
        dfa_initial_state = frozenset(self.epsilon_closure({self.initial_state}))
        print(f"Initial State (epsilon-closure of {self.initial_state}): {dfa_initial_state}")

        # Initialize the DFA final states
        dfa_final_states = set()

        # Initialize the list of unprocessed states with the initial state
        unprocessed_states = [dfa_initial_state]
        print(f"Initial Unprocessed States: {unprocessed_states}")

        # Map the epsilon-closure of the initial state to the first DFA state ('q0')
        state_mapping = {dfa_initial_state: 'q0'}
        print(f"Initial State Mapping: {state_mapping}")

        # Counter for naming new DFA states
        next_state_index = 1

        while unprocessed_states:
            # Process the next unprocessed state
            current_states = unprocessed_states.pop(0)
            dfa_state_name = state_mapping[current_states]
            print(f"\nProcessing DFA state: {dfa_state_name}, which corresponds to NFA states: {current_states}")

            # Add the current DFA state to the set of DFA states
            dfa_states.add(dfa_state_name)
            print(f"DFA States Updated: {dfa_states}")

            # Check if any NFA state in the current DFA state set is a final state
            if any(state in self.final_states for state in current_states):
                dfa_final_states.add(dfa_state_name)
                print(f"Added {dfa_state_name} to DFA Final States: {dfa_final_states}")

            # Process each symbol in the alphabet
            for symbol in self.alphabet:
                if symbol == 'e':
                    continue  # Skip epsilon transitions in DFA

                print(" for all symbols Find all next states from the current states on the given symbol")
                next_states = set()
                for state in current_states:
                    if state in self.transitions and symbol in self.transitions[state]:
                        next_states.update(self.transitions[state][symbol])
                print(f"Next states from {current_states} on symbol '{symbol}': {next_states}")

                # Compute the epsilon-closure of the next states
                epsilon_closure_next = frozenset(self.epsilon_closure(next_states))
                print(f"Epsilon-closure of {next_states}: {epsilon_closure_next}")

                # If the epsilon-closure is a new state, add it to the mapping and unprocessed states
                if epsilon_closure_next not in state_mapping:
                    state_mapping[epsilon_closure_next] = f'q{next_state_index}'
                    unprocessed_states.append(epsilon_closure_next)
                    print(f"Discovered new DFA state {state_mapping[epsilon_closure_next]} corresponding to NFA states: {epsilon_closure_next}")
                    next_state_index += 1

                # Add the transition to the DFA
                current_dfa_state = state_mapping[current_states]
                next_dfa_state = state_mapping[epsilon_closure_next]
                if current_dfa_state not in dfa_transitions:
                    dfa_transitions[current_dfa_state] = {}
                dfa_transitions[current_dfa_state][symbol] = next_dfa_state
                print(f"Added transition: {current_dfa_state} --{symbol}--> {next_dfa_state}")

        # Remove epsilon from the alphabet for DFA
        dfa_alphabet = {symbol for symbol in self.alphabet if symbol != 'e'}
        print(f"\nDFA Alphabet: {dfa_alphabet}")
        print(f"DFA States: {dfa_states}")
        print(f"DFA Final States: {dfa_final_states}")
        print(f"DFA Transitions: {dfa_transitions}")

        # Return the constructed DFA
        return DFA(dfa_states, dfa_alphabet, dfa_transitions, 'q0' , dfa_final_states)

    
    # def draw_transition(self, filename):
    #     from graphviz import Digraph
    #     dot = Digraph()

    #     for state in self.states:
    #         if state in self.final_states:
    #             dot.node(state, state, shape='doublecircle')
    #         else:
    #             dot.node(state, state)
    #     dot.node('', '', shape='point')
    #     dot.edge('', self.initial_state)

    #     for state, transitions in self.transitions.items():
    #         for symbol, next_states in transitions.items():
    #             for next_state in next_states:
    #                 dot.edge(state, next_state, label=symbol)

    #     dot.render(filename, format='png', cleanup=True)