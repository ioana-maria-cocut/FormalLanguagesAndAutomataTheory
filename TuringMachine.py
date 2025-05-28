#simulam executarea unei masini Turing
def run_tm(tm):
    f = open(tm, "r")
    lines = f.readlines()

    #initializam componenetele masinii Turing
    band = []
    states = []
    symbols = []
    transitions = []

    mode = 0  # 0: initial, 1: band, 2: states, 3: symbols, 4: transitions
    for line in lines:
        line = line.strip()
        if (line or not line.startswith("#")):
            if line == "[Band]":
                mode = 1
            elif line == "[States]":
                mode = 2
            elif line == "[Symbols]":
                mode = 3
            elif line == "[Transitions]":
                mode = 4
            elif line == "[End]":
                mode = -1
            else :
                if mode == 1:
                    band = line.split(" ")
                    print (band)
                elif mode == 2:
                    states.append(line);
                    print (states)
                elif mode == 3:
                    symbols.append(line)
                    print (symbols)
                elif mode == 4:
                    transition = line.split(" ")
                    print(transition)
                    transitions.append(tuple(transition))
                else:
                    print("Error: Invalid mode")
                    exit(1)
    f.close()
    print(transitions)

    #functie care ne returneaza urmatoarea tranzitie in functie de starea curenta si simbolul curent
    def getCurrentTransition(state, symbol):
        for transition in transitions:
            if transition[0] == state and transition[1] == symbol:
                return transition
        return None

    # de aici incepem simularea masinii Turing
    CurrentState = states[0]
    CurrentPosition = 0
    CurrentSymbol = band[CurrentPosition]

    while CurrentState != states[-1]:
        transition = getCurrentTransition(CurrentState, CurrentSymbol)
        print(transition)
        NextState = transition[2]
        NextPosition = transition[4]

        band[CurrentPosition] = transition[3]

        if NextPosition == "R":
            CurrentPosition += 1
        elif NextPosition == "L":
            CurrentPosition -= 1

        CurrentSymbol = band[CurrentPosition]
        CurrentState = NextState

    print (band)