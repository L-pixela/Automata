from finiteAutomaton import FiniteAutomata
from graphviz import Digraph


class DFA(FiniteAutomata):
    def __init__(self, states=None, alphabet=None, transitions=None, initial_state=None, final_states=None):
        super().__init__()
        if states is not None:
            self.states = states
        if alphabet is not None:
            self.alphabet = alphabet
        if transitions is not None:
            self.transitions = transitions
        if initial_state is not None:
            self.initial_state = initial_state
        if final_states is not None:
            self.final_states = final_states

    
    def simulate(self, string):
        current_states = {self.initial_state}

        for symbol in string:
            if symbol not in self.alphabet:
                return f"Invalid Alphabet: Symbol '{symbol}' not found in the alphabet."

            next_states = set()
            for state in current_states:
                if state in self.transitions and symbol in self.transitions[state]:
                    next_states.update(self.transitions[state][symbol])

            current_states = next_states

        return any(state in self.final_states for state in current_states)
    
    def draw_transition(self, filename = "fa2.gv"):
        dot = Digraph()

        for state in self.states:
            if state in self.final_states:
                dot.node(state, state, shape='doublecircle')
            else:
                dot.node(state, state)

        dot.node('', '', shape='point')
        dot.edge('', self.initial_state)

        for state, transitions in self.transitions.items():
            for symbol, next_state in transitions.items():
                dot.edge(state, next_state, label=symbol)

        dot.render(filename, format='png', cleanup=True)

    def hopcroft_minimization(self):
        print('hi')

        print(self.transitions)
        self.states = set(self.states)
        self.final_states = set(self.final_states)
        print(type(self.states))
        print(type(self.final_states))

        P = {frozenset(self.final_states), frozenset(self.states - self.final_states)}


        # partition
        W = {frozenset(self.final_states)}
        #the final state
        # for ex : q0q1q2
        # p = q0q1, q2/ w= q2 which is final state

        while W:  # if W is not empty
            A = W.pop()  # pop W into A
            for c in self.alphabet:  # for all symbols in the alphabet
                X = {q for q in self.states if self.transitions[q].get(c) in A}
                new_P = set()
                for Y in P:
                    inter = Y & X
                    diff = Y - X
                    if inter and diff:
                        new_P.add(frozenset(inter))
                        new_P.add(frozenset(diff))
                        if Y in W:
                            W.remove(Y)
                            W.add(frozenset(inter))
                            W.add(frozenset(diff))
                        else:
                            if len(inter) <= len(diff):
                                W.add(frozenset(inter))
                            else:
                                W.add(frozenset(diff))
                    else:
                        new_P.add(Y)
                P = new_P

        new_states = {s: 'q' + str(i) for i, s in enumerate(P)}
        initial_state = new_states[frozenset({self.initial_state})]
        final_states = {new_states[s] for s in P if s & self.final_states}
        new_transitions = {}

        for subset in P:
            current_state = new_states[subset]
            new_transitions[current_state] = {}
            for q in subset:
                for symbol, target_set in self.transitions[q].items():
                    target_state = next(iter(target_set))  # Get the single target state from the set
                    new_transitions[current_state][symbol] = new_states[frozenset({target_state})]

        return DFA(new_states.values(), self.alphabet, new_transitions, initial_state, final_states)

    # self class needs to be defined, possibly from previous code
    # self should be an instance of this self class
