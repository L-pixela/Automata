import customtkinter as ctk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os
import tempfile
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

        ctk.CTkLabel(self.frame, text="Transitions: (format: state symbol next_state)").grid(row=4, column=0)
        self.transitions_text = ctk.CTkTextbox(self.frame, width=300, height=100)
        self.transitions_text.grid(row=4, column=1)

        # Create buttons
        ctk.CTkButton(self.frame, text="Create FA", command=self.create_fa).grid(row=5, column=0, columnspan=2)
        ctk.CTkButton(self.frame, text="Check Determinism", command=self.check_determinism).grid(row=6, column=0, columnspan=2)
        ctk.CTkButton(self.frame, text="Check String Acceptance", command=self.check_string_acceptance).grid(row=7, column=0, columnspan=2)
        ctk.CTkButton(self.frame, text="Convert to DFA", command=self.convert_to_dfa).grid(row=8, column=0, columnspan=2)
        ctk.CTkButton(self.frame, text="Minimize DFA", command=self.minimize_dfa).grid(row=9, column=0, columnspan=2)

        # Image display for visualization
        self.image_label = ctk.CTkLabel(self.frame)
        self.image_label.grid(row=10, column=0, columnspan=2, pady=10)

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
                    state, symbol, next_state = transition.split()
                except ValueError:
                    messagebox.showerror("Error", f"Invalid transition format: '{transition}'")
                    return

                if state not in transitions:
                    messagebox.showerror("Error", f"Invalid state: '{state}'")
                    return
                if symbol not in alphabet:
                    messagebox.showerror("Error", f"Invalid symbol: '{symbol}'")
                    return
                if next_state not in states:
                    messagebox.showerror("Error", f"Invalid next state: '{next_state}'")
                    return

                if symbol not in transitions[state]:
                    transitions[state][symbol] = set()
                transitions[state][symbol].add(next_state)

            self.fa = FiniteAutomata()
            self.fa.states = set(states)
            self.fa.alphabet = alphabet
            self.fa.transitions = transitions
            self.fa.initial_state = initial_state
            self.fa.final_states = final_states

            messagebox.showinfo("Success", "Finite Automaton created successfully.")
            self.visualize_fa()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create Finite Automaton: {str(e)}")

    def check_determinism(self):
        try:
            if self.fa:
                is_deterministic = self.fa.is_deterministic()
                self.fa_type = "DFA" if is_deterministic else "NFA"
                result_text = f"The FA is {self.fa_type}."
                messagebox.showinfo("Determinism Check", result_text)
            else:
                messagebox.showerror("Error", "Create FA first.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check determinism: {str(e)}")

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
                    messagebox.showinfo("String Acceptance Check", result_text)
            else:
                messagebox.showerror("Error", "Create FA first.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check string acceptance: {str(e)}")

    def convert_to_dfa(self):
        try:
            if self.fa_type == "NFA":
                nfa = NFA()
                nfa.__dict__.update(self.fa.__dict__)
                dfa = nfa.convert_to_dfa()
                self.fa = dfa
                self.fa_type = "DFA"
                messagebox.showinfo("Conversion to DFA", "NFA converted to DFA successfully.")
                self.visualize_fa()
            else:
                messagebox.showinfo("Conversion to DFA", "Already a DFA or no FA created.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert to DFA: {str(e)}")

    def minimize_dfa(self):
        try:
            if self.fa_type == "DFA":
                dfa = DFA()
                dfa.__dict__.update(self.fa.__dict__)
                dfa.minimize()
                self.fa = dfa
                messagebox.showinfo("Minimization", "DFA minimized successfully.")
                self.visualize_fa()
            else:
                messagebox.showerror("Error", "Provide a DFA.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to minimize DFA: {str(e)}")

    def visualize_fa(self):
        try:
            dot = self.fa.to_dot()

            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                dot.render(temp_file.name, format='png')
                temp_file.close()
                img = Image.open(temp_file.name)
                img = img.resize((400, 400), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)

            self.image_label.configure(image=img)
            self.image_label.image = img  # Keep a reference to avoid garbage collection

            # Remove the temporary file after use
            os.remove(temp_file.name)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to visualize FA: {str(e)}")

# Main GUI setup
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Finite Automaton GUI")
    app = FiniteAutomatonGUI(root)
    root.mainloop()
