import customtkinter as ctk
from gui import FiniteAutomatonGUI

def main():
    root = ctk.CTk()
    root.title("Finite Automaton")
    app = FiniteAutomatonGUI(root)
    root.mainloop()

main()