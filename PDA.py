import Config
'''
Un PDA este definit ca un 7-tuplu (Σ, Γ, Q, δ, q0, F, Z0) unde:
- Σ este alfabetul de intrare (lista de simboluri) -> sigma
- Γ este alfabetul de stivă (lista de simboluri) -> gamma
- Q este multimea de stari (lista de stari) -> states
- δ : Q x (Σ U {ε}) x (Γ U {ε}) -> P(Q x Γ)* este functia de tranzitie (lista de tranzitii) -> transitions
- q0 este starea inițială (start_state) -> start_state
- F este multimea de stari de acceptare (lista de stari de acceptare) -> accept_states
- Z0 este simbolul de start al stivei (start_symbol) -> start_symbol
'''

def config_pda(pda):
    sigma = []
    gamma = []
    states = []
    transitions = []
    start_state = None
    accept_states = []
    start_symbol = None
    sections = Config.parse_file(pda)

    # procesaeea fiecare sectiuni pentru a popula componentele PDA-ului
    for section in sections:
        if section == "Sigma":
            # configurarea alfabetului de intrare
            for symbol in sections[section]:
                symbol = symbol.strip()
                if symbol not in sigma:
                    sigma.append(symbol)
        # configurarea alfabetului de stivă
        elif section == "Gamma":
            for symbol in sections[section]:
                symbol = symbol.strip()
                if symbol not in gamma:
                    gamma.append(symbol)
        # configurarea starilor
        elif section == "States":
            for state in sections[section]:
                state = state.strip()
                if '=' in state:
                    name, rest = state.split("=")
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
                        states.append(state.strip())
        # configurarea stării de start
        elif section == "StartSymbol":
            if sections[section]:
                start_symbol = sections[section][0].strip()
        # configurarea tranzitiilor
        elif section == "Transitions":
            for transition in sections[section]:
                if ">" in transition:
                    left, right = transition.split(">")
                    left_parts = left.strip().split()
                    right_parts = right.strip().split()

                    if len(left_parts) == 3 and len(right_parts) >= 1:
                        t1, s, top = left_parts
                        t2 = right_parts[0]
                        push = right_parts[1] if len(right_parts) > 1 else "ε"

                        transitions.append((t1.strip(), s.strip(), top.strip(), t2.strip(), push.strip()))

    return sigma, gamma, states, transitions, start_state, accept_states, start_symbol

# validarea configurarii PDA-ului
def validate_pda(pda):
    sections = Config.parse_file(pda)
    states = []
    sigma = []
    gamma = []
    transitions = []
    ok = True

    for section in sections:
        if section == "Sigma":
            for symbol in sections[section]:
                symbol = symbol.strip()
                if symbol not in sigma:
                    sigma.append(symbol)
                else:
                    print(f"Error: Symbol '{symbol}' is duplicated in Sigma section.")
                    ok = False
        elif section == "Gamma":
            for symbol in sections[section]:
                symbol = symbol.strip()
                if symbol not in gamma:
                    gamma.append(symbol)
                else:
                    print(f"Error: Symbol '{symbol}' is duplicated in Gamma section.")
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
                        states.append(state.strip())
            if number_start > 1:
                print("Error: More than one start state defined.")
                ok = False
            if number_accept == 0:
                print("Error: No accept state defined.")
                ok = False
            if number_start == 0:
                print("Error: No start state defined.")
                ok = False
        elif section == "StartSymbol":
            if not sections[section]:
                print("Error: No start symbol defined.")
                ok = False
            elif len(sections[section]) > 1:
                print("Error: Multiple start symbols defined.")
                ok = False
        elif section == "Transitions":
            for transition in sections[section]:
                if ">" not in transition:
                    print(
                        f"Error: Invalid transition: '{transition}'. Expected format: 'state input stack_top > new_state stack_push'.")
                    ok = False
                    continue

                left, right = transition.split(">")
                left_parts = left.strip().split()
                right_parts = right.strip().split()

                if len(left_parts) != 3 or len(right_parts) < 1:
                    ok = False
                    print(
                        f"Error: Invalid transition format '{transition}'. Expected format: 'state input stack_top > new_state stack_push'.")
                    continue

                t1, s, top = left_parts
                t2 = right_parts[0]
                push = right_parts[1] if len(right_parts) > 1 else "ε"

                if t1 not in states:
                    print(f"Error: Transition from non-existent state '{t1}'.")
                    ok = False
                if t2 not in states:
                    print(f"Error: Transition to non-existent state '{t2}'.")
                    ok = False
                if s not in sigma and s != 'ε':
                    print(f"Error: Transition with non-existent symbol '{s}'.")
                    ok = False
                if top not in gamma and top != 'ε':
                    print(f"Error: Transition with non-existent stack top '{top}'.")
                    ok = False
    return ok


