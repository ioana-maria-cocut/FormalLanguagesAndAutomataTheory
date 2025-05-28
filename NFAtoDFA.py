import NFA

#convertim un NFA in DFA
def nfa_to_dfa(nfa):
    #daca foisierul de configurare nu este corect de ce am mai continua?
    if not NFA.validate_nfa(nfa):
        print("NFA validation failed. Please check the configuration file for errors.")
        return None
    #prezentam starile si tranzitiile NFA-ului
    sigma, states, transitions, start_state, accept_states = NFA.config_nfa(nfa)
    print(f"Original NFA:")
    print(f"Sigma: {sigma}")
    print(f"States: {states}")
    print(f"Transitions: {transitions}")
    print(f"Start State: {start_state}")
    print(f"Accept States: {accept_states}")
    print()

    #calculam epsilon closure pentru starea de start
    start_closure = NFA.epsilon_closure([start_state], transitions)
    print(f"Start state epsilon closure: {start_closure}")

    #aceste for fi componentele DFA-ului
    dfa_states = []
    dfa_transitions = []
    dfa_accept_states = []
    dfa_start_state = None

    state_mapping = {}
    state_counter = 0
    unprocessed_states = []

    start_state_name = f"q{state_counter}"
    state_mapping[start_state_name] = sorted(start_closure)
    dfa_states.append(start_state_name)
    dfa_start_state = start_state_name
    unprocessed_states.append(start_state_name)
    state_counter += 1

    # verifica daca state-urile din closure-ul de start sunt accept states
    if any(state in accept_states for state in start_closure):
        dfa_accept_states.append(start_state_name)

    print(f"DFA start state {start_state_name} represents NFA states: {state_mapping[start_state_name]}")

    #procesam fiecare stare a DFA-ului pentru a construi tranzitiile
    while unprocessed_states:
        current_dfa_state = unprocessed_states.pop(0)
        current_nfa_states = state_mapping[current_dfa_state]

        print(f"\nProcessing DFA state {current_dfa_state} (NFA states: {current_nfa_states})")

        # computarea tranzitiilor pentru fiecare simbol din sigma
        for symbol in sigma:
            next_nfa_states = set()

            # cautam toate starile NFA-ului care pot fi atinse din starile curente cu simbolul dat
            for nfa_state in current_nfa_states:
                next_states = NFA.get_next_state(nfa_state, symbol, transitions)
                next_nfa_states.update(next_states)

            # calculam epsilon closure pentru starile NFA-ului care pot fi atinse
            if next_nfa_states:
                next_states_closure = NFA.epsilon_closure(list(next_nfa_states), transitions)
                next_states_closure_sorted = sorted(next_states_closure)

                print(
                    f"  On symbol '{symbol}': {current_nfa_states} -> {list(next_nfa_states)} -> ε-closure: {next_states_closure_sorted}")

                # verificam daca exista deja o stare DFA care corespunde acestui set de stari NFA
                existing_dfa_state = None
                for dfa_state, nfa_state_set in state_mapping.items():
                    if nfa_state_set == next_states_closure_sorted:
                        existing_dfa_state = dfa_state
                        break

                if existing_dfa_state:
                    target_state = existing_dfa_state
                    print(f"    -> Existing DFA state: {target_state}")
                else:
                    new_dfa_state = f"q{state_counter}"
                    state_mapping[new_dfa_state] = next_states_closure_sorted
                    dfa_states.append(new_dfa_state)
                    unprocessed_states.append(new_dfa_state)
                    target_state = new_dfa_state
                    state_counter += 1

                    if any(state in accept_states for state in next_states_closure_sorted):
                        dfa_accept_states.append(new_dfa_state)

                    print(f"    -> New DFA state: {target_state} (NFA states: {next_states_closure_sorted})")

                dfa_transitions.append((current_dfa_state, symbol, target_state))
                print(f"    -> Added DFA transition: {current_dfa_state} --{symbol}--> {target_state}")


    print(f"DFA Sigma: {sigma}")
    print(f"DFA States: {dfa_states}")
    print(f"DFA Start State: {dfa_start_state}")
    print(f"DFA Accept States: {dfa_accept_states}")
    print(f"DFA Transitions ({len(dfa_transitions)} total):")
    for trans in dfa_transitions:
        print(f"  {trans[0]} --{trans[1]}--> {trans[2]}")

    print(f"\nState Mapping (DFA state -> NFA states):")
    for dfa_state, nfa_state_set in state_mapping.items():
        accepting = " (ACCEPTING)" if dfa_state in dfa_accept_states else ""
        start = " (START)" if dfa_state == dfa_start_state else ""
        print(f"  {dfa_state}: {nfa_state_set}{accepting}{start}")

    #returnam DFA-ul sub forma unui dictionar
    return {
        'sigma': sigma,
        'states': dfa_states,
        'transitions': dfa_transitions,
        'start_state': dfa_start_state,
        'accept_states': dfa_accept_states,
        'state_mapping': state_mapping
    }


