#asta era un test pentru ai sa imi creeze un fisier de configurare pentru o machine de Turing
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