def get_next_config(current_state, symbol, stack, transitions):
    # computarea următoarei configurații pe baza stării curente, simbolului de intrare și stivei
    next_configs = []

    #determinam ce simbol este in varful stivei
    if not stack:
        top = "ε"
    else:
        top = stack[-1]

    for transition in transitions:
        t1, s, stack_top, t2, push = transition

        # verificam daca vreo tranzitie este valida
        if (t1 == current_state and
                (s == symbol or s == 'ε') and
                (stack_top == top or stack_top == 'ε')):

            # creem o noua configuratie a stivei
            new_stack = stack.copy()

            # dam pop daca varful stivei nu este epsilon
            if stack_top != 'ε' and new_stack:
                new_stack.pop()

            # puenm noua valoare in stiva
            if push != 'ε':
                for char in reversed(push):
                    new_stack.append(char)

            input_consumed = 1 if s != 'ε' else 0

            next_configs.append((t2, new_stack, input_consumed))

    return next_configs

#simularea PDA-ului
def run_pda(pda):
    if not validate_pda(pda):
        print("PDA validation failed. Please check the configuration file for errors.")
        return None

    #componentele PDA-ului
    sigma, gamma, states, transitions, start_state, accept_states, start_symbol = config_pda(pda)
    print(f"Sigma: {sigma}")
    print(f"Gamma: {gamma}")
    print(f"States: {states}")
    print(f"Start State: {start_state}")
    print(f"Accept States: {accept_states}")
    print(f"Start Symbol: {start_symbol}")
    print(f"Transitions: {len(transitions)} total")
    for t in transitions:
        print(f"  {t[0]} {t[1]} {t[2]} > {t[3]} {t[4]}")
    print()

    string = input("Enter a string to test: ")

    # validarea simbolurilor din string
    for symbol in string:
        if symbol not in sigma:
            print(f"Error: Symbol '{symbol}' not in Sigma.")
            return

    # initializarea configuratiei PDA-ului
    initial_stack = [start_symbol] if start_symbol else []
    config = [(start_state, initial_stack, 0)]

    print(f"Starting configuration: State={start_state}, Stack={initial_stack}, Input='{string}'")
    print()

    step = 0
    max_steps = 10000  # nu vreau loop infinit nu am sa mint T_T

    #simulrea efectiva a PDA-ului
    while config and step < max_steps:
        step += 1
        new_config = []

        print(f"Step: {step}")

        for conf in config:
            current_state, current_stack, input_pos = conf

            print(f"  Configuration: State={current_state}, Stack={current_stack}, Position={input_pos}")


            if input_pos >= len(string):
                #verificam daca starea curenta este stare de accept
                if current_state in accept_states:
                    print(f"  -> ACCEPTED! Final state reached.")
                    print(f"The string '{string}' is accepted by the PDA.")
                    return

                # incercam o tranzitie epsilon daca nu mai avem simboluri de intrare
                next_configs = get_next_config(current_state, 'ε', current_stack, transitions)
                for next_state, next_stack, consumed in next_configs:
                    new_config.append((next_state, next_stack, input_pos + consumed))
                    print(
                        f"    Epsilon transition: {current_state} -> {next_state}, Stack: {current_stack} -> {next_stack}")
            else:
                # incercam tranzitii pe baza simbolului curent din string
                current_symbol = string[input_pos]
                next_configs = get_next_config(current_state, current_symbol, current_stack, transitions)

                for next_state, next_stack, consumed in next_configs:
                    new_config.append((next_state, next_stack, input_pos + consumed))
                    print(
                        f"    Transition on '{current_symbol}': {current_state} -> {next_state}, Stack: {current_stack} -> {next_stack}")

                epsilon_configs = get_next_config(current_state, 'ε', current_stack, transitions)
                for next_state, next_stack, consumed in epsilon_configs:
                    new_config.append((next_state, next_stack, input_pos + consumed))
                    print(
                        f"    Epsilon transition: {current_state} -> {next_state}, Stack: {current_stack} -> {next_stack}")

        config = new_config
        print()

        if not config:
            break

    if step >= max_steps:
        print(f"Maximum steps ({max_steps}) reached. Computation may be infinite.")

    print(f"The string '{string}' is not accepted by the PDA.")


