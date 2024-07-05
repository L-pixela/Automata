import customtkinter as ctk
from tkinter import simpledialog, Toplevel, Label, Button
from PIL import Image, ImageTk
import os
import datetime
from FA import FiniteAutomata
from NFA1 import NFA
from DFA1 import DFA

def create_fa(self):
        try:
            num_states = int(self.num_states_entry.get())
            states = [f"q{i}" for i in range(num_states)]

            alphabet = set(self.alphabet_entry.get().split())
            initial_state = self.initial_state_entry.get()

            final_states = set(self.final_states_entry.get().split())

            transitions = {}
            for state in states:
                transitions[state] = {}
                for symbol in alphabet:
                    transitions[state][symbol] = set()

            transitions_input = self.transitions_text.get("1.0", "end").strip().split("\n")
            for transition in transitions_input:
                try:
                    state, symbol, next_states = transition.split()
                    next_states = next_states.split(',')
                except ValueError:
                    self.show_custom_message("Error", f"Invalid transition format: '{transition}'")
                    return

                if state not in states:
                    self.show_custom_message("Error", f"Invalid state: '{state}'")
                    return
                if symbol not in alphabet and symbol != 'e':
                    self.show_custom_message("Error", f"Invalid symbol: '{symbol}'")
                    return
                if any(next_state not in states for next_state in next_states):
                    self.show_custom_message("Error", f"Invalid next state(s): '{','.join(next_states)}'")
                    return

                if symbol not in transitions[state]:
                    transitions[state][symbol] = set()
                transitions[state][symbol].update(next_states)

            self.fa = FiniteAutomata(states=set(states), alphabet=alphabet, transitions=transitions, initial_state=initial_state, final_states=final_states)

            self.show_custom_message("Success", "Finite Automaton created successfully.")
            self.visualize_fa()

        except Exception as e:
            self.show_custom_message("Error", f"Failed to create Finite Automaton: {str(e)}")

def check_determinism(self):
        try:
            if self.fa:
                is_deterministic = self.fa.is_deterministic()
                self.fa_type = "DFA" if is_deterministic else "NFA"
                result_text = f"The FA is {self.fa_type}."
                self.show_custom_message("Determinism Check", result_text)
            else:
                self.show_custom_message("Error", "Create FA first.")
        except Exception as e:
            self.show_custom_message("Error", f"Failed to check determinism: {str(e)}")

def check_string_acceptance(self):
        try:
            if self.fa:
                input_string = simpledialog.askstring("Input", "Enter a string:")
                if input_string is not None:
                    if self.fa_type == "DFA":
                        automaton = DFA(states=self.fa.states, alphabet=self.fa.alphabet, transitions=self.fa.transitions, initial_state=self.fa.initial_state, final_states=self.fa.final_states)
                    else:
                        automaton = NFA(states=self.fa.states, alphabet=self.fa.alphabet, transitions=self.fa.transitions, initial_state=self.fa.initial_state, final_states=self.fa.final_states)
                    is_accepted = automaton.simulate(input_string)
                    result_text = f"The string '{input_string}' is accepted." if is_accepted else f"The string '{input_string}' is not accepted."
                    self.show_custom_message("String Acceptance Check", result_text)
            else:
                self.show_custom_message("Error", "Create FA first.")
        except Exception as e:
            self.show_custom_message("Error", f"Failed to check string acceptance: {str(e)}")

def convert_to_dfa(self):
        try:
            if self.fa_type == "NFA":
                nfa = NFA(states=self.fa.states, alphabet=self.fa.alphabet, transitions=self.fa.transitions, initial_state=self.fa.initial_state, final_states=self.fa.final_states)
                dfa = nfa.convert_to_dfa()
                self.fa = dfa
                self.fa_type = "DFA"
                self.show_custom_message("Conversion to DFA", "NFA converted to DFA successfully.")
                self.visualize_converted_fa()
                # self.visualize_fa()
            else:
                self.show_custom_message("Conversion to DFA", "Already a DFA or no FA created.")
        except Exception as e:
            self.show_custom_message("Error", f"Failed to convert to DFA: {str(e)}")

def minimize_dfa(self):
        try:
            if self.fa_type == "DFA":
                dfa = DFA(states=self.fa.states, alphabet=self.fa.alphabet, transitions=self.fa.transitions, initial_state=self.fa.initial_state, final_states=self.fa.final_states)
                dfa.minimize()
                self.fa = dfa
                self.show_custom_message("Minimization", "DFA minimized successfully.")
                # self.visualize_fa()
                self.visualize_converted_fa()
            else:
                self.show_custom_message("Error", "Provide a DFA.")
        except Exception as e:
            self.show_custom_message("Error", f"Failed to minimize DFA: {str(e)}")

def visualize_fa(self):
        try:
            output_dir = "fa_images"
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_dir, f"finite_automaton_{timestamp}.png")

            dot = self.fa.to_dot()
            dot.render(output_path, format='png', view=True)

        except Exception as e:
            self.show_custom_message("Error", f"Failed to visualize FA: {str(e)}")

def visualize_converted_fa(self):
        try:
            output_dir = "fa_images"
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_dir, f"finite_automaton_{timestamp}.png")

            dot = self.fa.draw_transition()
            dot.render(output_path, format='png', view=True)

        except Exception as e:
            self.show_custom_message("Error", f"Failed to visualize FA: {str(e)}")

def show_custom_message(self, title, message):
        popup = Toplevel(self.root)
        popup.title(title)
        popup.geometry("350x200")
        custom_font = ("Arial", 12)
        Label(popup, text=message, wraplength=250, font=custom_font).pack(pady=20)
        Button(popup, text="OK", width=10, height=2, font=custom_font, command=popup.destroy).pack(pady=20)