import Config

def config_nfa(nfa):
    '''
    Un NFA este definit ca un 5-tuplu (Σ, Q, δ, q0, F) unde:
    - Σ este alfabetul (lista de simboluri) -> sigma
    - Q este multimea de stari (lista de stari) -> states
    - δ : Q x (Σ U {ε}) -> P(Q)  este functia de tranzitie (lista de tranzitii) -> transitions
    - q0 este starea inițiala (start_state) -> start_state
    - F este multimea de stari de acceptare (lista de stari de acceptare) -> accept_states
    '''
    sigma = []
    states = []
    transitions = []
    start_state = None
    accept_states = []
    sections = Config.parse_file(nfa)
#cam aceeasi chestie ca la DFA, doar ca aici avem si epsilon
    for section in sections:
        if section == "Sigma":
            for symbol in sections[section]:
                symbol = symbol.strip()
                if symbol not in sigma:
                    sigma.append(symbol)
        elif section == "States":
            for state in sections[section]:
                state = state.strip()
                if '=' in state:
                    name, rest = state.split('=')
                    name = name.strip()
                    rest = rest.strip()
                    if name not in states:
                        states.append(name)
                    if 'F' in rest:
                        accept_states.append(name)
                    if 'S' in rest:
                        if start_state is None:
                            start_state = name
                else:
                    if state not in states:
                        states.append(state)
        elif section == "Transitions":
            for transition in sections[section]:
                parts = transition.split()
                if len(parts) == 3:
                    t1, s, t2 = parts
                    transitions.append((t1.strip(), s.strip(), t2.strip()))
    return sigma, states, transitions, start_state, accept_states

def validate_nfa(nfa):
    sections = Config.parse_file(nfa)
    states = []
    sigma = []
    transitions = []
    ok = True
# cam aceeasi chestie ca la DFA, doar ca aici avem si epsilon
    for section in sections:
        if section == "Sigma":
            for symbol in sections[section]:
                symbol = symbol.strip()
                if symbol not in sigma:
                    sigma.append(symbol)
                else:
                    print(f"Error: Symbol '{symbol}' is duplicated in Sigma section.")
                    ok = False
        elif section == "States":
            number_start = 0
            number_accept = 0
            for state in sections[section]:
                state = state.strip()
                if '=' in state:
                    name, rest = state.split('=')
                    name = name.strip()
                    rest = rest.strip()
                    if name not in states:
                        states.append(name)
                    else:
                        print(f"Error: State '{name}' is duplicated in States section.")
                        ok = False
                    if 'F' in rest:
                        number_accept += 1
                    if 'S' in rest:
                        number_start += 1
                else:
                    if state not in states:
                        states.append(state)
                    else:
                        print(f"Error: State '{state}' is duplicated in States section.")
                        ok = False
            if number_start == 0:
                print("Error: No start state defined.")
                ok = False
            if number_start > 1:
                print("Error: More than one start state defined.")
                ok = False
            if number_accept == 0:
                print("Error: No accept state defined.")
                ok = False
        elif section == "Transitions":
            for transition in sections[section]:
                parts = transition.split()
                if len(parts) != 3:
                    print(f"Error: Invalid transition format '{transition}'.")
                    ok = False
                    continue
                t1, s, t2 = parts
                if t1 not in states:
                    print(f"Error: Transition from non-existent state '{t1}'.")
                    ok = False
                if t2 not in states:
                    print(f"Error: Transition to non-existent state '{t2}'.")
                    ok = False
                if s not in sigma and s != 'ε':
                    print(f"Error: Transition with non-existent symbol '{s}'.")
                    ok = False
                if (t1, s, t2) not in transitions:
                    transitions.append((t1, s, t2))
                else:
                    print(f"Error: Transition '{t1} --{s}--> {t2}' is duplicated.")
                    ok = False
    return ok


def get_next_state(current_state, symbol, transitions):
    next_states = []
    for transition in transitions:
        if transition[0] == current_state and transition[1] == symbol:
            next_states.append(transition[2])
    return next_states

def epsilon_closure(states, transitions):
    closure = set(states)
    stack = list(states)

    while stack:
        current = stack.pop()

        epsilon_transition = get_next_state(current, 'ε', transitions)

        for next_state in epsilon_transition:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return list(closure)

def run_nfa(nfa):
    if not validate_nfa(nfa):
        print("NFA validation failed. Please check the configuration file for errors.")
        return
    else:
        sigma, states, transitions, start_state, accept_states = config_nfa(nfa)
        print(f"Sigma: {sigma}")
        print(f"States: {states}")
        print(f"Transitions: {transitions}")
        print(f"Start State: {start_state}")
        print(f"Accept States: {accept_states}")

        string = input("Enter a string to test: ")

        for symbol in string:
            if symbol not in sigma and symbol != 'ε':
                print(f"Error: Symbol '{symbol}' not in Sigma.")
                return

        current_states = epsilon_closure([start_state], transitions)
        print(f"Current States: {current_states}")

        for symbol in string:
            next_states = []

            for state in current_states:
                next_states.extend(get_next_state(state, symbol, transitions))

            if not next_states:
                print(f"Error: No transition for state(s) {current_states} with symbol '{symbol}'. String rejected.")
                return

            current_states = epsilon_closure(next_states, transitions)
            print(f"After symbol '{symbol}' : '{current_states}'")

        accepted = any(state in accept_states for state in current_states)

        if(accepted):
            accept_state_found = [state for state in current_states if state in accept_states]
            print(f"The string '{string}' is accepted by the NFA. Ended in state(s): {accept_state_found}.")
        else:
            print(f"The string '{string}' is not accepted by the NFA. Ended in state(s): '{current_states}'.")
    return


