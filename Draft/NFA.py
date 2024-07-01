from FA5 import FiniteAutomata
from DFA import DFA

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
        return DFA(dfa_states, dfa_alphabet, dfa_transitions, 'q0', dfa_final_states)
    
    # def simulate(self, string):
    #     current_states = {self.initial_state}
    #     for symbol in string:
    #         if symbol not in self.alphabet:
    #             return f"Invalid Alphabet: Symbol '{symbol}' not found in alphabet."
    #         next_states = set()
    #         for state in current_states:
    #             next_states.update(self.transitions[state].get(symbol, set()))
    #         if not next_states:
    #             return False  # No transition for any current state and symbol
    #         current_states = next_states
    #     return any(state in self.final_states for state in current_states)
    
    # def epsilon_closure(self, states):
    #     closure = set(states)
    #     stack = list(states)

    #     while stack:
    #         state = stack.pop()
    #         if '' in self.transitions[state]:  # epsilon transitions
    #             for next_state in self.transitions[state]['']:
    #                 if next_state not in closure:
    #                     closure.add(next_state)
    #                     stack.append(next_state)

    #     return closure
    
    # def convert_to_dfa(self):
    #     dfa = DFA()
    #     dfa.alphabet = self.alphabet

    #     initial_closure = self.epsilon_closure({self.initial_state})
    #     dfa.initial_state = frozenset(initial_closure)
    #     dfa.states.add(dfa.initial_state)

    #     unmarked_states = [dfa.initial_state]
    #     dfa.transitions[dfa.initial_state] = {}

    #     while unmarked_states:
    #         current_dfa_state = unmarked_states.pop()
    #         for symbol in self.alphabet:
    #             next_nfa_states = set()
    #             for nfa_state in current_dfa_state:
    #                 next_nfa_states.update(self.transitions[nfa_state].get(symbol, set()))

    #             closure = self.epsilon_closure(next_nfa_states)
    #             next_dfa_state = frozenset(closure)

    #             if next_dfa_state not in dfa.states:
    #                 dfa.states.add(next_dfa_state)
    #                 unmarked_states.append(next_dfa_state)
    #                 dfa.transitions[next_dfa_state] = {}

    #             dfa.transitions[current_dfa_state][symbol] = next_dfa_state

    #     for dfa_state in dfa.states:
    #         if any(nfa_state in self.final_states for nfa_state in dfa_state):
    #             dfa.final_states.add(dfa_state)

    #     return dfa