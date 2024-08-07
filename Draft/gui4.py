import customtkinter as ctk
from tkinter import simpledialog, Toplevel, Label, Button
from PIL import Image, ImageTk
import os
import datetime
from FA5 import FiniteAutomata
from NFA import NFA
from DFA import DFA

class FiniteAutomatonGUI:
    def __init__(self, root):
        self.root = root
        self.fa = None
        self.fa_type = None

        self.frame = ctk.CTkFrame(root)
        self.frame.pack(padx=20, pady=20)

        # Create widgets for input
        ctk.CTkLabel(self.frame, text="Number of States:").grid(row=0, column=0)
        self.num_states_entry = ctk.CTkEntry(self.frame)
        self.num_states_entry.grid(row=0, column=1)

        ctk.CTkLabel(self.frame, text="Alphabet:").grid(row=1, column=0)
        self.alphabet_entry = ctk.CTkEntry(self.frame)
        self.alphabet_entry.grid(row=1, column=1)

        ctk.CTkLabel(self.frame, text="Initial State:").grid(row=2, column=0)
        self.initial_state_entry = ctk.CTkEntry(self.frame)
        self.initial_state_entry.grid(row=2, column=1)

        ctk.CTkLabel(self.frame, text="Final States:").grid(row=3, column=0)
        self.final_states_entry = ctk.CTkEntry(self.frame)
        self.final_states_entry.grid(row=3, column=1)

        ctk.CTkLabel(self.frame, text="Transitions: (format: state symbol next_state1,next_state2,...)").grid(row=4, column=0)
        self.transitions_text = ctk.CTkTextbox(self.frame, width=300, height=100)
        self.transitions_text.grid(row=4, column=1)

        # Create buttons
        ctk.CTkButton(self.frame, text="Create FA", command=self.create_fa).grid(row=5, column=0, columnspan=2)
        ctk.CTkButton(self.frame, text="Check Determinisic or not", command=self.check_determinism).grid(row=6, column=0, columnspan=2)
        ctk.CTkButton(self.frame, text="Check String Acceptance", command=self.check_string_acceptance).grid(row=7, column=0, columnspan=2)
        ctk.CTkButton(self.frame, text="Convert to DFA", command=self.convert_to_dfa).grid(row=8, column=0, columnspan=2)
        ctk.CTkButton(self.frame, text="Minimize DFA", command=self.minimize_dfa).grid(row=9, column=0, columnspan=2)

    def create_fa(self):

        try:
            num_states = int(self.num_states_entry.get()) #input number states
            states = [f"q{i}" for i in range(num_states)] #making states for the number states input using loop

            alphabet = set(self.alphabet_entry.get().split()) #input alphabet and the input are split by space
            initial_state = self.initial_state_entry.get() # get the input of initial_state

            final_states = set(self.final_states_entry.get().split()) # input of final_states, multiple final_states are split by space
            # transition validating the transition input with the input above like states, alphabet, init and final states
            transitions = {}
            for state in states:
                transitions[state] = {}
                for symbol in alphabet:
                    transitions[state][symbol] = set()# putting it in a set
            # input of transition split by going to another row and taking the input with format of state,symbol,next_states spliting by space
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

            self.fa = FiniteAutomata()
            self.fa.states = set(states)
            self.fa.alphabet = alphabet
            self.fa.transitions = transitions
            self.fa.initial_state = initial_state
            self.fa.final_states = final_states

            self.show_custom_message("Success", "Finite Automaton created successfully.")
            self.visualize_fa()

        except Exception as e:
            self.show_custom_message("Error", f"Failed to create Finite Automaton: {str(e)}")

        # try:
        #     num_states = int(self.num_states_entry.get()) #input number states
        #     states = [f"q{i}" for i in range(num_states)] #making states for the number states input using loop

        #     alphabet = set(self.alphabet_entry.get().split()) #input alphabet and the input are split by space
        #     initial_state = self.initial_state_entry.get() # get the input of initial_state

        #     final_states = set(self.final_states_entry.get().split()) # input of final_states, multiple final_states are split by space
        #     # transition validating the transition input with the input above like states, alphabet, init and final states
        #     transitions = {}
        #     for state in states:
        #         transitions[state] = {}
        #         for symbol in alphabet:
        #             transitions[state][symbol] = set() # putting it in a set
        #     # input of transition split by going to another row and taking the input with format of state,symbol,next_states spliting by space
        #     transitions_input = self.transitions_text.get("1.0", "end").strip().split("\n")
        #     for transition in transitions_input:
        #         try:
        #             state, symbol, next_state = transition.split()
        #         except ValueError:
        #             self.show_custom_message("Error", f"Invalid transition format: '{transition}'")
        #             return

        #         if state not in transitions:
        #             self.show_custom_message("Error", f"Invalid state: '{state}'")
        #             return
        #         if symbol not in alphabet:
        #             self.show_custom_message("Error", f"Invalid symbol: '{symbol}'")
        #             return
        #         if next_state not in states:
        #             self.show_custom_message("Error", f"Invalid next state: '{next_state}'")
        #             return

        #         if symbol not in transitions[state]:
        #             transitions[state][symbol] = set()
        #         transitions[state][symbol].add(next_state)

        #     self.fa = FiniteAutomata()
        #     self.fa.states = set(states)
        #     self.fa.alphabet = alphabet
        #     self.fa.transitions = transitions
        #     self.fa.initial_state = initial_state
        #     self.fa.final_states = final_states

        #     self.show_custom_message("Success", "Finite Automaton created successfully.")
        #     self.visualize_fa()

        # except Exception as e:
        #     self.show_custom_message("Error", f"Failed to create Finite Automaton: {str(e)}")

    def check_determinism(self):
        try:
            if self.fa:
                is_deterministic = self.fa.is_deterministic()
                self.fa_type = "DFA" if is_deterministic else "NFA"
                result_text = f"The FA is {self.fa_type}."
                self.show_custom_message("Deterministic or not Check", result_text)
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
                        automaton = DFA()
                    else:
                        automaton = NFA()
                    automaton.__dict__.update(self.fa.__dict__)
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
                nfa = NFA()
                nfa.__dict__.update(self.fa.__dict__)
                dfa = nfa.convert_to_dfa()
                self.fa = dfa
                self.fa_type = "DFA"
                print("DFA Transitions:")
                for state, transitions in dfa.transitions.items():
                    for symbol, next_state in transitions.items():
                        print(f"Transition: {state} --[{symbol}]--> {next_state}")
                self.show_custom_message("Conversion to DFA", "NFA converted to DFA successfully.")
                self.visualize_fa()
            else:
                self.show_custom_message("Conversion to DFA", "Already a DFA or no FA created.")
        except Exception as e:
            self.show_custom_message("Error", f"Failed to convert to DFA: {str(e)}")

    def minimize_dfa(self):
        try:
            if self.fa_type == "DFA":
                dfa = DFA()
                dfa.__dict__.update(self.fa.__dict__)
                dfa.minimize()
                self.fa = dfa
                print("DFA Transitions:")
                for state, transitions in dfa.transitions.items():
                    for symbol, next_state in transitions.items():
                        print(f"Transition: {state} --[{symbol}]--> {next_state}")
                self.show_custom_message("Minimization", "DFA minimized successfully.")
                self.visualize_fa()
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

            # img = Image.open(output_path)
            # img = img.resize((400, 400), Image.ANTIALIAS)
            # img = ImageTk.PhotoImage(img)

            # # Create a new Toplevel window to display the image
            # popup = Toplevel(self.root)
            # popup.title("Finite Automaton Visualization")

            # image_label = Label(popup, image=img)
            # image_label.image = img  # Keep a reference to avoid garbage collection
            # image_label.pack(padx=10, pady=10)

        except Exception as e:
            self.show_custom_message("Error", f"Failed to visualize FA: {str(e)}")

    def show_custom_message(self, title, message):
        popup = Toplevel(self.root)
        popup.title(title)
        popup.geometry("350x200")
        # Define a custom font with a specific size
        custom_font = ("Arial", 12)
        # Label for the message to appear
        Label(popup, text=message, wraplength=250, font=custom_font).pack(pady=20)
        # Button for the message
        Button(popup, text="OK", width=10, height=2, font=custom_font, command=popup.destroy).pack(pady=20)

# Main GUI setup
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Finite Automaton")
    app = FiniteAutomatonGUI(root)
    root.mainloop()
