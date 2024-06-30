from FA5 import FiniteAutomata
from DFA import DFA

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
    
    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            if '' in self.transitions[state]:  # epsilon transitions
                for next_state in self.transitions[state]['']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)

        return closure
    
    def convert_to_dfa(self):
        dfa = DFA()
        dfa.alphabet = self.alphabet

        initial_closure = self.epsilon_closure({self.initial_state})
        dfa.initial_state = frozenset(initial_closure)
        dfa.states.add(dfa.initial_state)

        unmarked_states = [dfa.initial_state]
        dfa.transitions[dfa.initial_state] = {}

        while unmarked_states:
            current_dfa_state = unmarked_states.pop()
            for symbol in self.alphabet:
                next_nfa_states = set()
                for nfa_state in current_dfa_state:
                    next_nfa_states.update(self.transitions[nfa_state].get(symbol, set()))

                closure = self.epsilon_closure(next_nfa_states)
                next_dfa_state = frozenset(closure)

                if next_dfa_state not in dfa.states:
                    dfa.states.add(next_dfa_state)
                    unmarked_states.append(next_dfa_state)
                    dfa.transitions[next_dfa_state] = {}

                dfa.transitions[current_dfa_state][symbol] = next_dfa_state

        for dfa_state in dfa.states:
            if any(nfa_state in self.final_states for nfa_state in dfa_state):
                dfa.final_states.add(dfa_state)

        return dfa