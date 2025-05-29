# Formal languages and Automata Theory
This repository contains the code I worked on for my CS112 course. During the laboratoy I worked on DFA, NFA, and regular expressions. The code is written in Python and is designed to be easy to understand and modify.
<br>
To run the code, you need to have Python installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).
Open the script in your favorite IDE or text editor, and run the run.py file. The code is well-commented, so you can easily understand how it works.

This repository contains the .py files and some examples you can verify with the ending corespponding to the .py name.

## Structurile fisierelor pentru testare
Structura fisierelor .dfa
```
# comentarii
# Un DFA este definit ca un 5-tuple (Σ, Q, δ, q0, F) unde:
#    - Σ este alfabetul (lista de simboluri) -> sigma
#    - Q este multimea de stari (lista de stari) -> states
#    - δ este functia de tranzitie (lista de tranzitii) -> transitions
#    - q0 este starea inițiala (start_state) -> start_state
#    - F este multimea de stari de acceptare (lista de stari de acceptare) -> accept_states

Sigma:
    word1
    word2
    ...
    wordk
End

# o stare urmata de "=" si de S (start) sau F (accept) in orice ordine arata felul de stare
States:
    state1 = S F
    state2 
    ...
    statek = F
End

# δ(statea, wordk) = stateb
Transitions:
    statex worda statey
    stateq wordc statew
    ...
    statez wordl stateb
End
```

Structura fisierelor .nfa:
```
#comentarii
#Un NFA este definit ca un 5-tuplu (Σ, Q, δ, q0, F) unde:
#    - Σ este alfabetul (lista de simboluri) -> sigma
#    - Q este multimea de stari (lista de stari) -> states
#    - δ : Q x (Σ U {ε}) -> P(Q)  este functia de tranzitie (lista de tranzitii) -> transitions
#    - q0 este starea inițiala (start_state) -> start_state
#    - F este multimea de stari de acceptare (lista de stari de acceptare) -> accept_states
# puteti folosi ε pentru tranzitii
Sigma:
    word1
    word2
    ...
    wordk
End

# o stare urmata de "=" si de S (start) sau F (accept) in orice ordine arata felul de stare
States:
    state1 = S F
    state2 
    ...
    statek = F
End

# δ(statea, wordk) = stateb
Transitions:
    statex worda statey
    stateq wordc statew
    ...
    statez wordl stateb
End

```

Structura fisierelor .pda:

```
#comentarii
# Un PDA este definit ca un 7-tuplu (Σ, Γ, Q, δ, q0, F, Z0) unde:
#   - Σ este alfabetul de intrare (lista de simboluri) -> sigma
#   - Γ este alfabetul de stivă (lista de simboluri) -> gamma
#   - Q este multimea de stari (lista de stari) -> states
#   - δ : Q x (Σ U {ε}) x (Γ U {ε}) -> P(Q x Γ)* este functia de tranzitie (lista de tranzitii) -> transitions
#   - q0 este starea inițială (start_state) -> start_state
#   - F este multimea de stari de acceptare (lista de stari de acceptare) -> accept_states
#   - Z0 este simbolul de start al stivei (start_symbol) -> start_symbol
# puteti folosi ε pentru tranzitii

Sigma:
    word1
    word2
    ...
    wordk
End

Gamma:
    stack1
    stack2
    ...
    stackn
End

StartSymbol:
    stackf
End

# o stare urmata de "=" si de S (start) sau F (accept) in orice ordine arata felul de stare
States:
    state1 = S F
    state2 
    ...
    statek = F
End

#δ(statea, word2, stack8) = (stateh, newStack)
Transitions:
    statex worda statey
    stateq wordc statew
    ...
    statez wordl stateb
End

```

Structura fisierelor .tm
```
#comentarii
#acesta este un exemplu pe care mi l-a dat claude.ai care nu functioneaza eu 1 - ai 0
[Band]
1 1 1 + 1 1 + 1 1 1 $
[End]

[States]
qs
q1
q2
q3
qa
[End]

[Symbols]
1
+
$
[End]

[Transitions]
qs 1 qs 1 R
qs + q1 1 R
q1 1 q1 1 R
q1 + q2 1 R
q2 1 q2 1 R
q2 $ qa $ L
[End]
```
