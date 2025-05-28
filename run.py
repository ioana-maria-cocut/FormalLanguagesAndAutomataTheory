import Config
import DFA
from DFA import debug_config_dfa
import NFA
from NFA import config_nfa, validate_nfa
import os
import PDA
import NFAtoDFA
import TuringMachine

# states = Config.parse_file("15a.dfa")
# print(states)
# debug_config_dfa("15a.dfa")
# DFA.run_dfa("15a.dfa")
# NFA.run_nfa("curs3N1.nfa")

def display_menu():
    print("1. Run DFA")
    print("2. Run NFA")
    print("3. Convert NFA to DFA")
    print("4. Run PDA")
    print("5. Run Turing Machine")
    print("6. Exit")

def run_menu():
    print("Welcome to cs112 lab! Please select an option:")
    option = None
    while option != "6":
        display_menu()
        option = input("Enter your choice (1-6): ")
        if option == "1":
            ok = False
            while ok == False:
                dfa_file = input("Enter the DFA configuration file name: ")
                if os.path.exists(dfa_file):
                    ok = True
                    DFA.run_dfa(dfa_file)
                else:
                    print(f"File '{dfa_file}' does not exist. Please try again.")
        elif option == "2":
            ok = False
            while ok == False:
                nfa_file = input("Enter the NFA configuration file name: ")
                if os.path.exists(nfa_file):
                    ok = True
                    NFA.run_nfa(nfa_file)
                else:
                    print(f"File '{nfa_file}' does not exist. Please try again.")
        elif option == "3":
            ok = False
            while ok == False:
                nfa_file = input("Enter the NFA configuration file name: ")
                if os.path.exists(nfa_file):
                    ok = True
                    NFAtoDFA.nfa_to_dfa(nfa_file)
                else:
                    print(f"File '{nfa_file}' does not exist. Please try again.")
        elif option == "4":
            ok = False
            while ok == False:
                pda_file = input("Enter the PDA configuration file name: ")
                if os.path.exists(pda_file):
                    ok = True
                    PDA.run_pda(pda_file)
                else:
                    print(f"File '{pda_file}' does not exist. Please try again.")
        elif option == "5":
            ok = False
            while ok == False:
                tm_file = input("Enter the Turing Machine configuration file name: ")
                if os.path.exists(tm_file):
                    ok = True
                    TuringMachine.run_tm(tm_file)
                else:
                    print(f"File '{tm_file}' does not exist. Please try again.")
    print("Exiting the program. Goodbye!")


run_menu()