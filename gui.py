import customtkinter as ctk
from tkinter import messagebox

class FiniteAutomaton:
    def __init__(self, states, symbols, start_state, final_states, transitions):
        self.states = states
        self.symbols = symbols
        self.start_state = start_state
        self.final_states = final_states
        self.transitions = transitions

    def is_deterministic(self):
        for state in self.transitions:
            for symbol in self.symbols:
                if len(self.transitions[state][symbol]) > 1:
                    return False
        return True

    def test_string(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol in self.transitions[current_state]:
                current_state = self.transitions[current_state][symbol][0]
            else:
                return False
        return current_state in self.final_states

# # Define the FA from the image
# states = {'q0', 'q1', 'q2'}
# symbols = {'1', '0'}
# start_state = 'q0'
# final_states = {'q2'}
# transitions = {
#     'q0': {'1': ['q1'], '0': ['q2']},
#     'q1': {'1': [], '0': []},
#     'q2': {'1': [], '0': []}
# }

row_count = 1
row_widgets = []  # Keep track of added rows for deletion

def add_row():
    global row_count
    new_label = ctk.CTkLabel(frame, text="Input State:")
    new_label.grid(row=row_count, column=0)
    
    new_entry_state = ctk.CTkEntry(frame)
    new_entry_state.grid(row=row_count, column=1)

    new_entry_trans = ctk.CTkEntry(frame)
    new_entry_trans.grid(row=row_count, column=2)
    
    row_widgets.append((new_label, new_entry_state, new_entry_trans))
    row_count += 1

def delete_row():
    global row_count
    if row_widgets:
        last_row = row_widgets.pop()
        for widget in last_row:
            widget.grid_forget()
        row_count -= 1
 


def check_deterministic():
    # is_dfa = fa.is_deterministic()
    # result_text = "The FA is deterministic." if is_dfa else "The FA is non-deterministic."
     messagebox.showinfo("Determinism Check", result_text)

def check_string_acceptance():
    # input_string = string_entry.get()
    # is_accepted = fa.test_string(input_string)
    # result_text = f"The string '{input_string}' is accepted." if is_accepted else f"The string '{input_string}' is not accepted."
     messagebox.showinfo("String Acceptance Check", result_text)
def constuct_DFA_from_NFA():
    messagebox.showinfo("constuct_DFA_from_NFA", result_text)

def Design_FA():
    messagebox.showinfo("Design_FA", result_text)

def Minimize_DFA():
    messagebox.showinfo("Minimize_DFA", result_text)
# Create the GUI
root = ctk.CTk()
root.title("Automaton")

frame = ctk.CTkFrame(root)
frame.pack(padx=200, pady=200)

# Create and place the initial label and entry for input
ctk.CTkLabel(frame, text="Input State:").grid(row=2, column=0)
string_entry = ctk.CTkEntry(frame)
string_entry.grid(row=2, column=1)

ctk.CTkLabel(frame, text="Tran").grid(row=0, column=2)
string_entry = ctk.CTkEntry(frame)
string_entry.grid(row=2, column=2)


# Create and place the button for adding rows
add_row_button = ctk.CTkButton(frame, text="Add Row", command=add_row)
add_row_button.grid(row=20, column=0)

# Create and place the button for deleting rows
add_row_button = ctk.CTkButton(frame, text="Delete Row", command=delete_row)
add_row_button.grid(row=20, column=1)

ctk.CTkLabel(frame, text="").grid(row=21, column=0)

acceptance_button = ctk.CTkButton(frame, text="Check Acceptance", command=check_string_acceptance)
acceptance_button.grid(row=22, column=0)

deterministic_button = ctk.CTkButton(frame, text="Check Determinism  ", command=check_deterministic)
deterministic_button.grid(row=23, column=0)

deterministic_button = ctk.CTkButton(frame, text="constuct DFA  ", command=constuct_DFA_from_NFA)
deterministic_button.grid(row=24, column=0)

deterministic_button = ctk.CTkButton(frame, text="Design FA", command=Design_FA)
deterministic_button.grid(row=25, column=0)

deterministic_button = ctk.CTkButton(frame, text="Minimize DFA ", command=Minimize_DFA)
deterministic_button.grid(row=26, column=0)

root.mainloop()
