import Config

# configurarea DFA-ului punand toate datele in liste
def config_dfa(dfa):
    '''
    Un DFA este definit ca un 5-tuple (Σ, Q, δ, q0, F) unde:
    - Σ este alfabetul (lista de simboluri) -> sigma
    - Q este multimea de stari (lista de stari) -> states
    - δ este functia de tranzitie (lista de tranzitii) -> transitions
    - q0 este starea inițiala (start_state) -> start_state
    - F este multimea de stari de acceptare (lista de stari de acceptare) -> accept_states
    '''
    sigma = []
    states = []
    transitions = []
    start_state = None
    accept_states = []
    sections = Config.parse_file(dfa)

    for section in sections:
        #configurarea alfabetului
        if section == "Sigma":
            for symbol in sections[section]:
                sigma.append(symbol.strip())
        # configurarea starilor
        elif section == "States":
            for state in sections[section]:
                if '=' in state:
                    name, rest = state.split('=')
                    name = name.strip()
                    rest = rest.strip()
                    states.append(name)
                    # F este pentru starile de accept
                    if 'F' in rest:
                        accept_states.append(name)
                    # S este pentru starea de start
                    if 'S' in rest:
                        start_state = name
                else:
                    states.append(state.strip())
        # configurarea tranzitiilor
        # δ(t1, s) = t2
        elif section == "Transitions":
            for transition in sections[section]:
                parts = transition.split()
                if len(parts) == 3:
                    t1, s, t2 = parts
                    transitions.append((t1, s, t2))

    return sigma, states, transitions, start_state, accept_states


# testarea parsarii pentru ca nu functiona :(
def debug_config_dfa(dfa):
    sigma, states, transitions, start_state, accept_states = config_dfa(dfa)

    print("Sigma:", sigma)
    print("States:", states)
    print("Transitions:", transitions)
    print("Start state:", start_state)
    print("Accept states:", accept_states)

    return sigma, states, transitions, start_state, accept_states


# verifica, daca fisierul de configurare al DFA-ului este valid
def validate_dfa(dfa):
    sections = Config.parse_file(dfa)
    sigma = []
    states = []
    transitions = []
    ok = True

    # sigma states transitions se face pe baza corectitudinii
    for section in sections:
        if section == "Sigma":
            for symbol in sections[section]:
                if symbol not in sigma:
                    sigma.append(symbol)
                #sa nu fie simboluri duplicate
                else:
                    ok = False
                    print(f"Error: Symbol '{symbol}' is duplicated in Sigma section.")

        elif section == "States":
            number_start = 0
            number_accept = 0
            for state in sections[section]:
                if '=' in state:
                    name, rest = state.split('=')
                    name = name.strip()
                    rest = rest.strip()
                    if "F" in rest:
                        number_accept += 1
                    if "S" in rest:
                        number_start += 1
                    if name not in states:
                        states.append(name)
                    else:
                        ok = False
                        print(f"Error: State '{name}' is duplicated in States section.")
                else:
                    if state not in states:
                        states.append(state)
                    else:
                        ok = False
                        print(f"Error: State '{state}' is duplicated in States section.")

            # poate fi doar o stare de start si cel putin una de acceptare
            if number_start > 1:
                ok = False
                print("Error: More than one start state defined.")
            if number_accept == 0:
                ok = False
                print("Error: No accept state defined.")
            if number_start == 0:
                ok = False
                print("Error: No start state defined.")

        elif section == "Transitions":
            for transition in sections[section]:
                parts = transition.split()
                if len(parts) != 3:
                    ok = False
                    print(f"Error: Invalid transition format '{transition}'.")
                    continue

                t1, s, t2 = parts
                if t1 not in states:
                    ok = False
                    print(f"Error: Transition from non-existing state '{t1}'.")
                if t2 not in states:
                    ok = False
                    print(f"Error: Transition to non-existing state '{t2}'.")
                if s not in sigma:
                    ok = False
                    print(f"Error: Transition with non-existing symbol '{s}'.")
                if (t1, s, t2) not in transitions:
                    transitions.append((t1, s, t2))
                else:
                    ok = False
                    print(f"Error: Duplicate transition '{t1} --{s}--> {t2}'.")

    return ok

#functie care calculeaza urmatoarea stare a DFA-ului
def get_next_state(current_state, symbol, transitions):
    for transition in transitions:
        if transition[0] == current_state and transition[1] == symbol:
            return transition[2]
    return None

# functie care verifica daca starea curenta este o stare de acceptare
def is_accept_state(state, accept_states):
    return state in accept_states

# functie care ruleaza DFA-ul
def run_dfa(dfa):
    #verificam daca fisierul de configurare este valid
    if validate_dfa(dfa):
        sigma, states, transitions, start_state, accept_states = config_dfa(dfa)
        print(f"Sigma: {sigma}")
        print(f"States: {states}")
        print(f"Transitions: {transitions}")
        #input de pus in dfa ca sa vedem daca este acceptat
        string = input("Enter a string to test: ")
        current_state = start_state
        #verificam daca simbolurile din string sunt in alfabetul DFA-ului
        for symbol in string:
            if symbol not in sigma:
                print(f"Error: Symbol '{symbol}' not in Sigma.")
                return

        # chiar mergem prin DFA si prin toate starile yippieee
        for symbol in string:
            next_state = get_next_state(current_state, symbol, transitions)
            if next_state is None:
                print(f"Error: No transition for state '{current_state}' with symbol '{symbol}'.")
                return
            print(f"'{current_state}' -> '{next_state}' with '{symbol}'.")
            current_state = next_state
        if is_accept_state(current_state, accept_states):
            print(f"The string '{string}' is accepted by the DFA.")
        else:
            print(f"The string '{string}' is not accepted by the DFA. Ended in state '{current_state}'.")
    else:
        print("DFA validation failed. Please check the configuration file for errors.")
        return
