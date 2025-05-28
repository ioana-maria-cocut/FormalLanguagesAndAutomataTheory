# suma a doua numere unare
[Band]
1 1 1 + 1 1 1 $
[End]

[States]
qs
q1
qa
[End]

[Symbols]
1
+
$
[End]

[Transitions]
qs 1 qs 1 R
qs + qs 1 R
qs $ q1 s L
q1 1 qa $ R
[End]