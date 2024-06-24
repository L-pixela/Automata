class DFA:
  def __init__(self):
    self.states = set()
    self.alphabet = set()
    self.transitions = {}
    self.initial_state = None
    self.final_states = set()

  def get_user_input(self):
    # Get states
    while True:
      try:
        num_states = int(input("Enter the number of states: "))
        if num_states <= 0:
          raise ValueError("Number of states must be positive")
        break
      except ValueError:
        print("Invalid input. Please enter a positive integer.")

    for i in range(num_states):
      state = input(f"Enter state {i+1}: ")
      self.states.add(state)

    # Get alphabet
    while True:
      alphabet_input = input("Enter the alphabet symbols (separated by spaces): ").split()
      if not alphabet_input:
        print("Invalid input. Please enter at least one alphabet symbol.")
      else:
        self.alphabet.update(alphabet_input)
        break

    # Get transitions
    for state in self.states:
      self.transitions[state] = {}
      for symbol in self.alphabet:
        while True:
          next_state = input(f"Enter next state for state '{state}' and symbol '{symbol}': ")
          if next_state not in self.states:
            print(f"Invalid state '{next_state}'. Please enter a valid state from {self.states}.")
          else:
            self.transitions[state][symbol] = next_state
            break

    # Get initial state
    while True:
      initial_state = input("Enter the initial state: ")
      if initial_state not in self.states:
        print(f"Invalid initial state '{initial_state}'. Please enter a valid state from {self.states}.")
      else:
        self.initial_state = initial_state
        break

    # Get final states
    while True:
      final_state_input = input("Enter final states (separated by spaces): ").split()
      if not final_state_input:
        print("Invalid input. Please enter at least one final state.")
      else:
        for state in final_state_input:
          if state not in self.states:
            print(f"Invalid final state '{state}'. Please enter valid states from {self.states}.")
          else:
            self.final_states.add(state)
        break

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
dfa = DFA()

dfa.get_user_input()

string = input("Enter a string to simulate: ")
result = dfa.simulate(string)

if isinstance(result, str):
  print(result)
else:
  if result:
    print(f"String '{string}' is accepted by the DFA.")
  else:
    print(f"String '{string}' is rejected by the DFA.")
